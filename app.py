import os
import cv2
import tempfile
import traceback
import warnings
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import PIL
from pathlib import Path
import gradio as gr
import numpy as np
from modelscope.models import Model

# Silence known deprecation warning from pkg_resources used by modelscope
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API.*")

# Set model cache directory to project root
MODEL_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
os.environ['MODELSCOPE_CACHE'] = MODEL_CACHE_DIR
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)

# Lazy-loaded model handle
img_colorization = None
model_loaded = False


def load_model():
    """Attempt to download/load the model. Returns a status message."""
    global img_colorization, model_loaded
    try:
        print("Loading model from cache or downloading...")
        img_colorization = pipeline(Tasks.image_colorization, model='iic/cv_ddcolor_image-colorization')
        model_loaded = True
        print("Model loaded successfully!")
        return "Model ready. Upload an image to colorize."
    except Exception as e:
        img_colorization = None
        model_loaded = False
        tb = traceback.format_exc()
        print(f"Model load error: {e}")
        return f"Failed to load model: {e}\n\n{tb}"


def inference_run(img_path):
    """Run inference if model is loaded; else return informative message."""
    if not model_loaded or img_colorization is None:
        return None, "Model is loading... Please wait or try again in a moment."

    try:
        image = cv2.imread(str(img_path))
        if image is None:
            return None, "Error: Could not read image file. Please check the file format."
        output = img_colorization(image[..., ::-1])
        result = output[OutputKeys.OUTPUT_IMG].astype(np.uint8)

        temp_dir = tempfile.mkdtemp()
        out_path = os.path.join(temp_dir, 'colorify_image.png')
        cv2.imwrite(out_path, result)
        return Path(out_path), "✓ Image colorized successfully!"
    except Exception as e:
        tb = traceback.format_exc()
        return None, f"Inference error: {e}\n\n{tb}"


title = "Colorify"

# Global flag for async model loading
model_load_thread = None

def load_model_async():
    """Load model in background thread."""
    global img_colorization, model_loaded
    try:
        print("Loading model from local cache...")
        # Use local model path
        local_model_path = os.path.join(MODEL_CACHE_DIR, 'models', 'iic', 'cv_ddcolor_image-colorization')
        
        if os.path.exists(local_model_path):
            print(f"Found local model at {local_model_path}")
            img_colorization = pipeline(Tasks.image_colorization, model=local_model_path)
        else:
            print(f"Local model not found at {local_model_path}")
            # Try to load from ModelScope as fallback
            img_colorization = pipeline(Tasks.image_colorization, model='iic/cv_ddcolor_image-colorization')
        
        model_loaded = True
        print("✓ Model loaded successfully!")
    except Exception as e:
        print(f"Model load error: {e}")
        model_loaded = False

# Start model loading in background thread
import threading
model_load_thread = threading.Thread(target=load_model_async, daemon=True)
model_load_thread.start()

with gr.Blocks(title=title) as demo:
    # Title and tagline with inline styles
    gr.HTML("<style>"
            "footer{display:none !important;} .footer{display:none !important;} .gradio-footer{display:none !important;}"
            "@keyframes glow {0%, 100% {text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #fff;} 50% {text-shadow: 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #fff;}}"
            ".neon-title {animation: glow 2s ease-in-out infinite;}"
            ".gradio-image {min-height: 700px !important;}"
            ".gradio-row:last-child {text-align: center;}"
            ".gradio-button {width: 200px !important; margin: 0 auto !important;}"
            "</style>"
            "<div style='text-align:center'>"
            "<h1 class='neon-title' style='margin-bottom:6px; font-size:80px; font-weight:700; color:#fff;'>🎨Colorify</h1>"
            "<p style='margin-top:0; color:#fff; font-size:18px; font-weight:500; letter-spacing:0.5px;'>Upload a black-and-white photo and let the model bring it to life</p>"
            "</div>")

    with gr.Row():
        inp = gr.Image(type="filepath", label="Input", scale=1, sources=["upload"])
        out = gr.Image(type="pil", label="Output", scale=1)

    with gr.Row():
        run_btn = gr.Button("Colorize", min_width=80)

    def run_and_status(img):
        if img is None:
            return None
        if not model_loaded:
            print("Model is still loading... Please wait.")
            return None
        out_path, msg = inference_run(img)
        print(f"Inference result: {msg}")
        return out_path

    run_btn.click(fn=run_and_status, inputs=[inp], outputs=[out])

# Launch (footer hidden via CSS)
demo.queue().launch()

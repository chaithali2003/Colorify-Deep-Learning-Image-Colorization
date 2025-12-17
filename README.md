---
title: Colorify - Image Colorization
emoji: 🎨
colorFrom: indigo
colorTo: cyan
sdk: gradio
sdk_version: 3.50.0
app_file: app.py
pinned: false
license: apache-2.0
---

# Colorify 🎨

Transform black-and-white photos into vibrant, colorized images using advanced AI powered by ModelScope's DDColor model.

## Features

- 🖼️ **Automatic Image Colorization** - Convert grayscale images to color using deep learning
- ⚡ **Fast Processing** - Efficient inference on CPU/GPU
- 🎯 **Easy to Use** - Simple web interface built with Gradio
- 📥 **Automatic Model Download** - Model downloads and caches locally on first run
- 🎨 **Beautiful UI** - Modern neon-styled interface with smooth animations

## Project Structure

```
Colorify/
├── app.py                 # Main Gradio application
├── style.css             # (Optional) External stylesheet
├── logo.png              # App logo/favicon
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore          # Git ignore rules
└── models/             # Model cache directory (auto-created)
    └── models/iic/cv_ddcolor_image-colorization/
```

## Requirements

- Python 3.8+
- 2GB+ disk space for model weights
- Internet connection (first run to download model)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Colorify
```

### 2. Create Virtual Environment (Recommended)

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages:
- gradio (3.50.0)
- modelscope
- torch
- opencv-python
- numpy
- Pillow
- sentencepiece
- timm

## Usage

### Run the Application
```bash
python app.py
```

The application will:
1. Start the Gradio web server at `http://127.0.0.1:7860`
2. Begin downloading the colorization model in background (first run only)
3. Display "Loading model... Please wait" until model is ready

### Using the Web Interface

1. **Upload Image** - Click "Input" to upload a black-and-white photo
2. **Colorize** - Click the "Colorize" button
3. **Download Result** - The colorized image appears in the "Output" box and can be saved

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- WebP (.webp)

## Model Information

**Model:** DDColor Image Colorization  
**Source:** [ModelScope - iic/cv_ddcolor_image-colorization](https://modelscope.cn/models/iic/cv_ddcolor_image-colorization)  
**Framework:** PyTorch  
**Model Size:** ~500MB  
**Input:** Grayscale or color images (H×W×3)  
**Output:** Colorized image (H×W×3)  
**Hardware:** Works on CPU (slower) or GPU (faster)

## Configuration

### Model Cache Location
The model is cached in `./models/` directory in the project root. To use a custom location, modify:
```python
MODEL_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

```

## Acknowledgments

- **ModelScope** for the DDColor model
- **Gradio** for the web framework
- **PyTorch** team for the deep learning framewor

```

Made with ❤️ by Chaithali S


# POC Wireframe Repository Summary

## Project Overview
**poc-wireframe** is a Python-based proof of concept for wireframe extraction from application screenshots. The project uses AI models to analyze UI screenshots and extract layout information, components, and features to help generate recommended wireframes for new applications.

## Business Goal
Automate the tedious process of:
1. Installing and testing apps (10 apps each time)
2. Adding testing data
3. Using apps to collect MVP features
4. Summarizing MVP features across apps
5. Creating recommended wireframes for new applications

## Repository Structure

### Root Directory
```
poc-wireframe/
├── README.md                 # Project overview and goals
├── requirements.txt        # Python dependencies
├── setup.py               # Python setup script
├── input/                # Input data directory
│   └── screenshots/      # Screenshot images (8 WordPress admin screenshots)
├── output/              # Generated analysis results
├── src/                # Source code (Python implementation)
│   ├── extract.py         # Main extraction script
│   └── extract/          # Extraction modules
│       ├── find_screenshots.py  # Screenshot discovery
│       └── analyze_image.py     # AI image analysis
├── README_PYTHON.md         # Python implementation notes
```

### Source Code Structure

#### Python Implementation (Primary)
- `src/extract.py` - Main Python extraction script
- `src/extract/find_screenshots.py` - Screenshot discovery functionality
- `src/extract/analyze_image.py` - Image analysis using Qwen2.5-VL-7B-Instruct model

#### JavaScript/TypeScript Files (Reference Examples Only)
- `src/extract/analyze-image.ts` - Example image analysis using Florence-2-large via Hugging Face API

## Technology Stack

### Python Implementation (Primary)
- **Runtime**: Python 3.13+
- **AI Model**: Qwen2.5-VL-7B-Instruct (local processing)
- **Dependencies**:
  - `transformers` - Hugging Face transformers library
  - `torch` - PyTorch for model inference
  - `Pillow` - Image processing
  - `accelerate` - Model loading optimization

## Available Scripts

### Python Scripts (Primary)
- `python setup.py` - Install Python dependencies
- `python src/extract.py` - Run Python extraction (requires transformers installation)

## Input Data
The `input/screenshots/` directory contains 8 WordPress admin interface screenshots:
- 2 general screenshots
- 6 WordPress admin panel captures from various dates in August 2025

## Processing Pipeline

### Current Implementation Flow
1. **Screenshot Discovery**: Scan `input/screenshots/` for image files (PNG, JPG, JPEG)
2. **Image Analysis**: Process first image with AI model to extract:
   - Overall screen description and purpose
   - UI components (buttons, forms, navigation)
   - Text content visible in interface
   - Layout structure and organization
   - Interactive elements and features
   - Screen type/category classification
3. **Output Generation**: Save analysis to `output/analyze-image.text`

### Planned Full Pipeline (from README)
1. Read image files from input/screenshots
2. For each image: Call image-to-text to analyze screen content, layout, components
3. Group images by screen
4. For each screen: Summarize extracted data, UI layout, short description
5. Save extracted data in `output/screen/[screen_name].json`

## Key Features

### Current Capabilities
- ✅ Screenshot file discovery and metadata extraction
- ✅ AI-powered UI analysis with structured output
- ✅ WordPress admin interface analysis focus
- ✅ Output file generation with timestamps

### Future Components (inspired by example scripts)
- Feature extraction and analysis 
- Wireframe suggestion generation 
- Enhanced main application entry point
- Multi-image extraction workflow

## Implementation Status

### Completed Python Features
- ✅ Screenshot discovery functionality
- ✅ Image analysis with Qwen2.5-VL-7B-Instruct
- ✅ Main extraction script
- ✅ Dependencies and setup
- ✅ Output handling

### Benefits of Python Implementation
- **Cost Effective**: No API usage costs (local processing)
- **Privacy**: Images processed locally
- **Offline Capability**: Works without internet
- **Customization**: Direct model parameter access
- **No API Token Required**: Eliminates authentication complexity

## Development Commands

### Setup and Installation
```bash
# Python (primary implementation)
python setup.py
# or manually: pip install -r requirements.txt
```

### Running the Application
```bash
# Python implementation
python src/extract.py
```

### Testing
```bash
# Test screenshot discovery (if test files exist)
python src/python/test_find_screenshots.py
```

## File Locations for Development

### Key Files to Monitor
- `src/extract/analyze_image.py:7` - Python UI analysis function  
- `src/extract/find_screenshots.py:7` - Python screenshot discovery
- `src/extract.py` - Main Python extraction script
- `requirements.txt` - Python dependencies

### Configuration Files
- `requirements.txt` - Python dependencies
- `setup.py` - Python installation script

## Current State Summary
This repository contains a Python implementation for wireframe extraction from application screenshots. The JavaScript/TypeScript files serve as reference examples showing alternative implementation approaches. The primary working code is in Python, using local AI model processing with Qwen2.5-VL-7B-Instruct for analyzing WordPress admin interface screenshots with plans for broader application wireframe extraction.
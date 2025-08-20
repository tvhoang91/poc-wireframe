# Python Migration for POC Wireframe

This directory contains the Python version of the wireframe extraction tool, migrated from the original TypeScript implementation.

## Migration Changes

### From TypeScript to Python
- **Original**: Uses `@huggingface/inference` and `@huggingface/transformers` (Node.js)
- **New**: Uses `transformers` library with `pipeline` (Python)

### Model Change
- **Original**: Florence-2-large via Hugging Face Inference API
- **New**: Qwen2.5-VL-7B-Instruct via local Transformers pipeline

## Setup

1. Install Python dependencies:
```bash
python setup.py
```

Or manually:
```bash
pip install -r requirements.txt
```

2. Run the extraction:
```bash
python src/python/extract.py
```

## Directory Structure

```
src/python/
├── extract.py           # Main extraction script (equivalent to extract.ts)
├── find_screenshots.py  # Screenshot discovery (equivalent to find-screenshots.ts)
└── analyze_image.py     # Image analysis using Qwen model (equivalent to analyze-image.ts)
```

## Dependencies

- `transformers`: Hugging Face Transformers library
- `torch`: PyTorch for model inference
- `Pillow`: Image processing
- `accelerate`: Model loading optimization

## Usage

The Python implementation maintains the same functionality as the TypeScript version:

1. Scans `input/screenshots/` for image files
2. Analyzes the first image using Qwen2.5-VL-7B-Instruct
3. Saves analysis to `output/analyze-image.text`

## Benefits of Python Migration

1. **Local Processing**: No API token required (model runs locally)
2. **Cost Effective**: No API usage costs
3. **Privacy**: Images processed locally
4. **Customization**: Direct access to model parameters
5. **Offline Capability**: Works without internet connection
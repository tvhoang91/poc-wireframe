from transformers import pipeline
from PIL import Image
import os
from typing import Dict, Any


def analyze_ui_from_image(image_path: str) -> str:
    """
    Analyze UI screenshot using Qwen2.5-VL-7B-Instruct model
    """
    # Initialize the pipeline
    pipe = pipeline("image-text-to-text", model="Qwen/Qwen2.5-VL-7B-Instruct")
    
    # Load the image
    image = Image.open(image_path)
    
    # Define the comprehensive prompt for UI analysis
    comprehensive_prompt = """Analyze this application UI screenshot and provide:
1. Overall screen description and purpose
2. List of UI components (buttons, forms, navigation, etc.)
3. Text content visible in the interface
4. Layout structure and organization
5. Any interactive elements or features identified
6. Screen type/category (dashboard, form, settings, etc.)

IMPORTANT GUIDELINES:
- SKIP platform navigation menus (WordPress admin sidebar, Shopify navigation, etc.)
- IGNORE standard platform headers and footers
- FOCUS ONLY on the main content area and application-specific UI elements
- DO NOT include generic platform layout elements like admin menus, top bars, or standard CMS navigation
- Concentrate on the actual application features and custom content being built

Format the response as structured information for extracting application wireframe data."""
    
    # Prepare messages in the format expected by the model
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": comprehensive_prompt}
            ]
        }
    ]
    
    try:
        # Run the analysis
        result = pipe(messages)
        
        # Extract the generated text from the result
        if isinstance(result, list) and len(result) > 0:
            # Handle different response formats
            if isinstance(result[0], dict):
                return result[0].get('generated_text', str(result[0]))
            else:
                return str(result[0])
        else:
            return str(result)
            
    except Exception as e:
        print(f"Error analyzing image: {e}")
        raise e
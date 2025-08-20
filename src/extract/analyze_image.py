import os
import base64
from huggingface_hub import InferenceClient
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def analyze_ui_from_image(image_path: str) -> str:
    """
    Analyze UI screenshot using Qwen2.5-VL-7B-Instruct model via Inference Client
    """
    # Initialize the Inference Client
    client = InferenceClient(
        provider="hyperbolic",
        api_key=os.environ["HUGGINGFACE_API_TOKEN"],
    )
    
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
    
    try:
        # Read and encode image as base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine image mime type
        image_ext = os.path.splitext(image_path)[1].lower()
        mime_type = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg', 
            '.jpeg': 'image/jpeg'
        }.get(image_ext, 'image/png')
        
        # Prepare the completion request
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": comprehensive_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
        )
        
        # Extract the response text
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        raise e
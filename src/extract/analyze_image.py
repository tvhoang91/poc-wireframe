import os
import base64
import json
from pathlib import Path
from huggingface_hub import InferenceClient
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

def analyze_feature_from_folder(folder_path: str, feature_name: str = None) -> Dict[str, Any]:
    """
    Analyze all screenshots in a folder as a cohesive feature using single chat completion
    
    Args:
        folder_path: Path to folder containing screenshot images
        feature_name: Optional name for the feature being analyzed
        
    Returns:
        Dict containing comprehensive feature analysis with screens, workflow, and recommendations
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    # Find all image files in the folder
    image_extensions = {'.png', '.jpg', '.jpeg'}
    image_files = [
        f for f in folder.iterdir() 
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    if not image_files:
        raise ValueError(f"No image files found in {folder_path}")
    
    # Sort by filename for consistent ordering
    image_files.sort(key=lambda x: x.name)
    
    # Initialize the Inference Client
    client = InferenceClient(
        provider="hyperbolic",
        api_key=os.environ["HUGGINGFACE_API_TOKEN"],
    )
    
    # Prepare comprehensive feature analysis prompt
    if not feature_name:
        feature_name = folder.name.replace('_', ' ').replace('-', ' ').title()
    
    feature_analysis_prompt = f"""Analyze these {len(image_files)} screenshots as a cohesive feature called "{feature_name}". 

COMPREHENSIVE FEATURE ANALYSIS REQUIREMENTS:

1. **Feature Overview**:
   - Identify the main feature/functionality shown across all screenshots
   - Describe the overall purpose and business value
   - Summarize how users would interact with this feature

2. **Screen Analysis & Grouping**:
   - Group screenshots by distinct screens/states (some images may show the same screen)
   - For each unique screen, provide:
     * Screen name/identifier
     * Screen type (dashboard, form, listing, detail, etc.)
     * Which image files show this screen
     * Layout description and key UI components
     * Interactive elements and their purposes

3. **User Workflow & Navigation**:
   - Map the user journey through the feature
   - Identify navigation patterns between screens
   - Document the step-by-step process users follow
   - Note any conditional flows or decision points

4. **MVP Feature Assessment**:
   - Identify core/essential screens for MVP
   - List must-have vs. nice-to-have functionality
   - Suggest simplified workflow for initial implementation

5. **Wireframe Recommendations**:
   - Propose wireframe structure for each core screen
   - Suggest responsive layout considerations
   - Recommend component hierarchy and information architecture

IMPORTANT GUIDELINES:
- SKIP platform-specific navigation (WordPress admin sidebar, etc.)
- FOCUS on the actual feature content and functionality
- IGNORE generic CMS/platform chrome and headers
- Provide structured, actionable insights for development

Return response as a well-structured analysis that can be easily converted to JSON format."""

    try:
        # Prepare message content with all images
        message_content = [{"type": "text", "text": feature_analysis_prompt}]
        
        # Add all images to the single chat completion
        for image_file in image_files:
            with open(image_file, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Determine mime type
            mime_type = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg', 
                '.jpeg': 'image/jpeg'
            }.get(image_file.suffix.lower(), 'image/png')
            
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_data}"
                }
            })
        
        # Single chat completion with all images
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[{
                "role": "user", 
                "content": message_content
            }],
        )
        
        analysis_text = completion.choices[0].message.content
        
        # Structure the response
        result = {
            "feature_name": feature_name,
            "folder_path": str(folder_path),
            "images_analyzed": [f.name for f in image_files],
            "analysis_text": analysis_text,
            "metadata": {
                "total_images": len(image_files),
                "image_files": [str(f) for f in image_files]
            }
        }
        
        return result
        
    except Exception as e:
        print(f"Error analyzing feature from folder: {e}")
        raise e



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
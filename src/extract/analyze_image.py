import os
import base64
import json
from pathlib import Path
from huggingface_hub import InferenceClient
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


def analyze_screen_from_folder(folder_path: str, screen_name: str = None) -> Dict[str, Any]:
    """
    Analyze all screenshots of the same screen showing different states/interactions
    
    Args:
        folder_path: Path to folder containing screenshots of the same screen
        screen_name: Optional name for the screen being analyzed
        
    Returns:
        Dict containing screen analysis with base state, interactions, and UI components
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
        provider="novita",
        api_key=os.environ["HUGGINGFACE_API_TOKEN"],
    )
    
    # Prepare screen state analysis prompt
    if not screen_name:
        screen_name = folder.name.replace('_', ' ').replace('-', ' ').title()

    system_analysis_prompt = """You are a UI analysis assistant."""
    
    screen_analysis_prompt = f"""Analyze these {len(image_files)} screenshots showing the SAME SCREEN "{screen_name}" in different states and interactions. And suggest a wireframe follow good UX/UI design for this screen.

IMPORTANT: All these screenshots are of the SAME SCREEN showing different UI states, interactions, and overlays.

SCREEN STATE ANALYSIS REQUIREMENTS:

1. **Base Screen Identification**:
   - Identify the core/base screen layout that appears across all screenshots
   - Describe the main screen purpose and functionality
   - List the persistent UI elements that remain constant

2. **Screen Wireframe Structure**:
   - Describe the screen wireframe layout
   - List of interactive elements and their purpose

3. **New Wireframe Insights**:
   - Suggest a new text wireframe for this screen
   - The wireframe should follow good UX/UI design
   - The wireframe will be built using React, Shadcn UI, Tailwind CSS

ANALYSIS GUIDELINES:
- FOCUS on the main content area, ignore platform chrome
- COMPARE states to understand interaction flows
- PROVIDE good UX/UI design insights for UI development

Return a comprehensive analysis explaining how this screen works and suggest a wireframe for this screen."""

    try:
        # Prepare message content with all images
        message_content = [{"type": "text", "text": screen_analysis_prompt}]
        
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
        
        # Single chat completion with all screen state images
        completion = client.chat.completions.create(
            model="zai-org/GLM-4.5V",
            # model="Qwen/Qwen2.5-VL-7B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": system_analysis_prompt
                },
                {
                    "role": "user", 
                    "content": message_content
                }
            ],
        )
        
        analysis_text = completion.choices[0].message.content
        
        # Structure the response
        result = {
            "screen_name": screen_name,
            "folder_path": str(folder_path),
            "images_analyzed": [f.name for f in image_files],
            "analysis_text": analysis_text,
            "metadata": {
                "total_images": len(image_files),
                "image_files": [str(f) for f in image_files],
                "analysis_type": "screen_state_analysis"
            }
        }
        
        return result
        
    except Exception as e:
        print(f"Error analyzing screen from folder: {e}")
        raise e



import os
import base64
import json
from pathlib import Path
from openai import OpenAI
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


def analyze_screen_from_folder(folder_path: str, screen_name: str = None) -> Dict[str, Any]:
    """
    Analyze all screenshots of the same screen showing different states/interactions using OpenAI GPT-4 Vision
    
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
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Prepare screen state analysis prompt
    if not screen_name:
        screen_name = folder.name.replace('_', ' ').replace('-', ' ').title()

    system_analysis_prompt = """You are a UI/UX analysis expert specializing in wireframe creation and interface design."""
    
    screen_analysis_prompt = f"""Analyze these {len(image_files)} screenshots showing the SAME SCREEN "{screen_name}" in different states and interactions. Provide a comprehensive analysis and suggest an improved wireframe following modern UX/UI design principles.

IMPORTANT: All these screenshots are of the SAME SCREEN showing different UI states, interactions, and overlays.

SCREEN STATE ANALYSIS REQUIREMENTS:

1. **Base Screen Identification**:
   - Identify the core/base screen layout that appears across all screenshots
   - Describe the main screen purpose and functionality

2. **Interaction Flow Analysis**:
   - Document different UI states shown in the screenshots
   - Identify interactive elements (buttons, forms, dropdowns, modals)
   - Map user interaction patterns and workflows

3. **Current UX/UI Assessment**:
   - Identify strengths in the current design
   - Point out potential usability issues or improvements
   - Assess information architecture and visual hierarchy

4. **Modern Wireframe Recommendation**:
   - Suggest which section of this screen could be improved
   - Apply modern UX/UI design principles (accessibility, mobile-first, clear hierarchy)
   - **IMPORTANT**: Provide an ASCII-art style representation of a user interface layout showing the recommended wireframe structure for each improved section
   - **IMPORTANT**: Provide a React, Shadcn UI, Tailwind CSS code for the recommended wireframe structure for each improved section

ANALYSIS GUIDELINES:
- FOCUS on content and functionality, minimize platform-specific chrome discussion
- COMPARE different states to understand complete user flows
- PROVIDE actionable insights for modern web application development
- CONSIDER accessibility and responsive design principles
- SUGGEST specific improvements backed by UX best practices

Return a detailed analysis with clear sections for each requirement above."""

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
                    "url": f"data:{mime_type};base64,{image_data}",
                    "detail": "high"  # Use high detail for better analysis
                }
            })
        
        # Single chat completion with all screen state images using GPT-4 Vision
        completion = client.chat.completions.create(
            model="gpt-4o",  # GPT-4 with vision capabilities
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
            max_tokens=16000,  # Increased for comprehensive analysis
            temperature=0.3   # Lower temperature for more consistent analysis
        )
        
        analysis_text = completion.choices[0].message.content
        
        # Structure the response
        result = {
            "screen_name": screen_name,
            "folder_path": str(folder_path),
            "images_analyzed": [f.name for f in image_files],
            "analysis_text": analysis_text,
            "model_used": "gpt-4o",
            "metadata": {
                "total_images": len(image_files),
                "image_files": [str(f) for f in image_files],
                "analysis_type": "screen_state_analysis_openai",
                "tokens_used": completion.usage.total_tokens if completion.usage else None,
                "cost_estimate_usd": _calculate_cost_estimate(completion.usage) if completion.usage else None
            }
        }
        
        return result
        
    except Exception as e:
        print(f"Error analyzing screen from folder with OpenAI: {e}")
        raise e


def _calculate_cost_estimate(usage) -> float:
    """
    Calculate estimated cost for GPT-4o API usage
    Prices as of 2024 (may need updating)
    """
    if not usage:
        return 0.0
    
    # GPT-4o pricing (approximate, check OpenAI pricing for current rates)
    input_cost_per_1k = 0.005   # $0.005 per 1k input tokens
    output_cost_per_1k = 0.015  # $0.015 per 1k output tokens
    
    input_cost = (usage.prompt_tokens / 1000) * input_cost_per_1k
    output_cost = (usage.completion_tokens / 1000) * output_cost_per_1k
    
    return round(input_cost + output_cost, 6)



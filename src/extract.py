import os
import json
from pathlib import Path
from datetime import datetime
from extract.find_screenshots import find_screenshots
from extract.analyze_image_prod import analyze_screen_from_folder

def main():
    """
    Main extraction function that processes screenshots and analyzes UI
    """
    print("Begin Extraction!")
    
    # Define screenshots directory
    review_management_screenshots_dir = Path.cwd() / "input" / "screen-review-management"
    
    try:
        print("\n--- Analyzing Screen with Multi-Image Approach ---")
        
        screen_analysis = analyze_screen_from_folder(str(review_management_screenshots_dir), "Review Management")
        
        print("\n=== SCREEN ANALYSIS COMPLETE ===")
        print(f"Screen: {screen_analysis['screen_name']}")
        print(f"Images Analyzed: {screen_analysis['metadata']['total_images']}")
        print("\n--- Analysis Preview ---")
        print(screen_analysis['analysis_text'][:200] + "..." if len(screen_analysis['analysis_text']) > 200 else screen_analysis['analysis_text'])
        
        # Save comprehensive screen analysis
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Save as JSON for structured data
        json_output_file = output_dir / "screen-analysis-prod.json"
        with open(json_output_file, 'w') as f:
            json.dump(screen_analysis, f, indent=2)
        print(f"\nScreen analysis saved to: {json_output_file}")
        
        # Also save readable text version
        text_output_file = output_dir / "screen-analysis-prod.text"
        text_content = (
            f"Screen Analysis: {screen_analysis['screen_name']}\n"
            f"Generated at: {datetime.now().isoformat()}\n"
            f"Images analyzed: {', '.join(screen_analysis['images_analyzed'])}\n\n"
            f"{screen_analysis['analysis_text']}"
        )
        text_output_file.write_text(text_content)
        print(f"Readable analysis saved to: {text_output_file}")
        
    except Exception as error:
        print(f"Extract Error")


if __name__ == "__main__":
    main()


"""
This script will extract the UI content from the screenshots of application.
The extracted content will be saved in output/extraction.json.

The extracted content need the following information:
- List of screens, with short description, UI layout
- List of features, with short description, MVP flag, which screen it belongs to

The extraction process will be as follows:
1. Read image files in input/screenshots
For each image:
2.1. call image_to_text to tell the image content in term of application screen, layout, components
Then
3. group images by screen
For each screen:
4. summarize the extracted data from all images of a screen; UI layout, short description
5. save the extracted data in output/screen/[screen_name].json
"""
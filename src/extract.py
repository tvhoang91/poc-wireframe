import os
from pathlib import Path
from datetime import datetime
from extract.find_screenshots import find_screenshots
from extract.analyze_image import analyze_ui_from_image

def main():
    """
    Main extraction function that processes screenshots and analyzes UI
    """
    print("Begin Extraction!")
    
    # Define screenshots directory
    screenshots_dir = Path.cwd() / "input" / "screenshots"
    
    try:
        # Find all screenshot files
        file_info = find_screenshots(str(screenshots_dir))
        
        print(f"Files in input/screenshots: {{\n"
              f"  firstImage: {file_info[0]['name'] if file_info else 'none'},\n"
              f"  imageCount: {len(file_info)}\n}}")
        
        if file_info:
            print("\n--- Analyzing first image with Qwen2.5-VL-7B-Instruct ---")
            first_image = file_info[0]
            print(f"Analyzing: {first_image['name']}")
            
            # Single comprehensive UI analysis call
            analysis = analyze_ui_from_image(first_image['path'])
            print("Comprehensive UI Analysis:", analysis)
            
            # Save analysis to output file
            output_dir = Path.cwd() / "output"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / "analyze-image.text"
            analysis_content = (
                f"Image Analysis for: {first_image['name']}\n"
                f"Analyzed at: {datetime.now().isoformat()}\n\n"
                f"{analysis}"
            )
            
            output_file.write_text(analysis_content)
            print(f"\nAnalysis saved to: {output_file}")
            
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
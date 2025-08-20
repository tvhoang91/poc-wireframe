import os
import json
from pathlib import Path
from datetime import datetime
from extract.find_screenshots import find_screenshots
from extract.analyze_image import analyze_ui_from_image, analyze_feature_from_folder

def main():
    """
    Main extraction function that processes screenshots and analyzes UI
    """
    print("Begin Extraction!")
    
    # Define screenshots directory
    review_management_screenshots_dir = Path.cwd() / "input" / "feature-review-management"
    
    try:
        print("\n--- Analyzing Feature with Multi-Image Approach ---")
        
        feature_analysis = analyze_feature_from_folder(str(review_management_screenshots_dir), "Review Management")
        
        print("\n=== FEATURE ANALYSIS COMPLETE ===")
        print(f"Feature: {feature_analysis['feature_name']}")
        print(f"Images Analyzed: {feature_analysis['metadata']['total_images']}")
        print("\n--- Analysis Preview ---")
        print(feature_analysis['analysis_text'][:200] + "..." if len(feature_analysis['analysis_text']) > 200 else feature_analysis['analysis_text'])
        
        # Save comprehensive feature analysis
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Save as JSON for structured data
        json_output_file = output_dir / "feature-analysis.json"
        with open(json_output_file, 'w') as f:
            json.dump(feature_analysis, f, indent=2)
        print(f"\nFeature analysis saved to: {json_output_file}")
        
        # Also save readable text version
        text_output_file = output_dir / "feature-analysis.text"
        text_content = (
            f"Feature Analysis: {feature_analysis['feature_name']}\n"
            f"Generated at: {datetime.now().isoformat()}\n"
            f"Images analyzed: {', '.join(feature_analysis['images_analyzed'])}\n\n"
            f"{feature_analysis['analysis_text']}"
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
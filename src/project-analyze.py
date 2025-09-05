import os
import json
from pathlib import Path
from datetime import datetime
from extract.find_screenshots import find_screenshots
from extract.analyze_image_prod import analyze_screen_from_folder

def main():
    print("Begin Analyze!")
    
    input_dir = Path.cwd() / "input" / "project-analyze"
    output_dir = Path.cwd() / "output" / "project-analyze"
    
    try:
        print(f"Input directory: {input_dir}")
        
        
    except Exception as error:
        print(f"Analyze Error")


if __name__ == "__main__":
    main()


"""
This script will need to output a wireframe for a webapp project.
With the input are screenshots of other similar application.
"""
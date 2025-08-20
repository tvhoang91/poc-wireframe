import os
from pathlib import Path
from typing import List, Dict
import time


def find_screenshots(screenshots_dir: str) -> List[Dict]:
    """
    Find all image files (png, jpg, jpeg) in the screenshots directory
    and return their metadata.
    """
    screenshots_path = Path(screenshots_dir)
    
    if not screenshots_path.exists():
        return []
    
    # Supported image extensions
    image_extensions = {'.png', '.jpg', '.jpeg'}
    
    files = []
    for file_path in screenshots_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            stat = file_path.stat()
            
            file_info = {
                'name': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'size_in_mb': f"{stat.st_size / (1024 * 1024):.2f}",
                'created': time.ctime(stat.st_ctime),
                'modified': time.ctime(stat.st_mtime),
                'is_file': True
            }
            files.append(file_info)
    
    return files
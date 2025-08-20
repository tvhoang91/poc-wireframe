#!/usr/bin/env python3
"""
Setup script for the Python version of poc-wireframe
"""

import subprocess
import sys
from pathlib import Path


def install_requirements():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully!")


def setup_directories():
    """Create necessary directories"""
    input_dir = Path("input/screenshots")
    output_dir = Path("output")
    
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Created directories: {input_dir}, {output_dir}")


def main():
    print("Setting up Python version of poc-wireframe...")
    
    # Install dependencies
    install_requirements()
    
    # Setup directories
    setup_directories()
    
    print("\nSetup complete!")
    print("Usage:")
    print("  python src/python/extract.py")


if __name__ == "__main__":
    main()
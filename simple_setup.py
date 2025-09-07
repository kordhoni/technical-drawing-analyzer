#!/usr/bin/env python3
"""
Simple Setup Script for Technical Drawing Analyzer
Krijon strukturën bazë të projektit
"""

import os
import subprocess
import sys

def create_basic_structure():
    """Krijon strukturën bazë të projektit"""
    
    print("🚀 Creating Technical Drawing Analyzer project structure...")
    
    # Krijoni strukturën e dosjes
    os.makedirs('modules', exist_ok=True)
    print("✅ Created modules/ directory")
    
    # Krijoni __init__.py
    with open('modules/__init__.py', 'w', encoding='utf-8') as f:
        f.write("# Empty file to make modules a package\n")
    print("✅ Created modules/__init__.py")
    
    # Krijoni requirements.txt
    requirements = """# Core dependencies
opencv-python>=4.5.0
Pillow>=8.0.0
numpy>=1.20.0
pandas>=1.3.0
openpyxl>=3.0.0

# PDF support
PyMuPDF>=1.20.0

# OCR support
pytesseract>=0.3.8
easyocr>=1.6.0

# PDF generation
reportlab>=3.6.0

# CAD support (optional)
ezdxf>=0.17.0

# Build tools
pyinstaller>=5.0.0
"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    print("✅ Created requirements.txt")
    
    # Krijoni install.bat
    install_bat = """@echo off
echo Technical Drawing Analyzer - Installation Script
echo ================================================

echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Creating virtual environment...
python -m venv technical_analyzer_env

echo.
echo Activating virtual environment...
call technical_analyzer_env\\Scripts\\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Installation completed successfully!
echo To run: python main.py
pause
"""
    
    with open('install.bat', 'w', encoding='utf-8') as f:
        f.write(install_bat)
    print("✅ Created install.bat")
    
    # Krijoni run.bat
    run_bat = """@echo off
echo Starting Technical Drawing Analyzer...

if exist "technical_analyzer_env\\Scripts\\activate.bat" (
    call technical_analyzer_env\\Scripts\\activate.bat
)

python main.py
pause
"""
    
    with open('run.bat', 'w', encoding='utf-8') as f:
        f.write(run_bat)
    print("✅ Created run.bat")
    
    # Krijoni një main.py bazë
    main_py_basic = """#!/usr/bin/env python3
\"\"\"
Technical Drawing Analyzer
Basic version - Add modules manually
\"\"\"

print("Technical Drawing Analyzer v1.0")
print("=" * 40)
print("Setup completed successfully!")
print("")
print("Next steps:")
print("1. Add the module files manually:")
print("   - modules/document_processor.py")
print("   - modules/symbol_recognizer.py") 
print("   - modules/output_generator.py")
print("   - modules/database_manager.py")
print("")
print("2. Copy the full main.py content from Claude")
print("3. Run: python main.py")
print("")
print("For now, this is just a placeholder.")

# Basic test
try:
    import tkinter as tk
    print("✅ Tkinter is available")
except ImportError:
    print("❌ Tkinter not found")

try:
    import cv2
    print("✅ OpenCV is available")
except ImportError:
    print("❌ OpenCV not installed - run install.bat first")

try:
    import numpy
    print("✅ NumPy is available")
except ImportError:
    print("❌ NumPy not installed - run install.bat first")

try:
    import PIL
    print("✅ Pillow is available")
except ImportError:
    print("❌ Pillow not installed - run install.bat first")

try:
    import pandas
    print("✅ Pandas is available")
except ImportError:
    print("❌ Pandas not installed - run install.bat first")

input("\\nPress Enter to exit...")
"""
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_py_basic)
    print("✅ Created main.py (basic version)")
    
    print("\n🎉 Basic structure created successfully!")
    print("\n📋 What you have now:")
    print("   ✅ modules/ directory")
    print("   ✅ requirements.txt")
    print("   ✅ install.bat")
    print("   ✅ run.bat") 
    print("   ✅ main.py (basic version)")
    
    print("\n📝 Next steps:")
    print("1. Run: install.bat")
    print("2. Add module files manually from Claude artifacts")
    print("3. Replace main.py with full version from Claude")
    print("4. Test: python main.py")

def main():
    """Main function"""
    print("Technical Drawing Analyzer - Simple Setup")
    print("=" * 50)
    
    create_basic_structure()
    
    print("\n🤔 Ready to install dependencies?")
    response = input("Run install.bat now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Running installation...")
        if os.name == 'nt':  # Windows
            os.system('install.bat')
        else:
            print("Please run: chmod +x install.sh && ./install.sh")
    else:
        print("\nRun 'install.bat' when ready!")

if __name__ == "__main__":
    main()

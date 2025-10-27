#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main application entry point for Excel File Processor.

This application provides a graphical interface to:
1. Upload a stores CSV file
2. Upload an Excel file
3. Process the files to generate store-specific Excel and TXT files
"""

import os
import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import main application class
from app.ui_pyside6.main_window import ExcelProcessorApp

def main():
    """Main function that initializes and runs the application."""
    # Make sure we're in the right directory for file operations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create output directory if it doesn't exist
    output_dir = Path('output')
    if not output_dir.exists():
        output_dir.mkdir()
        logger.info(f"Created output directory: {output_dir}")
    
    # Create source directory if it doesn't exist
    source_dir = Path('source')
    if not source_dir.exists():
        source_dir.mkdir()
        logger.info(f"Created source directory: {source_dir}")
    
    # Create stores directory if it doesn't exist
    stores_dir = Path('stores')
    if not stores_dir.exists():
        stores_dir.mkdir()
        logger.info(f"Created stores directory: {stores_dir}")
    
    # Initialize the PySide6 application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    
    # Set application icon
    icon_path = Path("images/logo.png")
    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon)
    
    # Create and show the main window
    window = ExcelProcessorApp()
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
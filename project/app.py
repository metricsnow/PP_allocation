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
from src.ui.main_window import ExcelProcessorApp

def main():
    """Main function that initializes and runs the application."""
    # Make sure we're in the right directory for file operations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create data directories if they don't exist
    for dir_name in ['data/output', 'data/source', 'data/stores']:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            logger.info(f"Created directory: {dir_path}")
    
    # Initialize the PySide6 application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    
    # Set application icon
    icon_path = Path("resources/images/logo.png")
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
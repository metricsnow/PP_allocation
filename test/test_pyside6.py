#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script to verify the PySide6 implementation.

This script imports and instantiates the main ExcelProcessorApp without running the full application.
"""

import sys
import os
import logging
from pathlib import Path

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_import():
    """Test importing the PySide6 implementation"""
    try:
        from PySide6.QtWidgets import QApplication
        logger.info("Successfully imported PySide6")
        return True
    except ImportError as e:
        logger.error(f"Failed to import PySide6: {e}")
        return False

def test_app_creation():
    """Test creating the main application"""
    try:
        from app.ui_pyside6.main_window import ExcelProcessorApp
        from PySide6.QtWidgets import QApplication
        
        # Create QApplication instance
        app = QApplication([])
        
        # Create main window
        window = ExcelProcessorApp()
        
        logger.info("Successfully created ExcelProcessorApp instance")
        return True
    except Exception as e:
        logger.error(f"Failed to create ExcelProcessorApp: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    import_success = test_import()
    app_success = False
    
    if import_success:
        app_success = test_app_creation()
    
    # Print results
    print("\nTest Results:")
    print(f"PySide6 Import Test: {'PASSED' if import_success else 'FAILED'}")
    print(f"App Creation Test: {'PASSED' if app_success else 'FAILED'}")
    
    if import_success and app_success:
        print("\nAll tests passed! PySide6 implementation is working correctly.")
    else:
        print("\nSome tests failed. Please check the log for details.") 
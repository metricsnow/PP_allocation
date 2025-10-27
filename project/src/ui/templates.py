#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Templates module for Excel File Processor (PySide6 version).

This module provides functionality to show example templates for:
1. Stores CSV file
2. Excel file
"""

import os
import tempfile
import pandas as pd
import webbrowser
import logging
from pathlib import Path
from PySide6.QtWidgets import QMessageBox

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def show_stores_template(app, parent=None):
    """
    Show an example template for the stores CSV file.
    
    Args:
        app: The application instance, used to access log method
        parent: The parent widget for displaying message boxes
    """
    # Path to the template file
    template_path = Path("template_files/stores.csv")
    
    if template_path.exists():
        # If template exists, open it directly
        webbrowser.open('file://' + str(template_path.absolute()))
        app.log(f"Opened stores CSV template: {template_path}")
    else:
        # Display error message if template doesn't exist
        QMessageBox.warning(
            parent,
            "Template Not Found",
            f"The template file {template_path} could not be found."
        )
        logger.error(f"Template file not found: {template_path}")

def show_excel_template(app, parent=None):
    """
    Show an example template for the Excel file.
    
    Args:
        app: The application instance, used to access log method
        parent: The parent widget for displaying message boxes
    """
    # Path to the template file
    template_path = Path("template_files/PRE ALLOCATION PP OUTLET PRODUCTION.xlsx")
    
    if template_path.exists():
        # If template exists, open it directly
        webbrowser.open('file://' + str(template_path.absolute()))
        app.log(f"Opened Excel template: {template_path}")
    else:
        # Display error message if template doesn't exist
        QMessageBox.warning(
            parent,
            "Template Not Found",
            f"The template file {template_path} could not be found."
        )
        logger.error(f"Template file not found: {template_path}") 
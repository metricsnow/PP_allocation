#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Templates module for Excel File Processor.

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
from tkinter import messagebox

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def show_stores_template(app):
    """
    Show an example template for the stores CSV file.
    
    Args:
        app: The application instance, used to access log method
    """
    # Path to the template file in the source directory
    template_path = Path("source/stores_template.csv")
    
    if template_path.exists():
        # If template exists, open it directly
        webbrowser.open('file://' + str(template_path.absolute()))
        app.log(f"Opened stores CSV template: {template_path}")
    else:
        # Create a temporary template file
        try:
            # Create example data
            example_data = pd.DataFrame({
                'store_name': [
                    'Store A', 
                    'Store B', 
                    'Store C',
                    'Store D/Branch 1',
                    'Store D/Branch 2'
                ]
            })
            
            # Create a temporary file to hold the example
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                example_data.to_csv(temp_file.name, index=False)
                
                # Open the temporary file
                webbrowser.open('file://' + temp_file.name)
                app.log(f"Created and opened stores CSV template: {temp_file.name}")
                
                # Display a message box with an explanation
                messagebox.showinfo(
                    "Stores CSV Template",
                    "This is an example template for the stores CSV file.\n\n"
                    "The file should have a single column with store names.\n"
                    "No header is required, but if present, it should be 'store_name'.\n\n"
                    "Each row should contain a unique store name."
                )
        except Exception as e:
            messagebox.showerror("Template Error", f"Error creating template: {e}")
            logger.error(f"Error creating stores template: {e}")

def show_excel_template(app):
    """
    Show an example template for the Excel file.
    
    Args:
        app: The application instance, used to access log method
    """
    # Path to the template file in the source directory
    template_path = Path("source/excel_template.xlsx")
    
    if template_path.exists():
        # If template exists, open it directly
        webbrowser.open('file://' + str(template_path.absolute()))
        app.log(f"Opened Excel template: {template_path}")
    else:
        # Create a temporary template file
        try:
            # Create example data with sample columns
            example_data = pd.DataFrame({
                'EANCode': ['1234567890123', '2345678901234', '3456789012345', '4567890123456'],
                'SEASON': ['Spring', 'Summer', 'Fall', 'Winter'],
                'Store A': [5, 10, 0, 3],
                'Store B': [3, 6, 8, 4],
                'Store C': [0, 2, 4, 1],
                'Store D/Branch 1': [7, 0, 2, 5],
                'Store D/Branch 2': [1, 3, 5, 0]
            })
            
            # Create a temporary file to hold the example
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                # Create Excel with sheet named "PRE ALLOCATION"
                with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
                    example_data.to_excel(writer, sheet_name='PRE ALLOCATION', index=False)
                
                # Open the temporary file
                webbrowser.open('file://' + temp_file.name)
                app.log(f"Created and opened Excel template: {temp_file.name}")
                
                # Display a message box with an explanation
                messagebox.showinfo(
                    "Excel Template",
                    "This is an example template for the Excel file.\n\n"
                    "The file should have:\n"
                    "1. A sheet named 'PRE ALLOCATION'\n"
                    "2. Columns for 'EANCode' and 'SEASON'\n"
                    "3. Additional columns for each store with quantities\n\n"
                    "The program will create separate files for each store with:\n"
                    "- A sheet for all seasons combined\n"
                    "- Individual sheets for each season\n"
                    "- TXT files with EANCode repeated based on quantities"
                )
        except Exception as e:
            messagebox.showerror("Template Error", f"Error creating template: {e}")
            logger.error(f"Error creating Excel template: {e}") 
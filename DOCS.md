# Project Documentation

## Overview
This project provides tools for working with Excel (XLSX) files in Python. It uses the openpyxl library to handle Excel file operations.

## Architecture
The project is structured around a single Python script that handles Excel file operations:

- `worker.py`: Main script for loading, processing, and manipulating Excel files

## Dependencies
- Python 3.x
- openpyxl: For working with Excel files
- pandas (optional): For additional data manipulation capabilities

## Key Components

### Excel File Operations
The core functionality for loading and working with Excel files is implemented in the main worker script. Key functionality includes:
- Loading Excel files
- Reading data from specific worksheets and ranges
- Processing data from Excel

### Error Handling
The application includes robust error handling for:
- Missing files
- Invalid file formats
- Data validation errors

## Installation and Setup
1. Create a virtual environment: `python -m venv venv_plein`
2. Activate the virtual environment: `venv_plein\Scripts\activate`
3. Install required packages: `pip install openpyxl pandas`

## Usage Examples
Specific usage examples will be added once the implementation is complete. 
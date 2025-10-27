#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File processor module for handling Excel and CSV file operations.

This module provides functionality to:
1. Load and read Excel (XLSX) files
2. Read stores from a CSV file
3. Process each store to create store-specific files
"""

import os
import logging
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Union
import pandas as pd

from app.processors.store_processor import process_store

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self):
        """Initialize the file processor."""
        pass
        
    def load_xlsx_file(self, file_path: Union[str, Path], sheet_name: str = "PRE ALLOCATION") -> Optional[pd.DataFrame]:
        """
        Load an Excel (xlsx) file and return its content as a pandas DataFrame.
        
        Args:
            file_path (Union[str, Path]): Path to the xlsx file
            sheet_name (str): Name of the sheet to load (default: "PRE ALLOCATION")
            
        Returns:
            Optional[pd.DataFrame]: DataFrame containing the Excel data or None if loading failed
        """
        try:
            logger.info(f"Loading Excel file: {file_path}")
            
            # Try to load the specified sheet
            try:
                logger.info(f"Loading '{sheet_name}' sheet from Excel file")
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Check if the sheet loaded successfully
                if df is not None and not df.empty:
                    logger.info(f"Successfully loaded '{sheet_name}' sheet with {len(df)} rows and {len(df.columns)} columns")
                    return df
                else:
                    logger.warning(f"The '{sheet_name}' sheet was empty or could not be loaded")
            except Exception as e:
                logger.warning(f"Error loading '{sheet_name}' sheet: {e}")
                
                # Check if Excel file has a sheet named without spaces
                try:
                    sheet_name_no_spaces = sheet_name.replace(" ", "_")
                    logger.info(f"Trying to load '{sheet_name_no_spaces}' sheet (without spaces)")
                    df = pd.read_excel(file_path, sheet_name=sheet_name_no_spaces)
                    if df is not None and not df.empty:
                        return df
                except Exception:
                    pass
                    
                # Get all sheet names to log them for debugging
                xls = pd.ExcelFile(file_path)
                sheet_names = xls.sheet_names
                logger.info(f"Available sheets in the Excel file: {sheet_names}")
                
                # If we can't load the specific sheet, try the first sheet
                logger.info("Trying to load the first sheet as fallback")
                df = pd.read_excel(file_path)
            
            logger.info(f"Successfully loaded Excel file with {len(df)} rows and {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"Excel file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            return None
    
    def read_stores_csv(self, file_path: Union[str, Path]) -> Optional[pd.DataFrame]:
        """
        Read a CSV file containing store information.
        
        Args:
            file_path (Union[str, Path]): Path to the stores CSV file
            
        Returns:
            Optional[pd.DataFrame]: DataFrame containing store information or None if loading failed
        """
        try:
            logger.info(f"Loading stores from CSV: {file_path}")
            
            # The stores file appears to have no headers, just store names
            # We'll read it as a single column dataframe
            stores_df = pd.read_csv(file_path, header=None, names=['store_name'])
            
            # Remove any blank rows
            stores_df = stores_df[stores_df['store_name'].notna()]
            stores_df = stores_df[stores_df['store_name'].str.strip() != '']
            
            # Drop duplicates
            unique_stores = stores_df.drop_duplicates()
            logger.info(f"Found {len(unique_stores)} unique stores")
            
            return unique_stores
        except FileNotFoundError:
            logger.error(f"Stores CSV file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading stores CSV: {e}")
            return None
    
    def find_store_column(self, df: pd.DataFrame, store_name: str) -> Optional[str]:
        """
        Find the column in the DataFrame that matches the store name.
        
        Args:
            df (pd.DataFrame): DataFrame to search in
            store_name (str): Store name to find
            
        Returns:
            Optional[str]: Matching column name or None if not found
        """
        # Try exact match first
        for col in df.columns:
            if col == store_name:
                return col
        
        # If exact match not found, try to find a column containing the store name
        for col in df.columns:
            if isinstance(col, str) and store_name in col:
                return col
        
        return None
    
    def process_store(self, store_name: str, xlsx_df: pd.DataFrame, output_dir: Path) -> bool:
        """
        Process a single store by finding matching column in the xlsx data,
        extracting EANCode and SEASON data for that store, and creating sheets
        for each distinct SEASON value in a new Excel file.
        
        Also creates TXT files for each store-season combination with repeated
        EANCode values based on the quantity value in the store's column.
        
        Args:
            store_name (str): Name of the store to search for
            xlsx_df (pd.DataFrame): DataFrame containing the Excel data
            output_dir (Path): Directory to save the output file
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            # Process the store using the imported function
            process_store(store_name, xlsx_df, output_dir)
            return True
        except Exception as e:
            logger.error(f"Error processing store {store_name}: {e}")
            return False
            
    def create_txt_file_with_repeated_eancodes(self, df: pd.DataFrame, ean_col: str, store_col: str, output_path: Path) -> bool:
        """
        Create a text file with repeated EANCode values based on quantity values.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            ean_col (str): Name of the EANCode column
            store_col (str): Name of the store column containing quantity values
            output_path (Path): Path to save the output text file
            
        Returns:
            bool: True if the file was created successfully, False otherwise
        """
        try:
            with open(output_path, 'w') as f:
                # For each row in the DataFrame
                for _, row in df.iterrows():
                    # Clean and format the EANCode: remove .0 suffix if present
                    eancode = str(row[ean_col]).strip()
                    if eancode.endswith('.0'):
                        eancode = eancode[:-2]
                    
                    # Try to get the quantity as an integer
                    try:
                        # Handle possible non-numeric or NaN values
                        qty = row[store_col]
                        
                        # Handle blank spaces as zero
                        if pd.isna(qty) or (isinstance(qty, str) and qty.strip() in ['', ' ', '  ']):
                            qty = 0
                        else:
                            qty = int(float(qty))
                        
                        # Write the EANCode repeated qty times
                        for _ in range(qty):
                            f.write(f"{eancode}\n")
                    except (ValueError, TypeError):
                        # If conversion fails, log a warning and continue
                        logger.warning(f"Could not convert quantity '{row[store_col]}' to integer for EANCode {eancode}")
                        continue
            
            logger.info(f"Created TXT file with repeated EANCodes: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating TXT file {output_path}: {e}")
            return False 
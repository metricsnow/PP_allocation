#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functions module for handling Excel and CSV file operations.

This module provides functionality to:
1. Load and process xlsx files from the source directory
2. Read unique stores from a CSV file in the stores directory
3. Extract important columns like EANCode and SEASON from xlsx files
4. Find common columns between xlsx files and stores.csv
"""

import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Set, Tuple
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_xlsx_file(file_path: Union[str, Path]) -> Optional[pd.DataFrame]:
    """
    Load an Excel (xlsx) file and return its content as a pandas DataFrame.
    Specifically loads the "PRE ALLOCATION" sheet.

    Args:
        file_path (Union[str, Path]): Path to the xlsx file

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the Excel data or None if loading failed
    """
    try:
        logger.info(f"Loading Excel file: {file_path}")
        
        # Specifically load the "PRE ALLOCATION" sheet
        try:
            logger.info("Loading 'PRE ALLOCATION' sheet from Excel file")
            df = pd.read_excel(file_path, sheet_name="PRE ALLOCATION")
            
            # Check if the sheet loaded successfully
            if df is not None and not df.empty:
                logger.info(f"Successfully loaded 'PRE ALLOCATION' sheet with {len(df)} rows and {len(df.columns)} columns")
                return df
            else:
                logger.warning("The 'PRE ALLOCATION' sheet was empty or could not be loaded")
        except Exception as e:
            logger.warning(f"Error loading 'PRE ALLOCATION' sheet: {e}")
            
            # Check if Excel file has a sheet named without spaces
            try:
                logger.info("Trying to load 'PRE_ALLOCATION' sheet (without spaces)")
                df = pd.read_excel(file_path, sheet_name="PRE_ALLOCATION")
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


def get_xlsx_files_from_source() -> List[Path]:
    """
    Get a list of all xlsx files in the source directory.

    Returns:
        List[Path]: List of paths to xlsx files
    """
    source_dir = Path('source')
    if not source_dir.exists():
        logger.warning(f"Source directory not found: {source_dir}")
        return []
    
    xlsx_files = list(source_dir.glob('*.xlsx'))
    logger.info(f"Found {len(xlsx_files)} xlsx files in source directory")
    return xlsx_files


def read_stores_csv() -> Optional[pd.DataFrame]:
    """
    Read the stores.csv file from the stores directory and return unique stores.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing unique store data or None if loading failed
    """
    stores_file = Path('stores/stores.csv')
    try:
        if not stores_file.exists():
            logger.error(f"Stores CSV file not found: {stores_file}")
            return None
        
        logger.info(f"Loading stores from CSV: {stores_file}")
        
        # The stores file appears to have no headers, just store names
        # We'll read it as a single column dataframe
        stores_df = pd.read_csv(stores_file, header=None, names=['store_name'])
        
        # Remove any blank rows
        stores_df = stores_df[stores_df['store_name'].notna()]
        stores_df = stores_df[stores_df['store_name'].str.strip() != '']
        
        # Drop duplicates
        unique_stores = stores_df.drop_duplicates()
        logger.info(f"Found {len(unique_stores)} unique stores")
        
        return unique_stores
    except Exception as e:
        logger.error(f"Error reading stores CSV: {e}")
        return None


def extract_important_columns(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Extract important columns from the dataframe, specifically EANCode and SEASON.
    
    Args:
        df (pd.DataFrame): DataFrame containing the Excel data
        
    Returns:
        Optional[pd.DataFrame]: DataFrame with only the important columns or None if the columns don't exist
    """
    important_columns = ['EANCode', 'SEASON']
    
    # Check if the important columns exist in the dataframe
    missing_columns = [col for col in important_columns if col not in df.columns]
    if missing_columns:
        logger.warning(f"Missing important columns in the dataframe: {missing_columns}")
        # Return the dataframe with only the available important columns
        available_columns = [col for col in important_columns if col in df.columns]
        if not available_columns:
            logger.error("No important columns found in the dataframe")
            return None
        return df[available_columns]
    
    logger.info(f"Extracted important columns: {important_columns}")
    return df[important_columns]


def find_common_columns(xlsx_df: pd.DataFrame, stores_df: pd.DataFrame) -> List[str]:
    """
    Find columns that are common between the xlsx dataframe and stores dataframe.
    
    Args:
        xlsx_df (pd.DataFrame): DataFrame containing the Excel data
        stores_df (pd.DataFrame): DataFrame containing the stores data
        
    Returns:
        List[str]: List of column names that exist in both dataframes
    """
    xlsx_columns = set(xlsx_df.columns)
    stores_columns = set(stores_df.columns)
    common_columns = list(xlsx_columns.intersection(stores_columns))
    
    logger.info(f"Found {len(common_columns)} common columns between XLSX and stores CSV: {common_columns}")
    return common_columns


def merge_data(xlsx_df: pd.DataFrame, stores_df: pd.DataFrame, on_column: str) -> Optional[pd.DataFrame]:
    """
    Merge the XLSX dataframe with the stores dataframe based on a common column.
    
    Args:
        xlsx_df (pd.DataFrame): DataFrame containing the Excel data
        stores_df (pd.DataFrame): DataFrame containing the stores data
        on_column (str): Column name to join the dataframes on
        
    Returns:
        Optional[pd.DataFrame]: Merged DataFrame or None if the merge fails
    """
    try:
        if on_column not in xlsx_df.columns or on_column not in stores_df.columns:
            logger.error(f"Column {on_column} not found in both dataframes")
            return None
        
        merged_df = pd.merge(xlsx_df, stores_df, on=on_column, how='inner')
        logger.info(f"Successfully merged dataframes on column '{on_column}', resulting in {len(merged_df)} rows")
        return merged_df
    except Exception as e:
        logger.error(f"Error merging dataframes: {e}")
        return None 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Worker module for handling Excel and CSV file operations.

This module provides the main process flow by:
1. Importing xlsx files from the source directory
2. Reading unique stores from a CSV file in the stores directory
3. For each store in stores.csv, finding matching columns in xlsx
4. Creating new Excel files for each store containing:
   - The store-specific column
   - EANCode column
   - SEASON column
5. Within each store file, creating separate sheets for each distinct SEASON value
6. Creating TXT files for each store-season combination with repeated EANCode values
   based on the quantity value in the store's column
"""

import sys
import os
import logging
import pandas as pd
from pathlib import Path
from functions import (
    load_xlsx_file,
    get_xlsx_files_from_source,
    read_stores_csv
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_store_column(df: pd.DataFrame, store_name: str) -> str:
    """
    Find the column in the DataFrame that exactly matches the store name.
    
    Args:
        df (pd.DataFrame): DataFrame to search in
        store_name (str): Store name to find
    
    Returns:
        str: Matching column name or None if not found
    """
    for col in df.columns:
        if col == store_name:
            return col
    
    # If exact match not found, try to find a column containing the store name
    for col in df.columns:
        if isinstance(col, str) and store_name in col:
            return col
    
    return None


def create_txt_file_with_repeated_eancodes(df: pd.DataFrame, ean_col: str, store_col: str, output_path: Path) -> None:
    """
    Create a text file with repeated EANCode values based on quantity values.
    
    Args:
        df (pd.DataFrame): DataFrame containing the data
        ean_col (str): Name of the EANCode column
        store_col (str): Name of the store column containing quantity values
        output_path (Path): Path to save the output text file
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
    except Exception as e:
        logger.error(f"Error creating TXT file {output_path}: {e}")


def process_store(store_name: str, xlsx_df: pd.DataFrame, output_dir: Path) -> None:
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
    """
    # Find column containing the store name
    store_col = find_store_column(xlsx_df, store_name)
    
    if store_col:
        logger.info(f"Found column matching store '{store_name}': {store_col}")
        
        # Identify EANCode and SEASON columns
        ean_col = None
        season_col = None
        
        for col in xlsx_df.columns:
            if isinstance(col, str):
                if 'EANCode' in col:
                    ean_col = col
                elif 'SEASON' in col:
                    season_col = col
        
        if not ean_col or not season_col:
            logger.warning(f"Could not find EANCode or SEASON columns for store {store_name}")
            return
        
        # Create a dataframe with the required columns
        result_columns = [ean_col, season_col, store_col]
        result_df = xlsx_df[result_columns].copy()
        
        # Filter rows where the store column has a value
        filtered_df = result_df[result_df[store_col].notna()]
        
        # If we have data, create an Excel file with separate sheets for each SEASON
        if not filtered_df.empty:
            # Create valid filename from store name (replace invalid characters)
            valid_filename = store_name.replace('/', '_').replace('\\', '_').replace(' ', '_')
            excel_file_path = output_dir / f"{valid_filename}.xlsx"
            
            # Get unique SEASON values
            unique_seasons = filtered_df[season_col].dropna().unique()
            logger.info(f"Found {len(unique_seasons)} unique SEASON values for store {store_name}")
            
            try:
                # Create a Pandas ExcelWriter
                with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                    # First, save all data to a sheet named 'ALL_SEASONS'
                    filtered_df.to_excel(writer, sheet_name='ALL_SEASONS', index=False)
                    
                    # Then create a sheet for each unique SEASON
                    for season in unique_seasons:
                        # Filter rows for this SEASON
                        season_df = filtered_df[filtered_df[season_col] == season]
                        
                        # Convert season to a valid sheet name if needed
                        sheet_name = str(season)
                        if len(sheet_name) > 31:  # Excel has a 31 character limit for sheet names
                            sheet_name = sheet_name[:31]
                        
                        # Replace any characters that aren't allowed in Excel sheet names
                        invalid_chars = [':', '\\', '/', '?', '*', '[', ']']
                        for char in invalid_chars:
                            sheet_name = sheet_name.replace(char, '_')
                        
                        # Save this season's data to its own sheet
                        season_df.to_excel(writer, sheet_name=sheet_name, index=False)
                        logger.info(f"Added sheet '{sheet_name}' with {len(season_df)} rows")
                        
                        # Create TXT file with repeated EANCodes for this store-season combination
                        season_str = str(season).replace(' ', '_').replace('.', '_')
                        txt_filename = f"{valid_filename}-{season_str}.txt"
                        txt_file_path = output_dir / txt_filename
                        
                        # Create the TXT file with repeated EANCodes
                        create_txt_file_with_repeated_eancodes(
                            season_df, ean_col, store_col, txt_file_path
                        )
                
                logger.info(f"Saved data for store {store_name} to {excel_file_path} with {len(unique_seasons)} season sheets")
            except PermissionError:
                logger.error(f"Permission denied when writing to file {excel_file_path}. The file may be open in another program.")
            except Exception as e:
                logger.error(f"Error saving data for store {store_name}: {e}")
        else:
            logger.warning(f"Store '{store_name}' found, but no data available")
    else:
        logger.warning(f"Store '{store_name}' not found in xlsx column headers")


def main():
    """Main function to execute all tasks."""
    # Step 1: Get all xlsx files from source directory
    xlsx_files = get_xlsx_files_from_source()
    
    if not xlsx_files:
        logger.error("No xlsx files found in source directory. Exiting.")
        return
    
    # Step 2: Read unique stores from CSV
    stores_df = read_stores_csv()
    if stores_df is None:
        logger.error("Failed to load stores data. Exiting.")
        return
    
    logger.info(f"Stores data loaded successfully with {len(stores_df)} unique stores")
    
    # Create output directory if it doesn't exist
    output_dir = Path('output')
    if not output_dir.exists():
        output_dir.mkdir()
        logger.info(f"Created output directory: {output_dir}")
    
    # Process the first (or only) xlsx file
    file_path = xlsx_files[0]
    logger.info(f"Processing file: {file_path}")
    
    # Load the xlsx file (specifically the "PRE ALLOCATION" sheet)
    xlsx_df = load_xlsx_file(file_path)
    if xlsx_df is None:
        logger.error(f"Failed to load Excel file. Exiting.")
        return
    
    # Print columns to help with troubleshooting
    logger.info("Available columns in the Excel file:")
    for col in xlsx_df.columns:
        print(f"Column: {col}")
    
    # Process each store in stores_df
    logger.info("\nProcessing stores from stores.csv...")
    for _, store_row in stores_df.iterrows():
        store_name = store_row['store_name']
        process_store(store_name, xlsx_df, output_dir)
    
    logger.info("Processing completed successfully")
    print(f"All store files have been saved to the '{output_dir}' directory")


if __name__ == "__main__":
    main()

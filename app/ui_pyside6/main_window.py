#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main window module for Excel File Processor GUI (PySide6 version).

This module defines the ExcelProcessorApp class that creates the main GUI window
and sets up the UI components using PySide6 (Qt for Python).
"""

import os
import sys
import logging
import tempfile
import webbrowser
import threading
from pathlib import Path
import pandas as pd
from PIL import Image

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog,
    QProgressBar, QTextEdit, QGroupBox, QMessageBox, QFrame,
    QApplication
)
from PySide6.QtCore import Qt, QSize, Signal, QObject, Slot
from PySide6.QtGui import QFont, QPixmap, QTextCursor, QIcon

try:
    # For SVG support
    import cairosvg
except ImportError:
    cairosvg = None

from app.ui_pyside6.utils import (
    load_image_to_pixmap, create_branded_header, 
    load_svg_to_pixmap
)
# We'll import these specifically in the methods for better error handling
# from app.ui_pyside6.templates import show_stores_template, show_excel_template
from app.processors.file_processor import FileProcessor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Worker class for background processing
class ProcessingWorker(QObject):
    """Worker object that runs the file processing in a separate thread"""
    progress_update = Signal(str, int)
    finished = Signal(bool, str)
    log_message = Signal(str)
    
    def __init__(self, file_processor, stores_path, excel_path, output_dir, sheet_name):
        super().__init__()
        self.file_processor = file_processor
        self.stores_path = stores_path
        self.excel_path = excel_path
        self.output_dir = output_dir
        self.sheet_name = sheet_name
    
    @Slot()
    def process(self):
        """Process the files (runs in a separate thread)"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)
            
            self.log_message.emit(f"Starting processing with:")
            self.log_message.emit(f"- Stores CSV: {self.stores_path}")
            self.log_message.emit(f"- Excel File: {self.excel_path}")
            self.log_message.emit(f"- Output Dir: {self.output_dir}")
            self.log_message.emit(f"- Sheet Name: {self.sheet_name}")
            
            # Update status
            self.progress_update.emit("Reading stores CSV...", 10)
            
            # Read stores from CSV file
            stores_df = self.file_processor.read_stores_csv(self.stores_path)
            
            if stores_df is None or stores_df.empty:
                raise Exception("Failed to read stores CSV or no stores found")
                
            self.log_message.emit(f"Found {len(stores_df)} stores in CSV")
            
            # Update status
            self.progress_update.emit("Reading Excel file...", 20)
            
            # Read Excel file
            xlsx_df = self.file_processor.load_xlsx_file(self.excel_path, self.sheet_name)
            
            if xlsx_df is None or xlsx_df.empty:
                raise Exception("Failed to read Excel file or no data found")
                
            self.log_message.emit(f"Read Excel file with {len(xlsx_df)} rows and {len(xlsx_df.columns)} columns")
            
            # Process each store
            total_stores = len(stores_df)
            processed_count = 0
            
            for _, store_row in stores_df.iterrows():
                store_name = store_row['store_name']
                
                # Update status
                progress = 20 + (70 * processed_count / total_stores)
                self.progress_update.emit(f"Processing store: {store_name}", int(progress))
                
                # Process the store
                self.file_processor.process_store(store_name, xlsx_df, Path(self.output_dir))
                
                processed_count += 1
                self.log_message.emit(f"Processed store: {store_name}")
            
            self.progress_update.emit("Processing completed successfully!", 100)
            self.log_message.emit(f"Processing completed successfully. Output saved to: {self.output_dir}")
            
            # Signal success
            self.finished.emit(True, f"Successfully processed {processed_count} stores.\nOutput files saved to: {self.output_dir}")
            
        except Exception as e:
            self.progress_update.emit(f"Error: {e}", 0)
            self.log_message.emit(f"Error processing files: {e}")
            self.finished.emit(False, str(e))

class ExcelProcessorApp(QMainWindow):
    """Main application window for Excel File Processor (PySide6 version)"""
    
    def __init__(self):
        super().__init__()
        # Initialize main window properties
        self.setWindowTitle("Philipp Plein Outlet Allocation Tool")
        
        # Set a standard size for the window (width, height)
        # Increasing size to better fit content and make buttons more readable
        standard_width = 1200  # Increased width
        standard_height = 1000  # Increased height to 1000
        
        # Make the window fixed size (non-resizable)
        self.setFixedSize(standard_width, standard_height)
        
        # Center the window on the screen
        self.center_window()
        
        # Set application icon
        self.set_application_icon()
        
        # Initialize variables
        self.stores_csv_path = ""
        self.excel_file_path = ""
        self.output_dir = ""
        self.sheet_name = "PRE ALLOCATION"
        self.same_folder = True
        self.processing = False
        
        # Create file processor instance
        self.file_processor = FileProcessor()
        
        # Set up the UI
        self.setup_ui()
        
        # Initialize with a log message
        self.log("Application started. Ready to process files.")
    
    def center_window(self):
        """Center the window on the screen"""
        # Get the available geometry of the screen
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        
        # Calculate the center position
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        
        # Move the window to the center
        self.move(x, y)
    
    def set_application_icon(self):
        """Set the application icon"""
        icon_path = Path("images/logo.png")
        if icon_path.exists():
            app_icon = QIcon(str(icon_path))
            self.setWindowIcon(app_icon)
        
    def setup_ui(self):
        """Create the user interface components"""
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        # Set margins for double spacing (40px) above header
        self.main_layout.setContentsMargins(0, 40, 0, 0)  # Double top margin
        self.main_layout.setSpacing(0)  # Control spacing between header and content explicitly
        self.central_widget.setStyleSheet("""
            background-color: white; 
            color: black;
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 3px;
                font-size: 12pt;
            }
            QLineEdit:focus {
                border: 1px solid #aaa;
            }
            QLabel {
                font-size: 13pt;
            }
            QCheckBox {
                font-size: 12pt;
            }
            QGroupBox {
                font-size: 16pt;
            }
        """)
        
        # Add branded header at the top with zero spacing
        header = create_branded_header(self)
        self.main_layout.addWidget(header)
        
        # Content container (with double spacing at top)
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(30, 40, 30, 30)  # Increased margins
        content_layout.setSpacing(30)  # Increased spacing between sections
        self.main_layout.addWidget(content_container)
        
        # Original button style - unmodified
        self.button_style = """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid black;
                border-radius: 3px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:pressed {
                background-color: #333;
                color: white;
            }
        """
        
        #
        # FILE SELECTION SECTION
        #
        file_section = QGroupBox("File Selection")
        file_section.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 15px;
                padding: 20px;
                font-size: 16pt;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """)
        content_layout.addWidget(file_section)
        file_layout = QVBoxLayout(file_section)
        file_layout.setSpacing(20)  # Increased spacing between form elements
        
        # Stores CSV selection
        stores_frame = QFrame()
        stores_layout = QHBoxLayout(stores_frame)
        stores_layout.setContentsMargins(0, 0, 0, 0)
        
        stores_label = QLabel("Stores CSV File:")
        stores_label.setFixedWidth(180)  # Increased width
        stores_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
        stores_layout.addWidget(stores_label)
        
        self.stores_entry = QLineEdit()
        self.stores_entry.setText(self.stores_csv_path)
        self.stores_entry.setMinimumHeight(36)  # Increased height
        stores_layout.addWidget(self.stores_entry, 1)  # 1 = stretch factor
        
        browse_stores_btn = QPushButton("Browse...")
        browse_stores_btn.setStyleSheet(self.button_style)
        browse_stores_btn.clicked.connect(self.browse_stores_csv)
        browse_stores_btn.setFixedWidth(100)  # Original width
        stores_layout.addWidget(browse_stores_btn)
        
        # Show Template button for stores CSV
        show_stores_btn = QPushButton("Show Template")
        show_stores_btn.setStyleSheet(self.button_style)
        show_stores_btn.clicked.connect(self.show_stores_template)
        show_stores_btn.setFixedWidth(120)  # Original width
        stores_layout.addWidget(show_stores_btn)
        
        file_layout.addWidget(stores_frame)
        
        # Excel file selection
        excel_frame = QFrame()
        excel_layout = QHBoxLayout(excel_frame)
        excel_layout.setContentsMargins(0, 0, 0, 0)
        
        excel_label = QLabel("Excel File:")
        excel_label.setFixedWidth(180)  # Increased width
        excel_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
        excel_layout.addWidget(excel_label)
        
        self.excel_entry = QLineEdit()
        self.excel_entry.setText(self.excel_file_path)
        self.excel_entry.setMinimumHeight(36)  # Increased height
        excel_layout.addWidget(self.excel_entry, 1)  # 1 = stretch factor
        
        browse_excel_btn = QPushButton("Browse...")
        browse_excel_btn.setStyleSheet(self.button_style)
        browse_excel_btn.clicked.connect(self.browse_excel_file)
        browse_excel_btn.setFixedWidth(100)  # Original width
        excel_layout.addWidget(browse_excel_btn)
        
        # Show Template button for Excel file
        show_excel_btn = QPushButton("Show Template")
        show_excel_btn.setStyleSheet(self.button_style)
        show_excel_btn.clicked.connect(self.show_excel_template)
        show_excel_btn.setFixedWidth(120)  # Original width
        excel_layout.addWidget(show_excel_btn)
        
        file_layout.addWidget(excel_frame)
        
        # Output directory selection
        output_frame = QFrame()
        output_layout = QHBoxLayout(output_frame)
        output_layout.setContentsMargins(0, 0, 0, 0)
        
        output_label = QLabel("Output Directory:")
        output_label.setFixedWidth(180)  # Increased width
        output_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
        output_layout.addWidget(output_label)
        
        self.output_entry = QLineEdit()
        self.output_entry.setText(self.output_dir)
        self.output_entry.setMinimumHeight(36)  # Increased height
        output_layout.addWidget(self.output_entry, 1)  # 1 = stretch factor
        
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.setStyleSheet(self.button_style)
        browse_output_btn.clicked.connect(self.browse_output_dir)
        browse_output_btn.setFixedWidth(100)  # Original width
        output_layout.addWidget(browse_output_btn)
        
        # Add empty widget with same width as Show Template to align buttons
        empty_widget = QWidget()
        empty_widget.setFixedWidth(120)  # Original width
        output_layout.addWidget(empty_widget)
        
        file_layout.addWidget(output_frame)
        
        # Same folder checkbox
        same_folder_frame = QFrame()
        same_folder_layout = QHBoxLayout(same_folder_frame)
        same_folder_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add a spacer with the same width as the labels for alignment
        spacer = QWidget()
        spacer.setFixedWidth(180)  # Increased width
        same_folder_layout.addWidget(spacer)
        
        self.same_folder_check = QCheckBox("Use Excel file directory as output")
        self.same_folder_check.setStyleSheet("font-size: 13pt;")  # Increased font size
        self.same_folder_check.setChecked(self.same_folder)
        self.same_folder_check.toggled.connect(self.toggle_output_dir)
        same_folder_layout.addWidget(self.same_folder_check)
        same_folder_layout.addStretch()  # Add spacer to align checkbox to the left
        
        file_layout.addWidget(same_folder_frame)
        
        # Sheet name frame
        sheet_frame = QFrame()
        sheet_layout = QHBoxLayout(sheet_frame)
        sheet_layout.setContentsMargins(0, 0, 0, 0)
        
        sheet_label = QLabel("Sheet Name:")
        sheet_label.setFixedWidth(180)  # Increased width
        sheet_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
        sheet_layout.addWidget(sheet_label)
        
        self.sheet_entry = QLineEdit()
        self.sheet_entry.setText(self.sheet_name)
        self.sheet_entry.setMinimumHeight(36)  # Increased height
        sheet_layout.addWidget(self.sheet_entry, 1)  # 1 = stretch factor
        
        # Add empty widgets to align with other rows
        empty_widget1 = QWidget()
        empty_widget1.setFixedWidth(100)  # Original width
        sheet_layout.addWidget(empty_widget1)
        
        empty_widget2 = QWidget()
        empty_widget2.setFixedWidth(120)  # Original width
        sheet_layout.addWidget(empty_widget2)
        
        file_layout.addWidget(sheet_frame)
        
        #
        # PROCESSING SECTION
        #
        processing_section = QGroupBox("Process Files")
        processing_section.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 15px;
                padding: 20px;
                font-size: 16pt;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """)
        content_layout.addWidget(processing_section)
        processing_layout = QVBoxLayout(processing_section)
        processing_layout.setSpacing(20)  # Increased spacing
        
        # Process button (primary CTA) - keeping original style but with slightly increased height
        process_frame = QFrame()
        process_layout = QHBoxLayout(process_frame)
        process_layout.setContentsMargins(0, 0, 0, 0)
        
        self.process_files_btn = QPushButton("PROCESS FILES")
        # Original process button style
        self.process_files_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-size: 12pt;
                font-weight: bold;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: #333;
            }
            QPushButton:pressed {
                background-color: #555;
            }
        """)
        self.process_files_btn.clicked.connect(self.start_processing)
        process_layout.addWidget(self.process_files_btn)
        process_layout.addStretch()
        
        processing_layout.addWidget(process_frame)
        
        #
        # RESULTS SECTION
        #
        results_section = QGroupBox("Results")
        results_section.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 15px;
                padding: 20px;
                font-size: 16pt;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """)
        content_layout.addWidget(results_section)
        results_layout = QVBoxLayout(results_section)
        results_layout.setSpacing(20)  # Increased spacing
        
        # Progress bar and status
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        # Progress bar with custom styling
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 3px;
                text-align: center;
                height: 30px;
                background-color: white;
                color: black;
                font-size: 12pt;
            }
            QProgressBar::chunk {
                background-color: black;
            }
        """)
        self.progress_bar.setMinimumHeight(36)  # Increased height
        status_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to process")
        self.status_label.setStyleSheet("font-size: 13pt;")  # Increased font size
        status_layout.addWidget(self.status_label)
        
        results_layout.addWidget(status_frame)
        
        # Log area with title
        log_title = QLabel("Processing Log:")
        log_title.setStyleSheet("font-size: 13pt; font-weight: bold;")
        results_layout.addWidget(log_title)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 3px;
                font-family: monospace;
                padding: 8px;
                font-size: 12pt;
            }
        """)
        results_layout.addWidget(self.log_text)
        
        # Add the info buttons at the bottom center - original button size
        info_buttons_frame = QFrame()
        info_buttons_layout = QHBoxLayout(info_buttons_frame)
        info_buttons_layout.setContentsMargins(0, 20, 0, 0)  # Increased top margin
        
        # Add stretchable space on the left
        info_buttons_layout.addStretch(1)
        
        # Show Process Button - original style and size
        self.process_btn = QPushButton("Show Process")
        self.process_btn.setStyleSheet(self.button_style)
        self.process_btn.clicked.connect(self.show_process_diagram)
        self.process_btn.setFixedWidth(120)  # Original width
        info_buttons_layout.addWidget(self.process_btn)
        
        # Add some spacing between buttons
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(10)  # Original spacing
        info_buttons_layout.addWidget(spacer_widget)
        
        # How to use Button - original style and size
        self.help_btn = QPushButton("How to Use")
        self.help_btn.setStyleSheet(self.button_style)
        self.help_btn.clicked.connect(self.show_user_guide)
        self.help_btn.setFixedWidth(120)  # Original width
        info_buttons_layout.addWidget(self.help_btn)
        
        # Add stretchable space on the right
        info_buttons_layout.addStretch(1)
        
        # Add the info buttons to the main content layout
        content_layout.addWidget(info_buttons_frame)
        
        # Initialize output directory state
        self.toggle_output_dir()
        
        # Apply consistent font smoothing
        self.setStyleSheet("""
            * {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
        """)
    
    def browse_stores_csv(self):
        """Browse for a stores CSV file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Stores CSV File",
            "",
            "CSV files (*.csv);;All files (*.*)"
        )
        if filename:
            self.stores_csv_path = filename
            self.stores_entry.setText(filename)
            self.log(f"Selected stores CSV file: {filename}")
    
    def browse_excel_file(self):
        """Browse for an Excel file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel files (*.xlsx *.xls);;All files (*.*)"
        )
        if filename:
            self.excel_file_path = filename
            self.excel_entry.setText(filename)
            
            # If "same folder" is checked, update output directory
            if self.same_folder:
                self.output_dir = os.path.dirname(filename)
                self.output_entry.setText(self.output_dir)
                
            self.log(f"Selected Excel file: {filename}")
    
    def show_stores_template(self):
        """Show an example template for the stores CSV file"""
        from app.ui_pyside6.templates import show_stores_template
        show_stores_template(self, self)
    
    def show_excel_template(self):
        """Show an example template for the Excel file"""
        from app.ui_pyside6.templates import show_excel_template
        show_excel_template(self, self)
        
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            ""
        )
        if directory:
            self.output_dir = directory
            self.output_entry.setText(directory)
            self.log(f"Selected output directory: {directory}")
    
    def toggle_output_dir(self):
        """Enable/disable output directory based on checkbox state"""
        self.output_entry.setEnabled(not self.same_folder_check.isChecked())
        
        # If checkbox is checked, use Excel file directory
        if self.same_folder_check.isChecked() and self.excel_file_path:
            self.output_dir = os.path.dirname(self.excel_file_path)
            self.output_entry.setText(self.output_dir)
    
    def show_process_diagram(self):
        """Show diagram illustrating the process flow"""
        process_svg_path = Path("process_bpmn/process.svg")
        
        if not process_svg_path.exists():
            QMessageBox.warning(
                self,
                "Missing Resource",
                "The process diagram (process.svg) could not be found."
            )
            return
            
        try:
            # Try to open the SVG file with the default browser
            webbrowser.open('file://' + str(process_svg_path.absolute()))
            self.log(f"Opened process diagram: {process_svg_path}")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open the process diagram: {e}"
            )
    
    def show_user_guide(self):
        """Show user guide"""
        guide_path = Path("instructions.html")
        
        if not guide_path.exists():
            QMessageBox.warning(
                self,
                "Missing Resource",
                "The instructions.html file could not be found."
            )
            return
            
        try:
            # Open the HTML file with the default browser
            webbrowser.open('file://' + str(guide_path.absolute()))
            self.log(f"Opened user guide: {guide_path}")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not open the user guide: {e}"
            )
            
    def start_processing(self):
        """Start the file processing operation"""
        # Validate inputs
        if not self.stores_csv_path:
            QMessageBox.warning(
                self,
                "Missing Input",
                "Please select a stores CSV file."
            )
            return
            
        if not self.excel_file_path:
            QMessageBox.warning(
                self,
                "Missing Input",
                "Please select an Excel file."
            )
            return
            
        if not self.output_dir:
            QMessageBox.warning(
                self,
                "Missing Input",
                "Please select an output directory."
            )
            return
            
        if not self.sheet_name:
            QMessageBox.warning(
                self,
                "Missing Input",
                "Please enter a sheet name."
            )
            return
            
        if self.processing:
            QMessageBox.warning(
                self,
                "Processing in Progress",
                "Please wait for the current processing to complete."
            )
            return
            
        # Start processing
        self.processing = True
        self.process_files_btn.setEnabled(False)
        self.status_label.setText("Processing...")
        self.progress_bar.setValue(0)
        
        # Clear log
        self.log_text.clear()
        self.log("Starting processing...")
        
        # Create worker thread for processing
        self.worker = ProcessingWorker(
            self.file_processor,
            self.stores_csv_path,
            self.excel_file_path,
            self.output_dir,
            self.sheet_name
        )
        
        # Connect signals
        self.worker.progress_update.connect(self.update_progress)
        self.worker.finished.connect(self.processing_finished)
        self.worker.log_message.connect(self.log)
        
        # Create thread and start processing
        self.thread = threading.Thread(target=self.worker.process)
        self.thread.daemon = True
        self.thread.start()
    
    def update_progress(self, message, value):
        """Update the progress bar and status message"""
        self.status_label.setText(message)
        self.progress_bar.setValue(value)
        
    def processing_finished(self, success, message):
        """Handle the completion of processing"""
        self.processing = False
        self.process_files_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(
                self,
                "Processing Complete",
                message
            )
            # Open output directory
            if os.path.exists(self.output_dir):
                try:
                    if sys.platform == 'win32':
                        os.startfile(self.output_dir)
                    elif sys.platform == 'darwin':  # macOS
                        os.system(f'open "{self.output_dir}"')
                    else:  # Linux
                        os.system(f'xdg-open "{self.output_dir}"')
                except Exception as e:
                    self.log(f"Could not open output directory: {e}")
        else:
            QMessageBox.critical(
                self,
                "Processing Failed",
                f"Error processing files: {message}"
            )
            
        self.log(f"Processing finished: {'SUCCESS' if success else 'FAILED - ' + message}")
        
    def log(self, message):
        """Add a message to the log text area"""
        # Log to console
        logger.info(message)
        
        # Add to log text area
        self.log_text.append(message)
        
        # Scroll to the bottom
        self.log_text.moveCursor(QTextCursor.End)
        self.log_text.ensureCursorVisible()
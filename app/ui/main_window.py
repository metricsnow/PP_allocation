#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main window module for Excel File Processor GUI.

This module defines the ExcelProcessorApp class that creates the main GUI window
and sets up the UI components.
"""

import os
import sys
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import pandas as pd
import threading
import tempfile
import webbrowser
import io
from PIL import Image, ImageTk

try:
    # For SVG support
    import cairosvg
except ImportError:
    cairosvg = None

from app.ui.utils import load_and_display_image
from app.processors.file_processor import FileProcessor
from app.utils.templates import show_stores_template, show_excel_template

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExcelProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pre Allocation Outlet Production")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Initialize variables for file paths
        self.stores_csv_path = tk.StringVar()
        self.excel_file_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.sheet_name = tk.StringVar(value="PRE ALLOCATION")
        
        # Status variables - defining these before create_widgets is called
        self.processing = False
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to process files")
        
        # Progress bar variable
        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0.0)
        
        # Create file processor instance
        self.file_processor = FileProcessor()
        
        # Create the main UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create the UI widgets."""
        # Set the background to white for all elements
        self.root.configure(bg="white")
        
        # Configure style to ensure all frames have white background
        style = ttk.Style()
        style.configure("TFrame", background="white")
        style.configure("TLabelframe", background="white")
        style.configure("TLabelframe.Label", background="white")
        style.configure("TLabel", background="white")
        style.configure("TCheckbutton", background="white")
        style.configure("TButton", background="white")
        
        main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add PP Logo Image Frame at the top
        logo_frame = ttk.Frame(main_frame, style="TFrame")
        logo_frame.pack(fill=tk.X, pady=5)
        
        # Load and display the PP logo (now at the top)
        self.load_and_display_logo(logo_frame)
        
        # Title and Process Button Frame below the logo
        title_frame = ttk.Frame(main_frame, style="TFrame")
        title_frame.pack(fill=tk.X, pady=10)
        
        # Title
        title_label = ttk.Label(
            title_frame, 
            text="Pre Allocation Outlet Production", 
            font=("Arial", 18, "bold"),
            background="white"
        )
        title_label.pack(side=tk.LEFT, pady=10)
        
        # How to use Button (positioned to the right of title)
        self.help_btn = ttk.Button(
            title_frame,
            text="How to use",
            command=self.show_user_guide,
            style="Black.TButton"
        )
        self.help_btn.pack(side=tk.RIGHT, padx=5)
        
        # Show Process Button (positioned to the right of title)
        self.process_btn = ttk.Button(
            title_frame,
            text="Show Process",
            command=self.show_process_diagram,
            style="Black.TButton"
        )
        self.process_btn.pack(side=tk.RIGHT, padx=5)
        
        # Frame for file selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10", style="TLabelframe")
        file_frame.pack(fill=tk.X, expand=False, pady=10)
        
        # Stores CSV selection
        stores_frame = ttk.Frame(file_frame, style="TFrame")
        stores_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(stores_frame, text="Stores CSV File:", background="white").pack(side=tk.LEFT, padx=5)
        ttk.Entry(stores_frame, textvariable=self.stores_csv_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Show Template button for stores CSV 
        ttk.Button(
            stores_frame, 
            text="Show Template", 
            command=self.show_stores_template,
            style="Black.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            stores_frame, 
            text="Browse...", 
            command=self.browse_stores_csv,
            style="Black.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        # Excel file selection
        excel_frame = ttk.Frame(file_frame, style="TFrame")
        excel_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(excel_frame, text="Excel File:", background="white").pack(side=tk.LEFT, padx=5)
        ttk.Entry(excel_frame, textvariable=self.excel_file_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Show Template button for Excel file
        ttk.Button(
            excel_frame, 
            text="Show Template",
            command=self.show_excel_template,
            style="Black.TButton"
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            excel_frame, 
            text="Browse...", 
            command=self.browse_excel_file,
            style="Black.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        # Output directory selection
        output_frame = ttk.Frame(file_frame, style="TFrame")
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output Directory:", background="white").pack(side=tk.LEFT, padx=5)
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(
            output_frame, 
            text="Browse...", 
            command=self.browse_output_dir,
            style="Black.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        # Processing options
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10", style="TLabelframe")
        options_frame.pack(fill=tk.X, expand=False, pady=10)
        
        # Checkbox for saving files in same folder as input
        self.same_folder_var = tk.BooleanVar(value=True)
        same_folder_check = ttk.Checkbutton(
            options_frame, 
            text="Save output in same folder as Excel file", 
            variable=self.same_folder_var,
            command=self.toggle_output_dir,
            style="TCheckbutton"
        )
        same_folder_check.pack(anchor=tk.W, pady=5)
        
        # Sheet name selection
        sheet_frame = ttk.Frame(options_frame, style="TFrame")
        sheet_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(sheet_frame, text="Excel Sheet Name:", background="white").pack(side=tk.LEFT, padx=5)
        ttk.Entry(sheet_frame, textvariable=self.sheet_name, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Label(sheet_frame, text="(default: PRE ALLOCATION)", background="white").pack(side=tk.LEFT)
        
        # Control Panel Frame - contains buttons to control processing
        control_frame = ttk.Frame(main_frame, style="TFrame")
        control_frame.pack(fill=tk.X, pady=10)
        
        # Process button - extra large and centered
        process_button = ttk.Button(
            control_frame,
            text="Process Files",
            command=self.start_processing,
            style="Black.TButton"
        )
        process_button.pack(side=tk.TOP, pady=10, fill=tk.X)
        
        # Progress bar
        progress_frame = ttk.Frame(main_frame, style="TFrame")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
            length=600
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status label below progress bar
        status_label = ttk.Label(
            progress_frame,
            textvariable=self.status_var,
            background="white",
            font=("Arial", 10)
        )
        status_label.pack(fill=tk.X, pady=5)
        
        # Log Text Box
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="10", style="TLabelframe")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create Text widget
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, width=80, height=8)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Initial log message
        self.log("Application started. Ready to process files.")
        
        # Disable output directory entry initially since same_folder is selected by default
        self.toggle_output_dir()

    def show_process_diagram(self):
        """Show the process diagram image."""
        process_bpmn_dir = Path("process_bpmn")
        if process_bpmn_dir.exists():
            # Try to find an SVG or PNG file
            svg_files = list(process_bpmn_dir.glob("*.svg"))
            png_files = list(process_bpmn_dir.glob("*.png"))
            
            if svg_files:
                svg_path = svg_files[0]
                if cairosvg:
                    # If cairosvg is available, convert SVG to PNG and display
                    try:
                        png_data = cairosvg.svg2png(url=str(svg_path))
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                            tmp.write(png_data)
                            webbrowser.open('file://' + tmp.name)
                        self.log(f"Opened process diagram: {svg_path}")
                        return
                    except Exception as e:
                        self.log(f"Error converting SVG: {e}")
                
                # Fallback to opening the SVG directly
                webbrowser.open('file://' + str(svg_path.absolute()))
                self.log(f"Opened process diagram: {svg_path}")
            elif png_files:
                # Open the PNG file directly
                webbrowser.open('file://' + str(png_files[0].absolute()))
                self.log(f"Opened process diagram: {png_files[0]}")
            else:
                messagebox.showinfo("Process Diagram", "No process diagram found in process_bpmn directory.")
        else:
            messagebox.showinfo("Process Diagram", "Process diagram directory not found.")

    def show_user_guide(self):
        """Show the user guide."""
        # Check for HTML instructions first
        html_guide = Path("instructions.html")
        md_guide = Path("instructions.md")
        
        if html_guide.exists():
            webbrowser.open('file://' + str(html_guide.absolute()))
            self.log("Opened user guide (HTML)")
        elif md_guide.exists():
            # Try opening the markdown file
            try:
                webbrowser.open('file://' + str(md_guide.absolute()))
                self.log("Opened user guide (Markdown)")
            except Exception:
                # If it can't be opened directly, show its content in a message
                try:
                    with open(md_guide, 'r') as f:
                        guide_content = f.read()
                    messagebox.showinfo("User Guide", guide_content)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open user guide: {e}")
        else:
            messagebox.showinfo("User Guide", "No user guide found (instructions.html or instructions.md)")

    def toggle_output_dir(self):
        """Toggle the output directory entry based on the same_folder checkbox."""
        entries = self.root.winfo_children()[0].winfo_children()
        
        # Find the file_frame and then the output_frame within it
        file_frame = None
        for widget in entries:
            if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "File Selection":
                file_frame = widget
                break
        
        if file_frame:
            # Find the output directory entry
            for frame in file_frame.winfo_children():
                for widget in frame.winfo_children():
                    if isinstance(widget, ttk.Entry) and widget.cget("textvariable") == str(self.output_dir):
                        # If same_folder is checked, disable the output directory entry
                        if self.same_folder_var.get():
                            widget.configure(state="disabled")
                        else:
                            widget.configure(state="normal")
                        break

    def browse_stores_csv(self):
        """Browse for a stores CSV file."""
        filename = filedialog.askopenfilename(
            title="Select Stores CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.stores_csv_path.set(filename)
            self.log(f"Selected stores CSV file: {filename}")

    def browse_excel_file(self):
        """Browse for an Excel file."""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.excel_file_path.set(filename)
            self.log(f"Selected Excel file: {filename}")
            
            # If same_folder is checked, set the output directory to the Excel file's directory
            if self.same_folder_var.get():
                excel_dir = os.path.dirname(filename)
                self.output_dir.set(excel_dir)

    def browse_output_dir(self):
        """Browse for an output directory."""
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.output_dir.set(dirname)
            self.log(f"Selected output directory: {dirname}")

    def log(self, message):
        """Add a message to the log text box."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Auto-scroll to the end

    def update_status(self, message, progress=None):
        """Update the status label and progress bar."""
        self.status_var.set(message)
        if progress is not None:
            self.progress_var.set(progress)

    def start_processing(self):
        """Start the file processing in a separate thread."""
        if self.processing:
            messagebox.showinfo("Processing", "Files are already being processed.")
            return
            
        if not self.validate_inputs():
            return
            
        self.processing = True
        self.update_status("Starting processing...", 0)
        
        # Start processing thread
        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()

    def validate_inputs(self):
        """Validate input fields before processing."""
        # Check if stores CSV file is selected
        if not self.stores_csv_path.get():
            messagebox.showerror("Error", "Please select a stores CSV file.")
            return False
            
        # Check if Excel file is selected
        if not self.excel_file_path.get():
            messagebox.showerror("Error", "Please select an Excel file.")
            return False
            
        # Check if output directory is selected (if not using same folder)
        if not self.same_folder_var.get() and not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory.")
            return False
            
        # Check if the files exist
        stores_path = Path(self.stores_csv_path.get())
        excel_path = Path(self.excel_file_path.get())
        
        if not stores_path.exists():
            messagebox.showerror("Error", f"Stores CSV file not found: {stores_path}")
            return False
            
        if not excel_path.exists():
            messagebox.showerror("Error", f"Excel file not found: {excel_path}")
            return False
            
        # If not using same folder, check if output directory exists
        if not self.same_folder_var.get():
            output_path = Path(self.output_dir.get())
            if not output_path.exists():
                # Ask if we should create the directory
                create_dir = messagebox.askyesno(
                    "Directory Not Found", 
                    f"Output directory not found: {output_path}\nDo you want to create it?"
                )
                if create_dir:
                    try:
                        output_path.mkdir(parents=True)
                        self.log(f"Created output directory: {output_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not create output directory: {e}")
                        return False
                else:
                    return False
                    
        return True
    
    def process_files(self):
        """Process the selected files."""
        try:
            # Get the file paths
            stores_path = self.stores_csv_path.get()
            excel_path = self.excel_file_path.get()
            sheet_name = self.sheet_name.get() or "PRE ALLOCATION"
            
            # Determine output directory
            if self.same_folder_var.get():
                output_dir = os.path.dirname(excel_path)
            else:
                output_dir = self.output_dir.get()
                
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            self.log(f"Starting processing with:")
            self.log(f"- Stores CSV: {stores_path}")
            self.log(f"- Excel File: {excel_path}")
            self.log(f"- Output Dir: {output_dir}")
            self.log(f"- Sheet Name: {sheet_name}")
            
            # Update status
            self.update_status("Reading stores CSV...", 10)
            
            # Read stores from CSV file
            stores_df = self.file_processor.read_stores_csv(stores_path)
            
            if stores_df is None or stores_df.empty:
                raise Exception("Failed to read stores CSV or no stores found")
                
            self.log(f"Found {len(stores_df)} stores in CSV")
            
            # Update status
            self.update_status("Reading Excel file...", 20)
            
            # Read Excel file
            xlsx_df = self.file_processor.load_xlsx_file(excel_path, sheet_name)
            
            if xlsx_df is None or xlsx_df.empty:
                raise Exception("Failed to read Excel file or no data found")
                
            self.log(f"Read Excel file with {len(xlsx_df)} rows and {len(xlsx_df.columns)} columns")
            
            # Process each store
            total_stores = len(stores_df)
            processed_count = 0
            
            for _, store_row in stores_df.iterrows():
                store_name = store_row['store_name']
                
                # Update status
                progress = 20 + (70 * processed_count / total_stores)
                self.update_status(f"Processing store: {store_name}", progress)
                
                # Process the store
                self.file_processor.process_store(store_name, xlsx_df, Path(output_dir))
                
                processed_count += 1
                self.log(f"Processed store: {store_name}")
            
            self.update_status("Processing completed successfully!", 100)
            self.log(f"Processing completed successfully. Output saved to: {output_dir}")
            
            # Show a message box with the results
            messagebox.showinfo(
                "Processing Complete", 
                f"Successfully processed {processed_count} stores.\nOutput files saved to: {output_dir}"
            )
            
        except Exception as e:
            self.update_status(f"Error: {e}", 0)
            self.log(f"Error processing files: {e}")
            messagebox.showerror("Processing Error", str(e))
        finally:
            self.processing = False

    def show_stores_template(self):
        """Show an example template for the stores CSV file."""
        show_stores_template(self)

    def show_excel_template(self):
        """Show an example template for the Excel file."""
        show_excel_template(self)

    def load_and_display_logo(self, parent_frame):
        """Load and display the PP logo."""
        logo_path = Path("images/pp_logo.png")
        
        if logo_path.exists():
            try:
                # Load the image
                image = Image.open(logo_path)
                
                # Resize the image to a reasonable height (80px) while maintaining aspect ratio
                original_width, original_height = image.size
                new_height = 80
                new_width = int(original_width * (new_height / original_height))
                
                image = image.resize((new_width, new_height), Image.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Store reference to prevent garbage collection
                self.logo_photo = photo
                
                # Create label and display image
                logo_label = ttk.Label(parent_frame, image=photo, background="white")
                logo_label.image = photo  # Keep a reference
                logo_label.pack(side=tk.LEFT, padx=10, pady=10)
                
                return logo_label
            except Exception as e:
                logger.error(f"Error loading logo image: {e}")
                return None
        else:
            logger.warning(f"Logo image not found: {logo_path}")
            return None 
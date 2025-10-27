#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI utilities module for Excel File Processor.

This module provides utility functions for UI operations such as:
1. Loading and displaying images
2. Creating and configuring UI components
"""

import os
import logging
import tempfile
import io
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_and_display_image(parent_frame, image_path, height=80, background="white", side=tk.LEFT, padx=10, pady=10):
    """
    Load an image from file and display it in a label.
    
    Args:
        parent_frame: The parent tkinter frame to display the image in
        image_path (str or Path): Path to the image file
        height (int): Height to resize the image to (maintains aspect ratio)
        background (str): Background color for the label
        side (tk constant): Side to pack the label on
        padx (int): X padding for the label
        pady (int): Y padding for the label
        
    Returns:
        tk.Label or None: The label containing the image, or None if loading failed
    """
    image_path = Path(image_path)
    
    if image_path.exists():
        try:
            # Load the image
            image = Image.open(image_path)
            
            # Resize the image to specified height while maintaining aspect ratio
            original_width, original_height = image.size
            new_height = height
            new_width = int(original_width * (new_height / original_height))
            
            image = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Create label and display image
            label = ttk.Label(parent_frame, image=photo, background=background)
            label.image = photo  # Keep a reference
            label.pack(side=side, padx=padx, pady=pady)
            
            return label
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    else:
        logger.warning(f"Image not found: {image_path}")
        return None

def create_labeled_entry(parent, label_text, variable, width=50, browse_command=None):
    """
    Create a frame with a label, entry widget, and optional browse button.
    
    Args:
        parent: The parent tkinter container
        label_text (str): Text for the label
        variable (tk.StringVar): Variable to bind to the entry
        width (int): Width of the entry widget
        browse_command (callable, optional): Command to execute when browse button clicked
        
    Returns:
        ttk.Frame: The frame containing the created widgets
    """
    frame = ttk.Frame(parent, style="TFrame")
    frame.pack(fill=tk.X, pady=5)
    
    # Label
    ttk.Label(frame, text=label_text, background="white").pack(side=tk.LEFT, padx=5)
    
    # Entry
    entry = ttk.Entry(frame, textvariable=variable, width=width)
    entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    # Browse button (if command provided)
    if browse_command:
        ttk.Button(
            frame, 
            text="Browse...", 
            command=browse_command,
            style="Black.TButton"
        ).pack(side=tk.LEFT, padx=5)
    
    return frame

def create_status_bar(parent):
    """
    Create a status bar with a label and a progress bar.
    
    Args:
        parent: The parent tkinter container
        
    Returns:
        tuple: (frame, label_var, progress_var)
    """
    frame = ttk.Frame(parent, style="TFrame")
    frame.pack(fill=tk.X, pady=5)
    
    # Create variables
    status_var = tk.StringVar(value="Ready")
    progress_var = tk.DoubleVar(value=0.0)
    
    # Progress bar
    progress_bar = ttk.Progressbar(
        frame,
        variable=progress_var,
        maximum=100,
        mode="determinate"
    )
    progress_bar.pack(fill=tk.X, pady=5)
    
    # Status label
    status_label = ttk.Label(
        frame,
        textvariable=status_var,
        background="white",
        font=("Arial", 10)
    )
    status_label.pack(fill=tk.X, pady=5)
    
    return frame, status_var, progress_var

def create_log_frame(parent, height=8):
    """
    Create a log frame with a text widget and scrollbar.
    
    Args:
        parent: The parent tkinter container
        height (int): Height of the text widget
        
    Returns:
        tuple: (frame, text_widget)
    """
    frame = ttk.LabelFrame(parent, text="Processing Log", padding="10", style="TLabelframe")
    frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Create Text widget
    text_widget = tk.Text(frame, wrap=tk.WORD, width=80, height=height)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    
    return frame, text_widget 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI utilities module for Excel File Processor (PySide6 version).

This module provides utility functions for UI operations such as:
1. Loading and displaying images
2. Creating and configuring UI components
"""

import os
import logging
import tempfile
import io
from pathlib import Path
from PIL import Image
from PySide6.QtWidgets import (
    QLabel, QFrame, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QProgressBar, QTextEdit, QScrollBar
)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtSvg import QSvgRenderer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_svg_to_pixmap(svg_path, width=None, height=None):
    """
    Load an SVG file and convert it to a QPixmap.
    
    Args:
        svg_path (str or Path): Path to the SVG file
        width (int, optional): Width to resize the SVG to
        height (int, optional): Height to resize the SVG to
        
    Returns:
        QPixmap or None: The loaded SVG as a QPixmap, or None if loading failed
    """
    svg_path = Path(svg_path)
    
    if svg_path.exists():
        try:
            # Create SVG renderer
            renderer = QSvgRenderer(str(svg_path))
            
            # Determine size for the pixmap
            if width is None and height is None:
                # Use original size
                size = renderer.defaultSize()
            elif width is None:
                # Calculate width based on height while maintaining aspect ratio
                original_size = renderer.defaultSize()
                aspect_ratio = original_size.width() / original_size.height()
                width = int(height * aspect_ratio)
                size = QSize(width, height)
            elif height is None:
                # Calculate height based on width while maintaining aspect ratio
                original_size = renderer.defaultSize()
                aspect_ratio = original_size.height() / original_size.width()
                height = int(width * aspect_ratio)
                size = QSize(width, height)
            else:
                # Use specified width and height
                size = QSize(width, height)
            
            # Create pixmap with correct size
            pixmap = QPixmap(size)
            pixmap.fill(Qt.transparent)
            
            # Render SVG to pixmap
            painter = QSvgRenderer(str(svg_path))
            painter.render(pixmap)
            
            return pixmap
        except Exception as e:
            logger.error(f"Error loading SVG {svg_path}: {e}")
            return None
    else:
        logger.warning(f"SVG file not found: {svg_path}")
        return None

def load_image_to_pixmap(image_path, height=80):
    """
    Load an image from file and convert it to a QPixmap.
    
    Args:
        image_path (str or Path): Path to the image file
        height (int): Height to resize the image to (maintains aspect ratio)
        
    Returns:
        QPixmap or None: The loaded image as a QPixmap, or None if loading failed
    """
    image_path = Path(image_path)
    
    if image_path.exists():
        try:
            # Load the image using PIL
            pil_image = Image.open(image_path)
            
            # Resize the image to specified height while maintaining aspect ratio
            original_width, original_height = pil_image.size
            new_height = height
            new_width = int(original_width * (new_height / original_height))
            
            pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert PIL image to QPixmap
            img_data = pil_image.tobytes("raw", "RGB")
            qimage = QImage(img_data, pil_image.width, pil_image.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            
            return pixmap
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    else:
        logger.warning(f"Image not found: {image_path}")
        return None

def create_branded_header(parent, app_title="Outlet Allocation Tool", version="v1.0"):
    """
    Create a branded header with the Philipp Plein logo
    
    Args:
        parent: The parent QWidget
        app_title (str): Application title (not used anymore)
        version (str): Version number (not used anymore)
        
    Returns:
        QFrame: The header frame
    """
    # Create a container frame with horizontal padding
    container_frame = QFrame(parent)
    container_frame.setStyleSheet("background-color: white; padding: 0px; margin: 0px;")
    
    # Use horizontal layout with padding on left and right
    container_layout = QHBoxLayout(container_frame)
    container_layout.setContentsMargins(40, 0, 40, 0)  # Add horizontal padding (40px on each side)
    container_layout.setSpacing(0)
    
    # Main header container - using a simple QLabel directly for minimal overhead
    jpg_path = Path("resources/images/header.jpg")
    if jpg_path.exists():
        pixmap = QPixmap(str(jpg_path))
        if not pixmap.isNull():
            # Create label with the image
            header_label = QLabel(parent)
            header_label.setPixmap(pixmap)
            header_label.setAlignment(Qt.AlignCenter)
            header_label.setContentsMargins(0, 0, 0, 0)
            header_label.setStyleSheet("background-color: white; padding: 0px; margin: 0px;")
            
            # Add the header to the container with stretches for centering
            container_layout.addStretch(1)
            container_layout.addWidget(header_label)
            container_layout.addStretch(1)
            
            return container_frame
    
    # Fallback if image loading fails
    header_frame = QFrame(parent)
    header_layout = QHBoxLayout(header_frame)
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(0)
    
    # Add stretch to push content to center
    header_layout.addStretch(1)
    
    # Create text label for fallback
    header_label = QLabel("PHILIPP PLEIN")
    header_label.setStyleSheet("color: black; font-size: 24pt; font-weight: bold;")
    header_layout.addWidget(header_label)
    
    # Add stretch to push content to center
    header_layout.addStretch(1)
    
    return header_frame

def create_labeled_entry(parent, label_text, initial_value="", browse_command=None):
    """
    Create a frame with a label, entry widget, and optional browse button.
    
    Args:
        parent: The parent QWidget
        label_text (str): Text for the label
        initial_value (str): Initial value for the entry
        browse_command (callable, optional): Command to execute when browse button clicked
        
    Returns:
        tuple: (QFrame, QLineEdit) - The frame and the line edit widget
    """
    frame = QFrame(parent)
    layout = QHBoxLayout(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Label
    label = QLabel(label_text, parent)
    layout.addWidget(label)
    
    # Entry
    entry = QLineEdit(parent)
    entry.setText(initial_value)
    layout.addWidget(entry)
    
    # Browse button (if command provided)
    if browse_command:
        browse_button = QPushButton("Browse...", parent)
        browse_button.clicked.connect(browse_command)
        layout.addWidget(browse_button)
    
    return frame, entry

def create_status_bar(parent):
    """
    Create a status bar with a label and a progress bar.
    
    Args:
        parent: The parent QWidget
        
    Returns:
        tuple: (QFrame, QLabel, QProgressBar)
    """
    frame = QFrame(parent)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Progress bar
    progress_bar = QProgressBar(parent)
    progress_bar.setRange(0, 100)
    progress_bar.setValue(0)
    layout.addWidget(progress_bar)
    
    # Status label
    status_label = QLabel("Ready", parent)
    status_label.setAlignment(Qt.AlignLeft)
    layout.addWidget(status_label)
    
    return frame, status_label, progress_bar

def create_log_widget(parent, height=8):
    """
    Create a log widget with a text edit and scrollbar.
    
    Args:
        parent: The parent QWidget
        height (int): Minimum height of the text widget in text lines
        
    Returns:
        tuple: (QFrame, QTextEdit)
    """
    frame = QFrame(parent)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Create Text widget
    text_widget = QTextEdit(parent)
    text_widget.setReadOnly(True)
    text_widget.document().setDocumentMargin(5)
    
    # Set minimum height based on font metrics (approximate)
    font_height = text_widget.fontMetrics().height()
    text_widget.setMinimumHeight(font_height * height + 20)  # Add margin
    
    layout.addWidget(text_widget)
    
    return frame, text_widget 
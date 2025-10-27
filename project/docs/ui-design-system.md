# UI Design System Documentation
## Comprehensive Guide for Reusing Visual Design and UI Components

**Version:** 1.0  
**Date:** 2025-01-27  
**Framework:** PySide6 (Qt for Python)  
**Purpose:** Document all visual design elements for reuse in other projects

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Visual Design System](#visual-design-system)
3. [Color Palette](#color-palette)
4. [Typography](#typography)
5. [Spacing & Layout](#spacing--layout)
6. [Component Library](#component-library)
7. [Layout Patterns](#layout-patterns)
8. [Branding Elements](#branding-elements)
9. [Extraction Guide](#extraction-guide)

---

## Design Philosophy

### Monochrome Minimalist Design
- **Principle**: Clean, professional, monochrome aesthetic with black text on white background
- **Purpose**: Premium luxury brand presentation (Philipp Plein)
- **Approach**: Minimal color, maximum clarity

### Key Design Principles

1. **Clarity over Decoration**: Every element serves a purpose
2. **Consistent Spacing**: Generous whitespace for visual breathing room
3. **Strong Typography**: Bold, readable fonts with clear hierarchy
4. **Bordered Sections**: Subtle borders to group related content
5. **Hover Interactions**: Interactive elements provide clear feedback

---

## Visual Design System

### Window Specifications

```python
# Window Configuration
standard_width = 1200      # Pixels
standard_height = 1000    # Pixels
fixed_size = True         # Non-resizable

# Center window on screen
screen_geometry = QApplication.primaryScreen().availableGeometry()
x = (screen_geometry.width() - window_width) // 2
y = (screen_geometry.height() - window_height) // 2
```

### Layout Structure

```
┌─────────────────────────────────────┐
│        40px top margin              │
├─────────────────────────────────────┤
│      BRANDED HEADER IMAGE           │
│    (Full width, center aligned)     │
├─────────────────────────────────────┤
│  30px margin | CONTENT | 30px       │
│              │                        │
│  [GroupBox: File Selection]         │
│  - Margins: 20px                     │
│  - Spacing: 20px                     │
│              │                        │
│  [GroupBox: Process Files]          │
│              │                        │
│  [GroupBox: Results]                │
│  - Progress Bar                     │
│  - Status Label                     │
│  - Log Text Area                    │
│              │                        │
│  [Info Buttons: Show Process,       │
│   How to Use]                       │
└─────────────────────────────────────┘
```

---

## Color Palette

### Primary Colors

```python
# Core Color Scheme
background_white = "#FFFFFF"        # Main background
text_black = "#000000"               # Primary text
border_gray = "#DDDDDD"              # Borders and dividers
hover_black = "#333333"              # Hover state
pressed_gray = "#555555"             # Pressed state
log_background = "#F8F8F8"           # Log area background
progress_fill = "#000000"            # Progress bar fill
```

### Usage Guidelines

| Element | Color | Hex | Usage |
|---------|-------|-----|-------|
| Background | White | `#FFFFFF` | Main window background |
| Text | Black | `#000000` | All text elements |
| Borders | Light Gray | `#DDDDDD` | GroupBox, LineEdit, ProgressBar borders |
| Log Background | Off-White | `#F8F8F8` | Log text area background |
| Button Hover | Black | `#000000` | Secondary buttons (reverses colors) |

---

## Typography

### Font System

```python
# System Font Stack
font_family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
```

### Font Sizes by Element

| Element | Size | Weight | CSS |
|---------|------|--------|-----|
| GroupBox Titles | 16pt | Bold | `font-size: 16pt; font-weight: bold;` |
| Labels (Form) | 13pt | Bold | `font-size: 13pt; font-weight: bold;` |
| General Labels | 13pt | Normal | `font-size: 13pt;` |
| Line Edit | 12pt | Normal | `font-size: 12pt;` |
| Checkbox | 12pt-13pt | Normal | `font-size: 13pt;` |
| Buttons (Standard) | Default | Bold | `font-weight: bold;` |
| Primary Button | 12pt | Bold/Uppercase | `font-size: 12pt; font-weight: bold; text-transform: uppercase;` |
| Log Text | 12pt | Monospace | `font-family: monospace; font-size: 12pt;` |

### Typography CSS

```css
/* Main Application Font */
* {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Labels */
QLabel {
    font-size: 13pt;
}

/* Form Labels (Bold) */
.bold-label {
    font-size: 13pt;
    font-weight: bold;
}

/* Input Fields */
QLineEdit {
    font-size: 12pt;
}

/* GroupBox Titles */
QGroupBox {
    font-size: 16pt;
    font-weight: bold;
}

/* Log Area */
QTextEdit {
    font-family: monospace;
    font-size: 12pt;
}
```

---

## Spacing & Layout

### Spacing System

```python
# Vertical Spacing
top_margin = 40              # Top of window
section_spacing = 30         # Between sections
element_spacing = 20         # Within sections
padding = 20                 # Inside GroupBox

# Horizontal Spacing
side_margin = 30             # Window sides
header_padding = 40          # Header horizontal padding

# Element Spacing
form_elements_spacing = 20   # Between form rows
button_spacing = 10          # Between buttons
```

### Layout Hierarchy

```
Main Window (1200x1000, fixed)
├── Central Widget (spans full window)
│   └── Main Layout (Vertical)
│       ├── Top Margin: 40px
│       ├── Branded Header
│       ├── Content Container
│       │   ├── Side Margins: 30px each
│       │   ├── Top Margin: 40px
│       │   ├── Bottom Margin: 30px
│       │   └── Spacing: 30px between sections
│       │       ├── File Selection GroupBox (20px padding)
│       │       ├── Processing GroupBox (20px padding)
│       │       └── Results GroupBox (20px padding)
│       └── Info Buttons (centered)
```

### Element Dimensions

```python
# Standard Dimensions
label_width = 180          # Fixed width for form labels
input_height = 36          # Minimum height for inputs
button_width_primary = 100 # Primary action buttons
button_width_secondary = 120 # Secondary/Show buttons

# Spacer Widths
empty_spacer_width_primary = 100   # Align with Browse buttons
empty_spacer_width_secondary = 120 # Align with Show Template buttons
```

---

## Component Library

### 1. Primary Button (PROCESS FILES)

**Style:** Black background, white text, uppercase

```css
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
```

**Dimensions:** Full width, flexible  
**Usage:** Primary call-to-action only

### 2. Secondary Buttons (Browse, Show Template, etc.)

**Style:** White background, black border, reverses on hover

```css
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
```

**Dimensions:** 
- Browse buttons: 100px wide
- Show Template buttons: 120px wide
- Info buttons (Show Process, How to Use): 120px wide

### 3. Line Edit (Input Fields)

**Style:** Bordered, rounded, with focus state

```css
QLineEdit {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-size: 12pt;
}
QLineEdit:focus {
    border: 1px solid #aaa;
}
```

**Dimensions:** 
- Minimum height: 36px
- Flexible width with stretch factor 1

### 4. GroupBox (Section Containers)

**Style:** Bordered sections with titles

```css
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
```

**Content Margins:** 20px all sides

### 5. Progress Bar

**Style:** Bordered, black fill

```css
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
```

**Dimensions:** Minimum height: 36px

### 6. Log Text Area

**Style:** Monospaced, gray background

```css
QTextEdit {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-family: monospace;
    padding: 8px;
    font-size: 12pt;
}
```

**Behavior:** Read-only, scrollable

### 7. Checkbox

**Style:** Standard checkbox with custom text

```css
QCheckBox {
    font-size: 13pt;
}
```

### 8. Label Types

**Form Labels (Bold):**
```css
.label-form {
    font-size: 13pt;
    font-weight: bold;
}
```

**Regular Labels:**
```css
QLabel {
    font-size: 13pt;
}
```

**Bold Log Title:**
```css
.label-log-title {
    font-size: 13pt;
    font-weight: bold;
}
```

---

## Layout Patterns

### 1. Header with Branded Image

**Location:** Top of window  
**Spacing:** 40px top margin from window edge

```python
def create_branded_header(parent):
    """
    Creates branded header with centered logo/header image
    """
    container_frame = QFrame(parent)
    container_frame.setStyleSheet("background-color: white;")
    
    container_layout = QHBoxLayout(container_frame)
    container_layout.setContentsMargins(40, 0, 40, 0)  # Horizontal padding
    
    # Load and center header image
    jpg_path = Path("resources/images/header.jpg")
    if jpg_path.exists():
        pixmap = QPixmap(str(jpg_path))
        header_label = QLabel(parent)
        header_label.setPixmap(pixmap)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("background-color: white;")
        
        container_layout.addStretch(1)
        container_layout.addWidget(header_label)
        container_layout.addStretch(1)
    
    return container_frame
```

### 2. Form Row Pattern

**Standard Layout:** Label (180px) | Input (flexible) | Browse Button (100px) | Show Template (120px)

```python
# Example: Stores CSV Selection
stores_frame = QFrame()
stores_layout = QHBoxLayout(stores_frame)
stores_layout.setContentsMargins(0, 0, 0, 0)

# Label (fixed width)
stores_label = QLabel("Stores CSV File:")
stores_label.setFixedWidth(180)
stores_label.setStyleSheet("font-size: 13pt; font-weight: bold;")
stores_layout.addWidget(stores_label)

# Input (flexible width)
self.stores_entry = QLineEdit()
self.stores_entry.setMinimumHeight(36)
stores_layout.addWidget(self.stores_entry, 1)  # Stretch factor

# Browse Button
browse_btn = QPushButton("Browse...")
browse_btn.setStyleSheet(button_style)
browse_btn.setFixedWidth(100)
stores_layout.addWidget(browse_btn)

# Show Template Button
show_template_btn = QPushButton("Show Template")
show_template_btn.setStyleSheet(button_style)
show_template_btn.setFixedWidth(120)
stores_layout.addWidget(show_template_btn)
```

### 3. Checkbox with Alignment

```python
# Checkbox row with leading spacer
same_folder_frame = QFrame()
same_folder_layout = QHBoxLayout(same_folder_frame)

# Spacer to align with labels above
spacer = QWidget()
spacer.setFixedWidth(180)
same_folder_layout.addWidget(spacer)

# Checkbox
self.same_folder_check = QCheckBox("Use Excel file directory as output")
self.same_folder_check.setStyleSheet("font-size: 13pt;")
same_folder_layout.addWidget(self.same_folder_check)

# Right stretch to align left
same_folder_layout.addStretch()
```

### 4. Centered Info Buttons

```python
# Bottom buttons (centered)
info_buttons_frame = QFrame()
info_buttons_layout = QHBoxLayout(info_buttons_frame)
info_buttons_layout.setContentsMargins(0, 20, 0, 0)

# Left stretch
info_buttons_layout.addStretch(1)

# Button 1
process_btn = QPushButton("Show Process")
process_btn.setStyleSheet(button_style)
process_btn.setFixedWidth(120)
info_buttons_layout.addWidget(process_btn)

# Spacer
spacer = QWidget()
spacer.setFixedWidth(10)
info_buttons_layout.addWidget(spacer)

# Button 2
help_btn = QPushButton("How to Use")
help_btn.setStyleSheet(button_style)
help_btn.setFixedWidth(120)
info_buttons_layout.addWidget(help_btn)

# Right stretch
info_buttons_layout.addStretch(1)
```

### 5. Primary Action Section

```python
# Process Files section
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
processing_layout.setSpacing(20)

# Primary button (full width)
process_frame = QFrame()
process_layout = QHBoxLayout(process_frame)

process_btn = QPushButton("PROCESS FILES")
process_btn.setStyleSheet("""
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
""")
process_layout.addWidget(process_btn)
process_layout.addStretch()  # Push button to left

processing_layout.addWidget(process_frame)
```

---

## Branding Elements

### 1. Application Icon

**Location:** `resources/images/logo.png`  
**Usage:** Window icon, set via `QApplication.setWindowIcon()`

```python
icon_path = Path("resources/images/logo.png")
if icon_path.exists():
    app_icon = QIcon(str(icon_path))
    app.setWindowIcon(app_icon)
```

### 2. Header Image

**Location:** `resources/images/header.jpg`  
**Usage:** Full-width header at top of window  
**Padding:** 40px left and right

```python
# Load header image
jpg_path = Path("resources/images/header.jpg")
if jpg_path.exists():
    pixmap = QPixmap(str(jpg_path))
    header_label = QLabel(parent)
    header_label.setPixmap(pixmap)
    header_label.setAlignment(Qt.AlignCenter)
```

### 3. Window Title

```python
self.setWindowTitle("Philipp Plein Outlet Allocation Tool")
```

---

## Extraction Guide

### Files to Copy for UI Reuse

```
src/ui/
├── main_window.py          # Complete UI implementation
├── utils.py               # UI utilities (image loading, headers)
├── templates.py           # Template dialogs
└── components/            # Reusable components (empty, can be created)

resources/
└── images/
    ├── logo.png          # Application icon
    └── header.jpg        # Header image
```

### Dependencies for UI Only

```python
# Required PySide6 imports
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog,
    QProgressBar, QTextEdit, QGroupBox, QMessageBox, QFrame,
    QApplication
)
from PySide6.QtCore import Qt, QSize, Signal, QObject, Slot
from PySide6.QtGui import QFont, QPixmap, QTextCursor, QIcon
```

### Minimal Working Example

```python
#!/usr/bin/env python
"""Minimal UI extraction example"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import ExcelProcessorApp

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = ExcelProcessorApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### Steps to Extract UI

1. **Copy UI Files:**
   ```bash
   cp src/ui/*.py your_project/ui/
   ```

2. **Copy Resources:**
   ```bash
   cp resources/images/* your_project/assets/
   ```

3. **Update Imports:**
   - Remove `from src.core.processors.file_processor import FileProcessor`
   - Replace with your own processing logic

4. **Update Resource Paths:**
   - Change `resources/images/` to your asset paths
   - Or use relative paths from your project structure

5. **Customize Branding:**
   - Replace `logo.png` with your logo
   - Replace `header.jpg` with your header image
   - Update window title

6. **Remove Business Logic:**
   - Keep all visual components
   - Remove file processing worker
   - Replace with your own logic

### Customization Points

| Element | Current | Customizable |
|---------|---------|--------------|
| Window Size | 1200x1000 | Yes, via `standard_width/height` |
| Header Image | `header.jpg` | Yes, change path in `utils.py` |
| Icon | `logo.png` | Yes, change path in `main_window.py` |
| Colors | Monochrome | Yes, update CSS in methods |
| Font | System font | Yes, update font-family |
| Button Styles | Standard | Yes, modify CSS |
| Spacing | Fixed values | Yes, adjust constants |

### Color Scheme Customization

To change from monochrome to a colored scheme:

```python
# In main_window.py, update:

# Background color
self.central_widget.setStyleSheet("""
    background-color: white;  # Change to your color
    color: black;
    ...
""")

# Button styles
button_style = """
    QPushButton {
        background-color: white;      # Change to your accent color
        color: black;                 # Change to contrast
        border: 1px solid black;      # Change border color
        ...
    }
    QPushButton:hover {
        background-color: black;      # Change to hover color
        color: white;                 # Change to hover text color
    }
"""
```

---

## Complete Style Sheet Reference

### Main Window Styles

```css
/* Central Widget Base Styles */
QWidget {
    background-color: white;
    color: black;
}

/* Form Input Styles */
QLineEdit {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-size: 12pt;
}

QLineEdit:focus {
    border: 1px solid #aaa;
}

/* Label Styles */
QLabel {
    font-size: 13pt;
}

/* Checkbox Styles */
QCheckBox {
    font-size: 12pt;
}

/* GroupBox Styles */
QGroupBox {
    font-size: 16pt;
}

/* Font Family */
* {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
```

### Button Styles

```css
/* Secondary Buttons (Standard) */
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

/* Primary Button (PROCESS FILES) */
QPushButton.primary {
    background-color: black;
    color: white;
    border: none;
    border-radius: 3px;
    padding: 8px 16px;
    font-size: 12pt;
    font-weight: bold;
    text-transform: uppercase;
}

QPushButton.primary:hover {
    background-color: #333;
}

QPushButton.primary:pressed {
    background-color: #555;
}
```

### GroupBox Styles

```css
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
```

### Progress Bar Styles

```css
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
```

### Log Text Area Styles

```css
QTextEdit {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-family: monospace;
    padding: 8px;
    font-size: 12pt;
}
```

---

## Summary

This design system provides:
- **Clean monochrome aesthetic** suitable for professional applications
- **Consistent spacing and typography** throughout
- **Clear visual hierarchy** via borders and grouping
- **Interactive feedback** on all buttons
- **Professional appearance** with minimal color palette
- **Reusable components** that can be extracted easily

**Key Features:**
✅ Professional monochrome design  
✅ Clear visual hierarchy  
✅ Consistent spacing system  
✅ Interactive button states  
✅ Readable typography  
✅ Bordered section grouping  
✅ Centered branding elements  
✅ Complete style documentation  

**Reuse:** All visual design elements are documented and can be extracted for use in other projects with minimal modification.


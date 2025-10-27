# UI Component Extraction Guide
## Quick Reference for Reusing UI in Other Projects

**Purpose:** Extract the visual design and UI components from this project for use in another project without the calculation logic.

---

## Quick Start

### 1. Copy These Files

```bash
# Copy UI modules
cp -r src/ui/ your_project/ui/

# Copy resources
cp -r resources/ your_project/assets/

# Copy style configurations (optional)
cp docs/ui-design-system.md your_project/docs/
```

### 2. Required Files Only

```
your_project/
├── ui/
│   ├── __init__.py
│   ├── main_window.py       # Main UI window
│   ├── utils.py             # UI utilities (header, image loading)
│   └── templates.py         # Template dialogs (optional)
├── assets/
│   ├── images/
│   │   ├── logo.png         # Your application icon
│   │   └── header.jpg       # Your header image
│   └── templates/           # Template files (if needed)
└── your_main.py             # Your entry point
```

### 3. Update Imports

**In main_window.py:**

**REMOVE:**
```python
from src.core.processors.file_processor import FileProcessor
```

**REPLACE with your own:**
```python
from your_project.your_module import YourProcessor
```

**UPDATE:**
```python
# In __init__ method
self.your_processor = YourProcessor()  # Replace FileProcessor()
```

### 4. Update Resource Paths

**In app.py and main_window.py:**

Change:
```python
icon_path = Path("resources/images/logo.png")
```

To:
```python
icon_path = Path("assets/images/logo.png")  # or your path
```

**In utils.py:**

Change:
```python
jpg_path = Path("resources/images/header.jpg")
```

To:
```python
jpg_path = Path("assets/images/header.jpg")  # or your path
```

### 5. Remove/Replace Business Logic

**In main_window.py, REMOVE:**

1. ProcessingWorker class (lines 52-127)
2. FileProcessor integration (line 160)
3. Worker thread handling (lines 745-762)
4. Processing methods (start_processing, update_progress, processing_finished)

**REPLACE with your own:**

```python
def start_processing(self):
    """Start your processing operation"""
    # Your custom processing logic here
    pass
```

### 6. Customize Branding

**Update window title:**
```python
self.setWindowTitle("Your Application Name")
```

**Replace images:**
```bash
# Replace with your images
your_project/assets/images/logo.png    # Your icon
your_project/assets/images/header.jpg  # Your header
```

**Update button text and labels:**
- Change "PROCESS FILES" to your action text
- Update all form labels to your field names
- Modify button text as needed

---

## Minimal Working Example

Create `your_main.py`:

```python
#!/usr/bin/env python
"""Your application entry point"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Import your customized UI
from ui.main_window import ExcelProcessorApp

def main():
    # Initialize PySide6
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set your application icon
    icon_path = Path("assets/images/logo.png")
    if icon_path.exists():
        from PySide6.QtGui import QIcon
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon)
    
    # Create and show window
    window = ExcelProcessorApp()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## What Stays (Visual Design)

✅ **All visual styling** - colors, fonts, spacing  
✅ **Layout structure** - sections, alignment, hierarchy  
✅ **Button styles** - primary and secondary  
✅ **Form elements** - inputs, labels, checkboxes  
✅ **GroupBoxes** - section containers  
✅ **Progress indicators** - progress bar, status labels  
✅ **Log display** - text area styling  
✅ **Spacing system** - margins, padding, gaps  
✅ **Typography** - font sizes, weights  
✅ **Branding elements** - header, icon  

## What Goes (Business Logic)

❌ **FileProcessor class** - replace with your logic  
❌ **ProcessingWorker** - replace with your processing  
❌ **Excel-specific logic** - replace with your data handling  
❌ **Store processing** - replace with your operations  
❌ **Template functionality** - replace with your needs  

---

## Customization Options

### Change Color Scheme

**In main_window.py:**

```python
# Monochrome (current)
button_style = """
    QPushButton {
        background-color: white;
        color: black;
        border: 1px solid black;
        ...
    }
"""

# Colored (custom)
button_style = """
    QPushButton {
        background-color: #4CAF50;    # Your color
        color: white;
        border: 1px solid #45a049;
        ...
    }
"""
```

### Adjust Window Size

```python
# Current
standard_width = 1200
standard_height = 1000

# Custom
standard_width = 1400    # Make it wider
standard_height = 800   # Make it shorter
```

### Change Font Sizes

```python
# Labels (13pt)
stores_label.setStyleSheet("font-size: 13pt; font-weight: bold;")

# Custom (16pt)
stores_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
```

### Modify Spacing

```python
# Current section spacing
content_layout.setSpacing(30)

# Custom
content_layout.setSpacing(50)  # More space
```

---

## Testing Your Extracted UI

1. **Run the minimal example:**
   ```bash
   python your_main.py
   ```

2. **Verify visual elements:**
   - ✅ Window displays correctly
   - ✅ Header image shows
   - ✅ Icon appears in window
   - ✅ Buttons render with correct styles
   - ✅ Forms align properly
   - ✅ Progress bar works
   - ✅ Log area displays

3. **Test interactions:**
   - ✅ Button hovers work
   - ✅ Inputs focus correctly
   - ✅ Forms validate
   - ✅ Dialogs open

---

## Advanced Customization

### Add New Sections

```python
# Add a new GroupBox section
new_section = QGroupBox("New Section")
new_section.setStyleSheet("""
    QGroupBox {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-top: 15px;
        padding: 20px;
        font-size: 16pt;
        font-weight: bold;
    }
""")
content_layout.addWidget(new_section)
```

### Add Custom Buttons

```python
# Custom button with icon
custom_btn = QPushButton("Custom Action")
custom_btn.setIcon(QIcon("path/to/icon.png"))
custom_btn.setStyleSheet(button_style)
custom_btn.clicked.connect(self.custom_action)
```

### Modify Header

```python
# In utils.py, modify create_branded_header()

# Add text below image
title_label = QLabel("Your Application Name")
title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
container_layout.addWidget(title_label)
```

---

## Summary

This guide provides everything needed to extract and reuse the visual design of this Excel processing application in another project.

**Quick Checklist:**
- [ ] Copy `src/ui/*.py` to your project
- [ ] Copy `resources/` to your assets
- [ ] Update import paths
- [ ] Remove business logic (FileProcessor, ProcessingWorker)
- [ ] Replace with your own processing logic
- [ ] Update branding (logo, header, title)
- [ ] Customize colors/fonts if desired
- [ ] Test the UI

**Result:** A professional, clean UI design that you can apply to any PySide6 application!


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple test script to verify PySide6 imports work correctly.
"""

import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    from PySide6.QtWidgets import QApplication, QLabel
    print("Successfully imported PySide6.QtWidgets")
    
    # Create minimal app
    app = QApplication([])
    label = QLabel("PySide6 works!")
    print("Successfully created PySide6 objects")
except Exception as e:
    print(f"Error importing PySide6: {e}") 
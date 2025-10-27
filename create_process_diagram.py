#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a simple process diagram for the Excel Processor application.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Create images directory if it doesn't exist
images_dir = Path("images")
if not images_dir.exists():
    images_dir.mkdir()

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 6))
plt.axis('off')
plt.tight_layout()

# Define colors
box_color = '#f0f0f0'
arrow_color = '#202020'
text_color = 'black'
box_border = '#505050'

# Process steps
steps = [
    "Select Stores CSV File",
    "Select Excel File",
    "Choose Output Directory",
    "Click 'PROCESS FILES'",
    "Review Results"
]

# Define positions
start_y = 4
box_width = 3
box_height = 0.8
h_spacing = 2
v_spacing = 1.2

# Draw the process flow
for i, step in enumerate(steps):
    # Alternate between left and right
    if i % 2 == 0:
        x = 2
        text_align = 'left'
        arrow_dx = h_spacing
        arrow_dy = -v_spacing
    else:
        x = 2 + box_width + h_spacing
        text_align = 'right'
        arrow_dx = -h_spacing
        arrow_dy = -v_spacing
    
    y = start_y - (i // 2) * 2 * v_spacing
    
    # Draw the box
    rect = patches.Rectangle((x, y), box_width, box_height, 
                            linewidth=1, edgecolor=box_border, 
                            facecolor=box_color, zorder=2)
    ax.add_patch(rect)
    
    # Add text
    ax.text(x + box_width/2, y + box_height/2, step, 
           horizontalalignment='center', verticalalignment='center',
           color=text_color, fontsize=12, fontweight='bold')
    
    # Add arrow to next step (except the last)
    if i < len(steps) - 1:
        if i % 2 == 0:  # If on left, arrow goes right then down
            # Horizontal arrow
            ax.arrow(x + box_width, y + box_height/2, 
                    arrow_dx, 0, 
                    head_width=0.1, head_length=0.2, 
                    fc=arrow_color, ec=arrow_color, zorder=1)
            # Vertical arrow
            ax.arrow(x + box_width + h_spacing, y + box_height/2, 
                    0, arrow_dy, 
                    head_width=0.1, head_length=0.2, 
                    fc=arrow_color, ec=arrow_color, zorder=1)
        else:  # If on right, arrow goes left then down
            # Horizontal arrow
            ax.arrow(x, y + box_height/2, 
                    arrow_dx, 0, 
                    head_width=0.1, head_length=0.2, 
                    fc=arrow_color, ec=arrow_color, zorder=1)
            # Vertical arrow
            ax.arrow(x + arrow_dx, y + box_height/2, 
                    0, arrow_dy, 
                    head_width=0.1, head_length=0.2, 
                    fc=arrow_color, ec=arrow_color, zorder=1)

# Add title
plt.title('Excel Processor Workflow', fontsize=16, pad=20)

# Save the figure as PNG with high DPI
plt.savefig('images/process_diagram.png', dpi=300, bbox_inches='tight')
print("Process diagram created successfully at 'images/process_diagram.png'") 
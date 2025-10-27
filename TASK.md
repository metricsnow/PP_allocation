# Open Tasks

manual added
- split large files into smaller parts
- improve layout
- improve "show template" positions
- add show analytics
- ~~move to PySide6 (Qt for Python) from tkinter~~


## Development
- [x] Create Python script to load and work with XLSX files
- [ ] Implement data validation for Excel data
- [x] Add error handling for file operations

## Documentation
- [ ] Complete comprehensive project documentation
- [ ] Add examples and use cases

## Testing
- [ ] Create unit tests for Excel file operations
- [ ] Test error handling scenarios

## Future Enhancements
- [ ] Add visualization capabilities for Excel data
- [x] Implement data export functionality

## UI Improvements & Branding

### Header & Global Style
- [x] Refine branding elements
  - [x] Replace black header with images/header.jpg (full width, fixed height or responsive)
  - [x] Remove subtitle text (e.g. "Outlet Allocation Tool – v1.0") below header
  - [x] Apply monochrome theme: black text, white background
  - [x] Apply consistent font smoothing and padding across all components
  - [x] Set images/logo.png as app icon and favicon

### Layout & Section Grouping
- [x] Improve section structure
  - [x] Wrap each section in a subtle bordered box (light gray 1px border, rounded corners, white inside)
  - [x] Apply consistent padding (~15-20px) inside section boxes
  - [x] Remove "Step 1", "Step 2" labels, keep only section titles like "File Selection"
  - [x] Increase vertical spacing between groups (min. 20px)

### Field Alignment & Button Layout
- [x] Align interface elements consistently
  - [x] Ensure all file path input fields have the same starting point and width
  - [x] Vertically align all "Browse" buttons
  - [x] Move "Show Template" buttons to the right side of "Browse" buttons
  - [x] Apply consistent horizontal spacing and alignment

### Button Styling & Hover Interactions
- [x] Standardize button appearance
  - [x] Style secondary buttons with white background and black border
  - [x] Add hover effect to buttons (black background, white text on hover)
  - [x] Style "Show Process" and "How to Use" buttons like "Show Template" buttons
  - [x] Reduce "Process Files" button height and font size to match general form controls
  - [x] Add rounded corners to buttons (optional)
  - [ ] Add icons to actions (folder, eye, play icons)

### Polish & Usability
- [x] Enhance user experience
  - [x] Maintain consistent spacing between sections (20px+)
  - [x] Ensure even margin between inputs and buttons
  - [x] Add light focus outline to inputs on click (optional)
  - [ ] Add loading spinner during file processing
  - [ ] Display success message upon completion
  - [x] Improve log readability with gray background and monospaced font

### Additional Enhancements
- [ ] Refine copywriting and localization
  - [ ] Simplify and elevate tone (avoid system jargon)
  - [ ] Add tooltips/helper texts to unclear elements

- [ ] Optional features
  - [ ] Add drag & drop file upload zone for CSV/Excel
  - [ ] Implement theme toggle (dark/light)
  - [ ] Add persistent settings to remember last used folder
  - [ ] Create "Clear Log" and "Export Log" buttons

## Code Cleanup
- [x] Consolidate duplicate code between app.py and run allocation.pyw (keep only app.py)
- [x] Remove allocation.pyw as it's redundant (functionality in worker.py)
- [x] Update excel_processor.spec to use app.py instead of run allocation.pyw
- [ ] Ensure proper directory structure with:
  - app.py: Main application entry point
  - worker.py: Core processing logic
  - functions.py: Shared utility functions
  - /images: Application resources
  - /output: Default output directory
  - /source: Template source files
  - /test: Test files and test data

## Completed Today
- [x] Update worker.py to save separate XLSX files for each store
- [x] Improve worker.py to create separate sheets for each SEASON value
- [x] Add functionality to create TXT files with repeated EANCode values based on quantity
- [x] Create GUI application (app.py) for file upload and processing
- [x] Remove redundant .pyw files and update PyInstaller spec file
- [x] Move from tkinter to PySide6 (Qt for Python)
- [x] Implement UI refinements based on Philipp Plein feedback 
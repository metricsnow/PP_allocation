# Reorganization Task: Logical Project Structure

## Current Issues
The project has mixed concerns and unclear organization:
- Legacy `app/ui/` (tkinter) exists alongside modern `app/ui_pyside6/`
- Root-level files scattered (`app.py`, `worker.py`, `functions.py`, etc.)
- Resources mixed with source code
- No clear separation between UI, processing, and data layers

## Proposed New Structure

```
project/
├── src/                           # All source code
│   ├── __init__.py
│   ├── ui/                        # User interface layer
│   │   ├── __init__.py
│   │   ├── main_window.py         # Main GUI window
│   │   ├── components/            # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── file_browser.py    # File selection components
│   │   │   ├── progress_display.py # Progress bars and logs
│   │   │   └── buttons.py         # Custom button widgets
│   │   ├── utils.py               # UI utilities (image loading, etc.)
│   │   └── styles.py              # Style definitions
│   ├── core/                      # Core business logic
│   │   ├── __init__.py
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── excel_processor.py  # Excel file processing
│   │   │   ├── store_processor.py # Store-specific processing
│   │   │   └── file_processor.py   # File handling
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── data_service.py     # Data operations
│   │   │   └── validation_service.py # Data validation
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_utils.py       # File utilities (from functions.py)
│   │       └── logger.py           # Logging configuration
│   └── cli/                       # CLI interface
│       ├── __init__.py
│       └── worker.py              # CLI worker (from worker.py)
├── docs/                          # Documentation
│   ├── user_guide.txt            # User guide
│   ├── api/                      # API documentation
│   └── architecture/             # Architecture docs
├── tests/                        # Test files
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_processors.py
│   │   └── test_utils.py
│   └── integration/
│       └── test_workflow.py
├── resources/                     # Static resources
│   ├── images/
│   │   ├── logo.png
│   │   └── header.jpg
│   └── templates/
│       ├── stores_template.csv
│       └── excel_template.xlsx
├── data/                         # Data directories (gitignored)
│   ├── source/                   # Input Excel files
│   ├── stores/                   # Store CSV files
│   └── output/                   # Generated output files
│
├── app.py                         # GUI entry point (thin wrapper)
├── worker.py                      # CLI entry point (thin wrapper)
├── requirements.txt               # Dependencies
├── README.md                      # Project readme
└── .gitignore                     # Git ignore rules
```

## Clean Project Root Principles

**ONLY these files should be in project root:**
- `app.py` - GUI entry point
- `worker.py` - CLI entry point  
- `requirements.txt` - Dependencies
- `README.md` - Project documentation
- `.gitignore` - Git configuration

**Everything else goes into logical subdirectories:**
- All source code → `src/`
- All documentation → `docs/`
- All resources → `resources/`
- All tests → `tests/`
- All generated data → `data/`

## Migration Plan

### Phase 1: Create New Structure
1. Create new directories: `src/`, `src/ui/`, `src/core/`, etc.
2. Move resources to `resources/`
3. Move docs to `docs/`
4. Create `config/` directory

### Phase 2: Consolidate UI
1. Move `app/ui_pyside6/` → `src/ui/`
2. Remove `app/ui/` (legacy tkinter)
3. Update imports in UI files
4. Organize UI components

### Phase 3: Organize Core Logic
1. Split `functions.py` → `src/core/utils/file_utils.py`
2. Move `app/processors/` → `src/core/processors/`
3. Update imports in all files
4. Create `src/core/utils/logger.py`

### Phase 4: CLI Reorganization
1. Move `worker.py` → `src/cli/worker.py`
2. Update imports
3. Keep root-level `worker.py` as thin entry point

### Phase 5: Update Imports
1. Update all import statements throughout codebase
2. Add `__init__.py` files
3. Test all imports

### Phase 6: Cleanup
1. Remove old directories
2. Update README and docs
3. Update .gitignore for `data/` directory
4. Test application

## File Mapping

### UI Layer
```
OLD                                    NEW
app/ui_pyside6/main_window.py    →    src/ui/main_window.py
app/ui_pyside6/utils.py          →    src/ui/utils.py
app/ui_pyside6/templates.py      →    src/ui/templates.py
app/ui/ (REMOVE - legacy)        →    (deleted)
```

### Core Logic
```
OLD                                    NEW
functions.py                     →    src/core/utils/file_utils.py
app/processors/file_processor.py →    src/core/processors/file_processor.py
app/processors/store_processor.py →    src/core/processors/store_processor.py
```

### CLI
```
OLD                                    NEW
worker.py                        →    src/cli/worker.py
```

### Resources
```
OLD                                    NEW
images/                          →    resources/images/
template_files/                  →    resources/templates/
```

### Data
```
OLD                                    NEW
(output, source, stores - created at runtime)
                               →    data/source/
                                     data/stores/
                                     data/output/
```

## Import Changes

### Before
```python
from app.ui_pyside6.main_window import ExcelProcessorApp
from app.processors.file_processor import FileProcessor
from functions import load_xlsx_file
```

### After
```python
from src.ui.main_window import ExcelProcessorApp
from src.core.processors.file_processor import FileProcessor
from src.core.utils.file_utils import load_xlsx_file
```

## Benefits

1. **Clear Separation of Concerns**
   - UI logic in `src/ui/`
   - Business logic in `src/core/`
   - CLI in `src/cli/`

2. **Better Organization**
   - All source code in `src/`
   - Resources separated from code
   - Documentation centralized

3. **Scalability**
   - Easy to add new processors
   - Components can be tested independently
   - Clear module boundaries

4. **Maintainability**
   - Easier to find code
   - Reduced coupling
   - Better imports

5. **Professional Structure**
   - Follows Python best practices
   - Industry-standard layout
   - Easy onboarding for new developers

## Risk Mitigation

1. **Incremental Migration**: Move files step by step
2. **Test After Each Step**: Verify application works
3. **Keep Backups**: Git commits after each phase
4. **Update Imports Gradually**: Update as we move files
5. **Document Changes**: Update README at each step

## Next Steps

1. Create new directory structure
2. Move files according to plan
3. Update imports
4. Remove old directories
5. Test thoroughly
6. Update documentation

---

**Status**: Planned
**Priority**: High
**Estimated Time**: 2-3 hours
**Risk**: Medium (requires careful import updates)


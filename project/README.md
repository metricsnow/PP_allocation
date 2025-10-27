# Excel File Processor

A Python utility for loading and working with Excel (XLSX) files.

## Getting Started

### Prerequisites
- Python 3.x installed on your system
- Git (optional, for cloning the repository)

### Installation

1. Clone or download this repository
```
git clone <repository-url>
```

2. Navigate to the project directory
```
cd <project-directory>
```

3. Create the virtual environment
```
python -m venv venv_plein
```

4. Activate the virtual environment

On Windows:
```
venv_plein\Scripts\activate
```

On macOS/Linux:
```
source venv_plein/bin/activate
```

5. Install required packages
```
pip install -r requirements.txt
```
Or install them directly:
```
pip install openpyxl pandas
```

### Running the Application

1. Make sure your Excel file is located in the project directory or provide the full path

2. Run the worker script:
```
python worker.py <path-to-excel-file>
```

3. Follow any on-screen prompts or instructions

## Features

- Load and read Excel (XLSX) files
- Process data from spreadsheets
- Safe error handling for file operations

## Project Structure

- `worker.py`: Main script for Excel file operations
- `TASK.md`: List of open tasks and features to be implemented
- `TASK_DONE.md`: List of completed tasks
- `DOCS.md`: Detailed project documentation
- `requirements.txt`: List of dependencies

## Troubleshooting

If you encounter issues:
1. Ensure your Excel file is not corrupted
2. Verify that the virtual environment is activated
3. Check that all dependencies are installed correctly

## Further Documentation

For more detailed information about the project, refer to `DOCS.md`. 
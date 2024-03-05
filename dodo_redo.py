import sys
from pathlib import Path

base_directory = Path(__file__).parent
src_directory = base_directory / 'src'

sys.path.insert(0, str(src_directory))

import config
from doit.tools import run_once, create_folder

DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)

def task_pull_wrds():
    """Pull data from WRDS if it doesn't already exist."""
    def check_files():
        return (DATA_DIR / "pulled" / "13f.parquet").exists() and \
               (DATA_DIR / "pulled" / "Mutual_Fund.parquet").exists()

    return {
        'actions': ['python src/pull_wrds.py'],
        'targets': [DATA_DIR / "pulled" / "13f.parquet", DATA_DIR / "pulled" / "Mutual_Fund.parquet"],
        'uptodate': [check_files],
        'clean': True,
        'task_dep': ['create_folders'],
    }

def task_create_folders():
    """Create necessary folders."""
    return {
        'actions': [(create_folder, [DATA_DIR / 'pulled'])],
        'targets': [DATA_DIR / 'pulled'],
        'uptodate': [True],  # Create folder only if it doesn't exist
        'clean': True,
    }

def task_construct_full_report():
    """Construct the full LaTeX report after ensuring WRDS data is available."""
    return {
        'actions': ['python src/construct_full_report.py'],
        'file_dep': [DATA_DIR / "pulled" / "13f.parquet", DATA_DIR / "pulled" / "Mutual_Fund.parquet"],
        'targets': [Path(config.OUTPUT_DIR) / "full_report.tex"],
        'task_dep': ['pull_wrds'],  # This task depends on `task_pull_wrds`
        'clean': True,
    }

def task_tex_to_pdf():
    """Compile the TeX file to PDF using the tex_to_pdf.py script."""
    return {
        'actions': ['python src/tex_to_pdf.py full_report.tex'], 
        'file_dep': [OUTPUT_DIR / 'full_report.tex'], 
        'targets': [OUTPUT_DIR / 'full_report.pdf'], 
        'clean': True,
    }
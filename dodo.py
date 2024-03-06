import sys
from pathlib import Path

base_directory = Path(__file__).parent
src_directory = base_directory / 'src'

sys.path.insert(0, str(src_directory))

import config
from doit.tools import run_once, create_folder

DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)

def task_pull_13f():
    """Pull 13f data from WRDS if it doesn't already exist.
    Outputs:
        parquets: 13f in DATA_DIR
    """
    def check_files():
        return (DATA_DIR / "pulled" / "13f.parquet").exists()

    return {
        'actions': ['python src/pull_13f.py'],
        'targets': [DATA_DIR / "pulled" / "13f.parquet"],
        'uptodate': [check_files],
        'clean': True,
        'task_dep': ['create_folders'],
    }

def task_pull_mf():
    """Pull mutual fund data from WRDS if it doesn't already exist.
    Outputs:
        parquets: Mutual_Fund in DATA_DIR
    """
    def check_files():
        return (DATA_DIR / "pulled" / "Mutual_Fund.parquet").exists()

    return {
        'actions': ['python src/pull_mf.py'],
        'targets': [DATA_DIR / "pulled" / "Mutual_Fund.parquet"],
        'uptodate': [check_files],
        'clean': True,
        'task_dep': ['create_folders'],
    }

def task_create_folders():
    """Create necessary folders.
    Outputs:
        Create folder for pulled dat
    """
    return {
        'actions': [(create_folder, [DATA_DIR / 'pulled'])],
        'targets': [DATA_DIR / 'pulled'],
        'uptodate': [True],  # Create folder only if it doesn't exist
        'clean': True,
    }

def task_construct_full_report():
    """Construct the full LaTeX report after ensuring WRDS data is available.
    Outputs:
        LaTex Report in Output DIR
    """
    return {
        'actions': ['python src/construct_full_report.py'],
        'file_dep': [DATA_DIR / "pulled" / "13f.parquet", DATA_DIR / "pulled" / "Mutual_Fund.parquet"],
        'targets': [Path(config.OUTPUT_DIR) / "full_report.tex"],
        'task_dep': ['pull_13f', 'pull_mf'],  # This task depends on `task_pull_13f and task_pull_mf`
        'clean': True,
    }

def task_compile_latex_docs():
    """Compile the LaTex documents to PDFs
    Outputs:
        PDFs in Reports
    """
    file_dep = [
        "./output/full_report.tex",
    ]
    targets = ["./reports/full_report.pdf",]

    return {
        "actions": [
            "latexmk -xelatex -cd -outdir=../reports ./output/full_report.tex",  # Compile
            "latexmk -xelatex -c -cd -outdir=../reports ./output/full_report.tex",  # Clean
        ],
        "targets": targets,
        "file_dep": file_dep,
        "clean": True,
    }

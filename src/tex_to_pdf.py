"""
Compiles the TeX file to PDF, in outputs
"""
from pdflatex import PDFLaTeX
from pathlib import Path
import config
import os

output_dir = Path(config.OUTPUT_DIR)

def generate_pdf_from_tex(tex_file_name):
    """
    Generates a PDF from a given TeX file. In this case it specifically works only for TeX files in the output directory.
    
    Parameters:
    - tex_file_name (str): The name of the TeX file, assumed to be in the output directory
    """
    tex_file_path = output_dir / tex_file_name
    
    if not tex_file_path.exists():
        print(f"Error: The file {tex_file_name} does not exist in {output_dir}.")
        return
    
    current_dir = Path.cwd()
    
    try:
        os.chdir(output_dir)
        pdfl = PDFLaTeX.from_texfile(str(tex_file_path))
        pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
        print(f"PDF generated successfully: {tex_file_path.with_suffix('.pdf')}")
    except Exception as e:
        print(f"An error occurred during PDF generation: {e}")
    finally:
        os.chdir(current_dir)



#generate_pdf_from_tex('full_report.tex')
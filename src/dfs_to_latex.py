"""
Produces a LaTeX table from the completed dataframe.

"""

import config
from pathlib import Path
from construct_stats import plot_stats_data, construct_stats

DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)

def generate_latex_table_body(df):
    """
    Generates the LaTeX table body for a given DataFrame
    """
    type_dict = {
        1.0: 'A. Banks',
        2.0: 'B. Insurance companies',
        3.0: 'C. Investment advisors',
        4.0: 'D. Mutual funds',
        5.0: 'E. Pension funds',
        6.0: 'E. Other'
    }

    body = ""
    for type_index, type_value in type_dict.items():
        body += f"& \\multicolumn{{10}}{{c}}{{{type_value}}}\\\\ \\cline{{2-11}} \n"
        if type_index in df.index:
            row = df.loc[type_index]
            body += f"& {row['number']} & {row['market_held']} & {row['AUM_median']} & {row['AUM_90']} & & {row['stocks_median']} & {row['stocks_90']} & & {row['universe_median']} & {row['universe_90']} \\\\\n"
        body += "    \\cline{2-11}\n"
    return body

def markdown_to_latex(md_path):
    """
    Reads a Markdown file and converts it to LaTeX format with specific replacements for our document
    """
    with open(md_path, 'r') as file:
        md_content = file.read()
    md_content = md_content.replace('# ', '\\section*{').replace('\n', '}\n')
    md_content = md_content.replace('## ', '\\subsection*{').replace('\n', '}\n')
    md_content = md_content.replace('===========================================================================\n',
                                    '\\noindent\\makebox[\\linewidth]{\\rule{\\paperwidth}{0.4pt}}\n')
    return md_content

def df_to_latex_with_md_and_plots(dfs, md_path, output):
    """
    Combines the content of a Markdown file, LaTeX tables from multiple DataFrames, and plots into a single .tex file
    """
    start = r"""\documentclass{article}
    \usepackage{caption}
    \usepackage[top=0.75in, left=1in,right=1in]{geometry}
    \usepackage{graphicx}
    \begin{document}"""
    
    md_latex = markdown_to_latex(md_path)
    full_latex = start + "\n" + md_latex + "\n\\newpage\n"
    
    for df in dfs:
        table_body = generate_latex_table_body(df)
        full_latex += table_body + "\n\\newpage\n"
        
        type_counts_df, aum_df, mgrs_df = construct_stats(df)
        plot_files = [
            plot_stats_data(type_counts_df, 'Count', 'Institution Type Counts Over Time', f'type_counts_{dfs.index(df)}.png'),
            plot_stats_data(aum_df, 'AUM', 'AUM Over Time', f'aum_{dfs.index(df)}.png', True),
            plot_stats_data(mgrs_df, 'UniqueMgrCounts', 'Managers Over Time', f'mgrs_{dfs.index(df)}.png')
        ]
        
        for plot_file in plot_files:
            full_latex += f"\\includegraphics[width=\\textwidth]{{{plot_file}}}\n\\newpage\n"

    end = r"\end{document}"
    full_latex += end
    
    path = OUTPUT_DIR / output
    with open(path, "w") as text_file:
        text_file.write(full_latex)

# md_path = 'path.md' 
# output_file = 'full_report.tex'
# dfs = [df1, df2, df3] etc
# df_to_latex_with_md_and_plots(dfs, md_path, output_file)

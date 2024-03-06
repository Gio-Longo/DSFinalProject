"""
Produces a .tex file including write-up, tables, and graphs

"""

import config
from pathlib import Path
from construct_stats import plot_stats_data, construct_stats

DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)

def generate_latex_string(dfs):
    """
    Inserts the dataframe data into the preconstructed LaTeX table layout
    """
    start = r"""\begin{table}
        \caption*{Table D1\\
        Summary of 13F Institutions by Type}
        \centering
        \resizebox{0.90\textwidth}{!}{
        \begin{tabular}{ccccccccccc}
            \hline
            &    &    & \multicolumn{2}{c}{Assets under} &  & \multicolumn{2}{c}{}  &  & \multicolumn{2}{c}{Number of stocks}\\
            &    &    & \multicolumn{2}{c}{management}   &  & \multicolumn{2}{c}{Number of} &  & \multicolumn{2}{c}{in investment}\\
            &    & \% of  & \multicolumn{2}{c}{(\$ million)} &  & \multicolumn{2}{c}{stocks held} &  & \multicolumn{2}{c}{universe}\\ 
            \cline{4-5} \cline{7-8} \cline{10-11} 
            & Number of & market &  & 90th &  &  & 90th &  &  & 90th \\
            Period & institutions & held & median & percentile &  & median & percentile &  & median & percentile \\ 
            \hline"""
    end = r"""
        \hline
        \end{tabular}}
        \end{table}"""

    type_dict = {
    1.0: 'A. Banks',
    2.0: 'B. Insurance companies',
    3.0: 'C. Investment advisors',
    4.0: 'D. Mutual funds',
    5.0: 'E. Pension funds',
    6.0: 'F. Other'}

    body = ""
    for type_index, type_value in type_dict.items():
        body += f"& \\multicolumn{{10}}{{c}}{{{type_value}}}\\\\ \\cline{{2-11}} \n"
        for period, df in dfs.items():
            period_str = f"{period[0][:4]}-{period[1][:4]}"
            if type_index in df.index:
                row = df.loc[type_index]
                body += f"{period_str} & {row['number']} & {row['market_held']} & {row['AUM_median']} & {row['AUM_90']} &  & {row['stocks_median']} & {row['stocks_90']} &  & {row['universe_median']} & {row['universe_90']} \\\\\n"
            else:
                body += f"{period_str} & 0 & 0 & 0 & 0 &  & 0 & 0 &  & 0 & 0 \\\\\n"
        body += "    \\cline{2-11}\n"

    return start+body+end


def markdown_to_latex(md_path):
    """
    Reads a Markdown file and converts it to LaTeX format.
    - Bullet points are converted to LaTeX itemize lists.
    - Markdown italics to LaTeX italics.
    - '---' to LaTeX horizontal line replacement.
    - Ensures text paragraphs are separated and headers are properly formatted.
    """
    with open(md_path, 'r') as file:
        md_lines = file.readlines()

    latex_lines = []
    in_itemize = False  

    for line in md_lines:
        if line.startswith('# '):
            _close_itemize_if_needed(latex_lines, in_itemize)
            in_itemize = False
            latex_lines.append('\\section*{' + _convert_italics(line[2:]) + '}')

        elif line.startswith('## '):
            _close_itemize_if_needed(latex_lines, in_itemize)
            in_itemize = False
            latex_lines.append('\\subsection*{' + _convert_italics(line[3:]) + '}')

        elif line.startswith('### '):
            _close_itemize_if_needed(latex_lines, in_itemize)
            in_itemize = False
            latex_lines.append('\\subsubsection*{' + _convert_italics(line[4:]) + '}')

        elif line.startswith('- '):
            if not in_itemize:
                latex_lines.append('\\begin{itemize}')
                in_itemize = True
            latex_lines.append('    \\item ' + _convert_italics(line[2:]))

        elif '---' in line:
            _close_itemize_if_needed(latex_lines, in_itemize)
            in_itemize = False
            latex_lines.append('\\noindent\\rule{\\linewidth}{0.4pt}')

        elif line.strip():  
            if in_itemize:
                latex_lines.append('\\end{itemize}')
                in_itemize = False
            latex_lines.append(_convert_italics(line) + '\n')

        else:  
            _close_itemize_if_needed(latex_lines, in_itemize)
            in_itemize = False
            latex_lines.append('')  

    _close_itemize_if_needed(latex_lines, in_itemize)

    return '\n'.join(latex_lines)

def _convert_italics(text):
    """
    Convert Markdown italics to LaTeX italics.
    """
    import re
    return re.sub(r'(\*|_)(.*?)\1', r'\\textit{\2}', text)

def _close_itemize_if_needed(latex_lines, in_itemize):
    """
    Close an open itemize environment if needed.
    """
    if in_itemize:
        latex_lines.append('\\end{itemize}\n')
        
def gen_bib():
    bib_entry = """
    @article{koijen2019demand,
    title={A demand system approach to asset pricing},
    author={Koijen, Ralph SJ and Yogo, Motohiro},
    journal={Journal of Political Economy},
    volume={127},
    number={4},
    pages={1475--1515},
    year={2019},
    publisher={The University of Chicago Press Chicago, IL}
    }
    """

    with open(OUTPUT_DIR / "paper.bib", "w") as file:
        file.write(bib_entry)

def df_to_latex_with_md_and_plots(df_old, df_new, plot_files, md_path, output):
    """
    Combines the content of a Markdown file, LaTeX tables from multiple DataFrames, and plots into a single .tex file
    """

    gen_bib()

    start = r"""\documentclass{article}
    \usepackage{caption}
    \usepackage[top=0.75in, left=1in,right=1in]{geometry}
    \usepackage{graphicx}
    \begin{document}"""
    
    md_latex = markdown_to_latex(md_path).replace(r"Asset Pricing}", r"Asset Pricing}\cite{koijen2019demand}")
    full_latex = start + "\n" + md_latex + "\n\\newpage\n"
    
    for df in [df_old, df_new]:
        table_body = generate_latex_string(df)
        full_latex += table_body + "\n\\clearpage\n"
        
    graph_headlines = [
        "Figure 1. Average AUM over Time",
        "Figure 2. Total AUM by Institution Type over Time",
        "Figure 3. Number of Unique Managers over Time"
    ]

    graph_captions = [
        "The average AUM held by each institution is mostly on an uptrend except for Banks. We see a drastic decrease in average AUM held by Banks during the 2008 crisis, which makes sense given the circumstances. ",
        "We see that all fund types have an increase in their AUM compared to the beginning of the period. However, we see that the greatest increases to AUM occur for Mutual Funds and Investment Advisors.",
        "The number of unique managers varies drastically by institution type. We see a lot more managers involved with Banks to start, but this number decreases rapidly (similarly with Insurance). The other three investment types see the opposite trend, starting with less managers and increasing over time."
    ]
    
    for i, plot_file in enumerate(plot_files):
        full_latex += f"""\\section*{{{graph_headlines[i]}}}\n"""
        full_latex += r"\begin{figure}[h]\centering"
        full_latex += f"""\\includegraphics[width=\\textwidth]{{{plot_file}}}\n"""
        full_latex += r"\c" + f"""aption{{{graph_captions[i]}}}\n""" + r"\end{figure}\\newpage\n"

    end = r"\bibliographystyle{plain}\bibliography{paper.bib}\end{document}"
    full_latex += end
    
    path = OUTPUT_DIR / output
    with open(path, "w") as text_file:
        text_file.write(full_latex)
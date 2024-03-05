"""
Produces a LaTeX table from the completed dataframe.

"""

import config
from pathlib import Path
from nbconvert import LaTeXExporter
import nbformat
from construct_stats import plot_stats_data, construct_stats


DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)

def generate_latex_string(dfs):
  """
  Inserts the dataframe data into the preconstructed LaTeX table layout
  """
  start = r"""\documentclass{article}
    \usepackage{caption}
    \usepackage[top=0.75in, left=1in,right=1in]{geometry}
    \begin{document}
    \begin{table}
    \caption*{Table D1\\
    Summary of 13F Institutions by Type}
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
    \end{tabular}
    \end{table}
    \end{document}"""

  type_dict = {
  1.0: 'A. Banks',
  2.0: 'B. Insurance companies',
  3.0: 'C. Investment advisors',
  4.0: 'D. Mutual funds',
  5.0: 'E. Pension funds',
  6.0: 'E. Other'}

  body = ""
  for type_index, type_value in type_dict.items():
      body += f"& \\multicolumn{{10}}{{c}}{{{type_value}}}\\\\ \\cline{{2-11}} \n"
      for period, df in dfs.items():
          period_str = f"{period[0][:4]}-{period[1][:4]}"
          if type_index in df.index:
              row = df.loc[type_index]
              body += f"{period_str} & {row['number']} & {row['market_held']} & {row['AUM_median']} & {row['AUM_90']} &  & {row['stocks_median']} & {row['stocks_90']} &  & {row['universe_median']} & {row['universe_90']} \\\\\n"
      body += "    \\cline{2-11}\n"

  return start+body+end


def notebook_to_latex(notebook_path):
    """
    Converts a notebook (.ipynb) to a LaTeX string
    """
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    latex_exporter = LaTeXExporter()
    latex_exporter.template_name = 'classic'

    (body, resources) = latex_exporter.from_notebook_node(nb)
    return body


def markdown_to_latex(md_path):
    """
    Reads a Markdown file and converts it to LaTeX format with specific replacements (for our markdown)
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
    Combines the content of a Markdown file, LaTeX tables from multiple DataFrames, and plots into a single .tex file.
    """
    md_latex = markdown_to_latex(md_path)

    full_latex = md_latex + "\n\\newpage\n"

    for df in dfs:
        # Generate the LaTeX table for the current DataFrame
        table_latex = generate_latex_string(df)
        full_latex += table_latex + "\n\\newpage\n"

        type_counts_df, aum_df, mgrs_df = construct_stats(df)
        plot_files = [
            plot_stats_data(type_counts_df, 'Count', 'Institution Type Counts Over Time', f'type_counts_{dfs.index(df)}.png'),
            plot_stats_data(aum_df, 'AUM', 'AUM Over Time', f'aum_{dfs.index(df)}.png', True),
            plot_stats_data(mgrs_df, 'UniqueMgrCounts', 'Managers Over Time', f'mgrs_{dfs.index(df)}.png')
        ]

        for plot_file in plot_files:
            full_latex += f"\\includegraphics[width=\\textwidth]{{{plot_file}}}\n\\newpage\n"

    path = OUTPUT_DIR / output
    with open(path, "w") as text_file:
        text_file.write(full_latex)

#md_path = 'your_markdown_file.md'  # Update this path as needed
#output_file = 'combined_output.tex'
#dfs = [df1, df2, df3]  # Replace df1, df2, df3 with your actual DataFrame variables
#df_to_latex_with_md_and_plots(dfs, md_path, output_file)

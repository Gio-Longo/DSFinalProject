import config
from pathlib import Path
DATA_DIR = Path(config.DATA_DIR)
OUTPUT_DIR = Path(config.OUTPUT_DIR)

def generate_latex_string(dfs):
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
  5.0: 'E. Pension funds'}

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

def gen_tex(dfs):
    doc_string = generate_latex_string(dfs)
    path = OUTPUT_DIR / f'table_doc.tex'
    with open(path, "w") as text_file:
        text_file.write(doc_string)
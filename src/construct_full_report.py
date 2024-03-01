from clean_data import *
from df_constructor import *
from dfs_to_latex import *

def construct_full_report():
    df = clean_data()
    dfs = construct_dfs(df)
    df_to_latex(dfs, "full_report.tex")
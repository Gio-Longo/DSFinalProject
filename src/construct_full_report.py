from clean_data import *
from df_constructor import *
from dfs_to_latex import *

def construct_full_report():
    df = clean_data()
    dfs_old, dfs_new = construct_dfs(df)
    dfs_stats = construct_stats(df)

    df_to_latex(dfs_old, dfs_new, dfs_stats, "full_report.tex")
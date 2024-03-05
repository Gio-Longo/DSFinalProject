"""
Constructs the LaTeX report with the finished table.
"""

from pathlib import Path
import config
from clean_data import *
from df_constructor import *
from construct_stats import *
from dfs_to_latex import *


periods_old = [('1980-01-01','1984-12-31'),
               ('1985-01-01','1989-12-31'),
               ('1990-01-01','1994-12-31'),
               ('1995-01-01','1999-12-31'),
               ('2000-01-01','2004-12-31'),
               ('2005-01-01','2009-12-31'),
               ('2010-01-01','2014-12-31'),
               ('2015-01-01','2017-12-31')]

periods_new = [('2018-01-01','2022-12-31'),
               ('2023-01-01','2023-12-31')]

range_old = ('1980-01-01','2017-12-31')
range_new = ('2018-01-01','2023-12-31')


def construct_full_report():
    """
    Generates the full LaTeX report, including data tables and plots
    """
    df_old = clean_data(range_old)
    df_new = clean_data(range_new)
    dfs_old = build_DFs(df_old, periods_old)
    dfs_new = build_DFs(df_new, periods_new)

    type_counts_df, aum_df, mgrs_df = construct_stats(df_old)
    plot_stats_data(type_counts_df, 'Count', 'Institution Type Counts Over Time', 'type_counts.png'),
    plot_stats_data(aum_df, 'AUM', 'AUM Over Time', 'aum.png', True),
    plot_stats_data(mgrs_df, 'UniqueMgrCounts', 'Managers Over Time', 'mgrs.png')

    md_path = Path("../README.md")

    df_to_latex_with_md_and_plots(df_old, df_new, ['type_counts.png', 'aum.png', 'mgrs.png'], md_path, "full_report.tex")

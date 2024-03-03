"""
Unit tests to confirm correct table construction
"""

import config
import os

from clean_data import *
from df_constructor import *
from dfs_to_latex import *

DATA_DIR = config.DATA_DIR
OUTPUT_DIR = config.OUTPUT_DIR

dfs_old = build_DFs.dfs_old
dfs_new = build_DFs.dfs_new

def old_df_test_values_match():
    assert dfs_old.shape[0] == # Number of Rows in the old data table
    assert dfs_old.shape[1] == # Number of Columns in the old data table 
    assert dfs_old[0][0] == # Row 1, Column 1 of the old data table

def new_df_test_values_match():
    assert dfs_new.shape[0] == # Number of Rows in the new data table
    assert dfs_new.shape[1] == # Number of Columns in the new data table
    assert dfs_new[0][0] == # Row 1, Column 1 of the new data table


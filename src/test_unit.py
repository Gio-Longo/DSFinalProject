import os
import re
import pandas as pd
from pathlib import Path
from clean_data import clean_data  
import config

#tex_file_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'full_report.tex')
tex_file_path = config.OUTPUT_DIR / 'full_report.tex'
#data_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'data', 'pulled'))
data_dir = config.DATA_DIR / 'pulled'

test_period = config.UNITTEST_PERIOD

# Tests for .tex file
def test_tex_file_exists():
    assert os.path.isfile(tex_file_path), f"{tex_file_path} does not exist"

def test_pension_funds_empty():
    with open(tex_file_path, 'r') as file:
        content = file.read()
        pension_funds_section = re.findall(r'\\multicolumn{10}{c}{E. Pension funds}.*?\\cline{2-11}\s*\\cline{2-11}', content, re.DOTALL)
        assert pension_funds_section, "Pension funds section not found"
        assert len(pension_funds_section[0].strip().split('\n')) == 2, "Pension funds section is not empty"

def test_table_headers_exist():
    expected_headers = ['Period', 'Number of institutions', 'Assets under management', 'Number of stocks']
    with open(tex_file_path, 'r') as file:
        content = file.read()
        for header in expected_headers:
            assert header in content, f"Header '{header}' not found in the table"

def test_investment_advisors_data_present():
    with open(tex_file_path, 'r') as file:
        content = file.read()
        investment_advisors_section = re.findall(r'\\multicolumn{10}{c}{C. Investment advisors}.*?\\cline{2-11}', content, re.DOTALL)
        assert investment_advisors_section, "Investment advisors section not found"
        assert len(investment_advisors_section[0].strip().split('\n')) > 2, "Investment advisors section is unexpectedly empty"

def test_clean_data_no_nulls():
    df_cleaned = clean_data(test_period, data_dir)
    assert not df_cleaned['prc'].isnull().any(), "'prc' column contains null values"
    assert not df_cleaned['shrout1'].isnull().any(), "'shrout1' column contains null values"

def test_clean_data_types():
    df_cleaned = clean_data(test_period, data_dir)
    expected_dtypes = {
        'fdate': 'datetime64[ns]',
        'mgrno': 'object',
        'mgrname': 'object',
        'typecode': 'float64',
        'cusip': 'object',
        'shares': 'float64',
        'prc': 'float64',
        'shrout1': 'float64'
    }

    for column, expected_dtype in expected_dtypes.items():
        assert df_cleaned[column].dtype == expected_dtype, f"Column '{column}' does not have expected dtype '{expected_dtype}'"

def test_typecodes_filtered_correctly():
    df_cleaned = clean_data(test_period, data_dir)
    allowed_typecodes = [1, 2, 3, 4, 5, 6]
    assert df_cleaned['typecode'].isin(allowed_typecodes).all(), "Typecodes not filtered correctly"

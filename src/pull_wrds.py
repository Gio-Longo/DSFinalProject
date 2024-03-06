"""
Module for fetching and storing data from WRDS

- 13F data retrieval, using docs from https://wrds-www.wharton.upenn.edu/data-dictionary/tr_13f/s34/
- mutual fund mappings for 300 mutual funds, not described under categories in 13F.
"""


import pandas as pd

import numpy as np
import wrds

import config
from pathlib import Path

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME


def pull_13f(wrds_username=WRDS_USERNAME, start_date = '03/31/1980', end_date = '12/31/2024'):
    """
    Pulls certain columns from the 13F dataset
    Selects during the SQL query for prc, shrout1 existing
    Does not select stkcd, exchcd due to changes in the database (ie. exchcd changes)
    """

    my_params = {'start_date':start_date, 'end_date': end_date}

    sql_query = """
        SELECT 
            a.fdate, a.mgrno, a.mgrname,  a.typecode, a.cusip, a.shares, a.prc, a.shrout1, a.stkcd, a.exchcd

        FROM 
            tr_13f.s34 AS a
        WHERE 
            a.fdate BETWEEN  %(start_date)s AND %(end_date)s
            AND a.prc IS NOT NULL 
            AND a.shrout1 IS NOT NULL
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df_13f = db.raw_sql(sql_query, params = my_params, date_cols=["fdate"])
    db.close()

    return df_13f

def pull_mf_mapping(wrds_username=WRDS_USERNAME, start_date = '03/31/1980', end_date = '12/31/2024'):
    """
    Pulls a list of mutual funds (via WRDS) to check against (13F does not hold this distinction)
    """

    my_params = {'start_date':start_date, 'end_date': end_date}

    sql_query = """
        SELECT a.fdate, a.mgrcocd
        FROM 
            tr_mutualfunds.S12TYPE5 AS a
        WHERE 
            a.fdate BETWEEN %(start_date)s AND %(end_date)s
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df_mf = db.raw_sql(sql_query, params = my_params, date_cols=["fdate"])
    db.close()

    return df_mf

def load_13f(data_dir=DATA_DIR):
    """
    Loads saved 13F data
    """
    path = Path(data_dir) / "pulled" / "13f.parquet"
    df_13f = pd.read_parquet(path)
    return df_13f


def load_Mutual_Fund(data_dir=DATA_DIR):
    """
    Loads saved MF data
    """
    path = Path(data_dir) / "pulled" / "Mutual_Fund.parquet"
    df_mf = pd.read_parquet(path)
    return df_mf

def _demo():
    comp = load_13f(data_dir=DATA_DIR)
    crsp = load_Mutual_Fund(data_dir=DATA_DIR)

if __name__ == "__main__":
    Path(DATA_DIR / "pulled").mkdir(parents=True, exist_ok=True)

    comp = pull_13f(wrds_username=WRDS_USERNAME)
    comp.to_parquet(DATA_DIR / "pulled" / "13f.parquet")

    crsp = pull_mf_mapping(wrds_username=WRDS_USERNAME)
    crsp.to_parquet(DATA_DIR / "pulled" / "Mutual_Fund.parquet")

"""
Module for fetching and storing data from WRDS

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

def load_Mutual_Fund(data_dir=DATA_DIR):
    """
    Loads saved MF data
    """
    path = Path(data_dir) / "pulled" / "Mutual_Fund.parquet"
    df_mf = pd.read_parquet(path)
    return df_mf

def _demo():
    crsp = load_Mutual_Fund(data_dir=DATA_DIR)

if __name__ == "__main__":
    Path(DATA_DIR / "pulled").mkdir(parents=True, exist_ok=True)

    crsp = pull_mf_mapping(wrds_username=WRDS_USERNAME)
    crsp.to_parquet(DATA_DIR / "pulled" / "Mutual_Fund.parquet")

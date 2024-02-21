import pandas as pd
import time

import numpy as np
import wrds

import config
from pathlib import Path

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME


def pull_13f(wrds_username=WRDS_USERNAME, start_date = '03/31/1980', end_date = '12/31/2017'):

    my_params = {'start_date':start_date, 'end_date': end_date}

    sql_query = """
        SELECT 
            a.fdate, a.mgrno, a.mgrname,  a.typecode, a.cusip, a.shares, a.prc, a.shrout1
        FROM 
            tr_13f.s34 AS a
        WHERE 
            a.fdate BETWEEN %(start_date)s AND %(end_date)s
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df_13f = db.raw_sql(sql_query, params = my_params, date_cols=["fdate"])
    db.close()

    return df_13f

def pull_mf_mapping(wrds_username=WRDS_USERNAME, start_date = '03/31/1980', end_date = '12/31/2017'):

    my_params = {'start_date':start_date, 'end_date': end_date}

    sql_query = """
        SELECT a.fdate, a.mgrco
        FROM 
            tr_mutualfunds.s12type7 AS a
        WHERE 
            a.fdate BETWEEN %(start_date)s AND %(end_date)s
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df_mf = db.raw_sql(sql_query, params = my_params, date_cols=["fdate"])
    db.close()

    return df_mf

def load_13f(data_dir=DATA_DIR):
    path = Path(data_dir) / "pulled" / "13f.parquet"
    df_13f = pd.read_parquet(path)
    return df_13f


def load_Mutual_Fund(data_dir=DATA_DIR):
    path = Path(data_dir) / "pulled" / "Mutual_Fund.parquet"
    df_mf = pd.read_parquet(path)
    return df_mf

def _demo():
    comp = load_13f(data_dir=DATA_DIR)
    crsp = load_Mutual_Fund(data_dir=DATA_DIR)

if __name__ == "__main__":
    comp = pull_13f(wrds_username=WRDS_USERNAME)
    comp.to_parquet(DATA_DIR / "pulled" / "13f.parquet")

    crsp = pull_mf_mapping(wrds_username=WRDS_USERNAME)
    crsp.to_parquet(DATA_DIR / "pulled" / "Mutual_Fund.parquet")
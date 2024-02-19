import pandas as pd

import numpy as np
import wrds

import config
from pathlib import Path

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME


def pull_13f(wrds_username=WRDS_USERNAME):
    sql_query = """
        SELECT 
            a.fdate, a.mgrno, a.mgrname,  a.typecode, a.cusip, a.shares, a.prc, a.shrout1
        FROM 
            tr_13f.s34 AS a
        WHERE 
            a.fdate BETWEEN '03/31/1980' AND '12/31/2017'
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df_13f = db.raw_sql(sql_query, date_cols=["fdate"])
    db.close()

    return df_13f

def pull_mutual_fund(wrds_username=WRDS_USERNAME):
    sql_query = """
        SELECT 
            a.fdate, a.fundno, a.fundname
        FROM 
            tr_mutualfunds.s12 AS a
        WHERE 
            a.fdate BETWEEN '03/31/1980' AND '12/31/2017'
        """

    db = wrds.Connection(wrds_username=wrds_username)
    df_13f = db.raw_sql(sql_query, date_cols=["fdate"])
    db.close()

    return df_13f

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

    crsp = pull_mutual_fund(wrds_username=WRDS_USERNAME)
    crsp.to_parquet(DATA_DIR / "pulled" / "Mutual_Fund.parquet")
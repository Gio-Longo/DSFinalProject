import pandas as pd
import numpy as np

import config
from pathlib import Path
DATA_DIR = Path(config.DATA_DIR)

def clean_data(period, data_dir = DATA_DIR):
    start, end = period
    
    df = pd.read_parquet(data_dir / "pulled/13f.parquet")
    df = df[df['fdate'] <= end]
    df = df.dropna(subset=['prc','shrout1'])
    df = df[(df['stkcd']=='0') | (df['stkcd'].isnull())]
    df = df[(df['exchcd'].isin(['A','B','V']))  | (df['exchcd'].isnull())]

    df_mf = pd.read_parquet(data_dir / "pulled/Mutual_Fund.parquet")
    df['mf'] = df['mgrname'].isin(df_mf['mgrco'].drop_duplicates())

    df_pf = pd.read_csv(data_dir / "manual/PF_names.csv")
    df['pf'] = df['mgrname'].isin(df_pf['PF_name'])

    last_type_before_dec98 = df[df['fdate'] < '1998-12-01'].groupby(['mgrno', 'mgrname'])['typecode'].last().rename('typecode_correct')
    df = df.merge(last_type_before_dec98, on=['mgrno', 'mgrname'], how='left')
    df.loc[df['fdate'] >= '1998-12-01', 'typecode'] = df['typecode_correct'].fillna(df['typecode'])

    most_recent_type_code = df.groupby(['mgrno', 'mgrname'])['typecode'].last().rename('typecode_recent')
    df = df.merge(most_recent_type_code, on=['mgrno', 'mgrname'])
    df['typecode'] = df['typecode_recent']

    df['new_typecode'] = np.nan
    df.loc[df['typecode'] == 1, 'new_typecode'] = 1
    df.loc[df['typecode'] == 2, 'new_typecode'] = 2
    df.loc[df['typecode'] == 3, 'new_typecode'] = 3
    df.loc[df.groupby(['mgrno', 'mgrname'])['mf'].transform('any') & df['typecode'].isin([3,4,5]), 'new_typecode'] = 4
    df.loc[df.groupby(['mgrno', 'mgrname'])['pf'].transform('any') & df['typecode'].isin([3,4,5]), 'new_typecode'] = 5
    df['new_typecode'] = df['new_typecode'].fillna(6)
    df['typecode'] = df['new_typecode']

    df = df[df['fdate'] >= start]
    return df[['fdate', 'mgrno', 'mgrname', 'typecode', 'shares', 'prc', 'shrout1']]

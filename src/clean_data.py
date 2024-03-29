"""
Cleans data based on parameters given in the paper.

- Loads main 13F data from parquet, and removes missing price (prc) or shares outstanding (shrout1).
- Filters entries not matching chosen stock codes (stkcd) or exchange codes (exchcd)
- Marks mutual/pension funds cross-referenced against Mutual_Fund and pension funds lists
- Adjusts typecode for entries before 1998 with the most recent typecode per manager; reclassifies typecode
    based on flag/original typecode
- Restricts start/end date

Takes period (tuple, start/end date) and the data directory (Path, with data) and returns a dataframe.
"""


import pandas as pd
import numpy as np

import config
DATA_DIR = config.DATA_DIR

STARTDATE = config.STARTDATE_OLD
ENDDATE = config.ENDDATE_OLD

def clean_data(period = (STARTDATE, ENDDATE), data_dir = DATA_DIR):
    """
    Takes period (tuple, start/end date) and the data directory (Path, with data)
    returns a dataframe of cleaned data
    """
    start, end = period
    df = pd.read_parquet(data_dir / "pulled/13f.parquet")
    df = df[df['fdate'] <= end]
    df = df.dropna(subset=['prc','shrout1'])
    df = df[(df['stkcd']=='0') | (df['stkcd'].isnull())]
    df = df[(df['exchcd'].isin(['A','B','V']))  | (df['exchcd'].isnull())]
    df = df.drop(columns=['stkcd', 'exchcd'])

    df = df.sort_values('fdate')
    last_type_before_dec98 = df[df['fdate'] < '1998-12-01'].groupby(['mgrno', 'mgrname'])['typecode'].last().rename('typecode_correct')
    df = df[df['fdate'] >= start].merge(last_type_before_dec98, on=['mgrno', 'mgrname'], how='left')
    df.loc[df['fdate'] >= '1998-12-01', 'typecode'] = df['typecode_correct'].fillna(df['typecode'])

    most_recent_type_code = df.groupby(['mgrno', 'mgrname'])['typecode'].last().rename('typecode_recent')
    df = df.merge(most_recent_type_code, on=['mgrno', 'mgrname'])
    df['typecode'] = df['typecode_recent']

    df['new_typecode'] = np.nan
    df.loc[df['typecode'] == 1, 'new_typecode'] = 1
    df.loc[df['typecode'] == 2, 'new_typecode'] = 2

    df_mf = pd.read_parquet(data_dir / "pulled/Mutual_Fund.parquet")
    df_mf = df_mf[df_mf['fdate'] <= end].drop_duplicates()
    df['fdate_temp'] = df['fdate'].where(df['fdate'] >= pd.to_datetime('03/31/1994'), pd.to_datetime('03/31/1994'))
    df = df.merge(df_mf, left_on=['mgrno', 'fdate_temp'], right_on=['mgrcocd', 'fdate'], how='left', indicator=True)
    df['mf'] = df['_merge'] == 'both'
    df = df.drop(columns=['_merge', 'fdate_temp', 'mgrcocd', 'fdate_y']).rename(columns={'fdate_x': 'fdate'})

    df.loc[df['mf'], 'new_typecode'] = 4
    df.loc[df['typecode'].isin([3,4]), 'new_typecode'] = 3

    df_pf = pd.read_csv(data_dir / "manual/PF_names.csv")
    df['pf'] = df['mgrname'].isin(df_pf['PF_name'])

    df.loc[df.groupby(['mgrno', 'mgrname'])['pf'].transform('any') & df['typecode'].isin([3,4,5]), 'new_typecode'] = 5
    df['new_typecode'] = df['new_typecode'].fillna(6)
    df['typecode'] = df['new_typecode']
    
    return df[['fdate', 'mgrno', 'mgrname', 'typecode', 'cusip', 'shares', 'prc', 'shrout1']]

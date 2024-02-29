import pandas as pd
import numpy as np

def roll_stocks(group):
    uc_dict = {'Qtr': [], 'universe': []}
    quarters = group['Qtr'].unique()
    for i, q in enumerate(quarters):
        window_quarters = quarters[max(0, i - 11) : i + 1]
        window_data = group[group['Qtr'].isin(window_quarters)]
        uc_dict['Qtr'].append(q)
        uc_dict['universe'].append(window_data['cusip'].nunique())
    return pd.DataFrame(uc_dict)

def market_val(df):
    df = df.drop_duplicates(subset=['cusip'])
    df['val'] = df['prc'] * df['shrout1']*1000000
    return df['val'].sum()

def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:02.0f}'.format(n*100)
    return percentile_


def build_DFs(cleaned_data, periods):
    df = pd.read_parquet(cleaned_data)
    df = df[df['fdate'].between(periods[0][0],periods[-1][1])]

    df['Qtr'] = df['fdate'].dt.to_period('Q')
    df = df.sort_values(by='Qtr')

    df['val'] = df['shares'] * df['prc']

    managers = df.groupby(['Qtr', 'mgrno', 'mgrname']).agg(
        AUM=('val', 'sum'),
        stocks=('cusip', 'nunique'),
        type=('typecode', 'last')
    ).reset_index()

    grouped = df.groupby(['mgrno', 'mgrname'])
    universe = grouped.apply(roll_stocks).reset_index(level=2, drop=True).reset_index()
    managers = managers.merge(universe, on=['Qtr', 'mgrno', 'mgrname'])

    market = df.groupby('Qtr').apply(market_val).reset_index()
    market.columns = ['Qtr', 'market_val']

    df_list = {}
    for period in periods:
        start, end = period
        managers_sub = managers[managers['Qtr'].between(start, end)]
        market_sub = market[market['Qtr'].between(start, end)]

        by_type = managers_sub.groupby('type').agg(
        number=('mgrno', 'nunique'),
        type_AUM=('AUM', 'sum'),
        AUM_median=('AUM', 'median'),
        AUM_90=('AUM', lambda x: np.percentile(x, 90)),
        stocks_median=('stocks', 'median'),
        stocks_90=('stocks', lambda x: np.percentile(x, 90)),
        universe_median=('universe', 'median'),
        universe_90=('universe', lambda x: np.percentile(x, 90)))

        by_type['market_held'] = np.round(by_type['type_AUM'] /market_sub['market_val'].sum()*100).astype(int)
        by_type['AUM_median'] = np.round(by_type['AUM_median'] /1000000).astype(int)
        by_type['AUM_90'] = np.round(by_type['AUM_90'] /1000000).astype(int)
        by_type['stocks_median'] = np.round(by_type['stocks_median']).astype(int)
        by_type['stocks_90'] = np.round(by_type['stocks_90']).astype(int)
        by_type['universe_median'] = np.round(by_type['universe_median']).astype(int)  
        by_type['universe_90'] = np.round(by_type['universe_90']).astype(int)  

        by_type = by_type.drop('type_AUM', axis=1)
        df_list[period] = by_type

    return df_list

# dfs = build_DFs('13f.parquet',[('1980-01-01','1984-12-31')])
# dfs[('1980-01-01','1984-12-31')]
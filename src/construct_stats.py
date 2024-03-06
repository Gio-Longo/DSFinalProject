"""
Constructs statistics by quarter for total number of institutions, 
AUM by type, and unique manager name/number pairs into tables 
and plots the data.

Functions:
- Pivot data into tables based on specific columns.
- Create dataframes for the count of institutions, AUM by type, and unique manager name/number pairs.
- Plot statistics over time!
"""

import config
from pathlib import Path
import pandas as pd
import plotnine as p9
import clean_data
from mizani.formatters import custom_format
from IPython.display import display

output_dir = Path(config.OUTPUT_DIR)

STARTDATE = config.STARTDATE_OLD
ENDDATE = config.ENDDATE_NEW

def pivot_table(table, col_val):
    """
    Creates a pivot table from a DataFrame, indexing by date (fdate), 
    and aggregates values by typecode
    """
    return table.pivot_table(
        index='fdate',
        columns='typecode', 
        values=col_val, 
    )


def create_avg_aum_df(cleaned_df):
    """
    Generates a DataFrame summarizing the total AUM by 'typecode' and 'fdate', aggregating
    AUM values for unique 'mgrno' and 'mgrname' combinations (since they are the same manager)
    """
    summed_aum_with_typecode = cleaned_df.groupby(['fdate', 'mgrno', 'mgrname']).agg({
        'AUM': 'mean',
        'typecode': 'first'  
    }).reset_index()

    summed_aum_with_typecode = summed_aum_with_typecode.sort_values(by=['fdate', 'mgrno', 'mgrname']).reset_index(drop=True)
    aum_by_code_and_date = summed_aum_with_typecode.groupby(['fdate', 'typecode'])['AUM'].sum().reset_index()

    return pivot_table(aum_by_code_and_date, 'AUM')


def create_aum_df(cleaned_df):
    """
    Generates a DataFrame summarizing the total AUM by 'typecode' and 'fdate', aggregating
    AUM values for unique 'mgrno' and 'mgrname' combinations (since they are the same manager)
    """
    summed_aum_with_typecode = cleaned_df.groupby(['fdate', 'mgrno', 'mgrname']).agg({
        'AUM': 'sum',
        'typecode': 'first'  
    }).reset_index()

    summed_aum_with_typecode = summed_aum_with_typecode.sort_values(by=['fdate', 'mgrno', 'mgrname']).reset_index(drop=True)
    aum_by_code_and_date = summed_aum_with_typecode.groupby(['fdate', 'typecode'])['AUM'].sum().reset_index()

    return pivot_table(aum_by_code_and_date, 'AUM')


def create_mgrs_df(cleaned_df):
    """
    DataFrame counting unique 'mgrno' and 'mgrname' pairs by 'typecode' and 'fdate'
    for distribution over time
    """
    unique_mgr_counts_by_type = (cleaned_df.groupby(['fdate', 'typecode'])
                                 .apply(lambda x: x.drop_duplicates(['mgrno', 'mgrname']).shape[0]).reset_index(name='UniqueMgrCounts'))
    return pivot_table(unique_mgr_counts_by_type, 'UniqueMgrCounts')


def construct_stats(cleaned_df):
    '''
    Creates three data frames that contain useful plotting information. The three dataframes are the
    total number of institutions at each quarter, the total AUM by institution type per quarter, and
    the number of unique manager name/number pairs per quarter.
    '''

    cleaned_df['AUM'] = cleaned_df['prc'] * cleaned_df['shares']

    type_counts_df = create_type_counts_df(cleaned_df).reset_index()
    aum_df = create_aum_df(cleaned_df).reset_index()
    mgrs_df = create_mgrs_df(cleaned_df).reset_index()

    cols = ['fdate' ,'Bank', 'Insurance', 'Mutual Funds', 'Investment Advisors', 'Other']

    type_counts_df.columns = cols
    aum_df.columns = cols
    mgrs_df.columns = cols

    stats = (type_counts_df, aum_df, mgrs_df)

    return stats


def plot_stats_data(stats_df, value_name, title, file_name, condense=False, path = plot_path):
    """
    Plots institution counts over time
    """
    df = stats_df.copy()
    df.reset_index(inplace=True)
    long_df = stats_df.melt(id_vars=['fdate'], var_name='Type', value_name=value_name)

    format = '{:,.0f}'
    if condense:
        format = '${:.0e}'
    
    plot = (
        p9.ggplot(long_df, p9.aes(x='fdate', y=value_name, color='Type')) +
        p9.geom_line() + 
        p9.labs(title=title, x='Date', y=value_name) +  
        p9.facet_wrap('~ Type', ncol=3, scales='free_y') +
        p9.scale_y_continuous(labels=custom_format(format)) +
        p9.theme(
            figure_size=(14, 7),
            axis_text_x=p9.element_text(rotation=45, hjust=1),
            plot_title=p9.element_text(ha='center')
        )
    )
    
    plot_path = output_dir / file_name
    plot.save(filename=plot_path, dpi=300)
    return plot_path

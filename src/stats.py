import config
from pathlib import Path
import pandas as pd
import plotnine as p9
import clean_data
from mizani.formatters import custom_format

output_dir = config.OUTPUT_DIR

plot_path = output_dir / 'plots'
plot_path.mkdir(parents=True, exist_ok=True)


def pivot_table(table, col_val):
    return table.pivot_table(
        index='fdate',
        columns='typecode', 
        values=col_val, 
    )


def create_type_counts_df(cleaned_df):
    inst_df = cleaned_df.copy()
    inst_df = (inst_df.groupby('fdate', as_index=False)
               .apply(lambda x: x.drop_duplicates(subset=['mgrno', 'mgrname'])).reset_index(drop=True))
    type_counts = inst_df.groupby('fdate')['typecode'].value_counts().unstack()

    return type_counts


def create_aum_df(cleaned_df):
    summed_aum_with_typecode = cleaned_df.groupby(['fdate', 'mgrno', 'mgrname']).agg({
        'AUM': 'sum',
        'typecode': 'first'  
    }).reset_index()

    summed_aum_with_typecode = summed_aum_with_typecode.sort_values(by=['fdate', 'mgrno', 'mgrname']).reset_index(drop=True)
    aum_by_code_and_date = summed_aum_with_typecode.groupby(['fdate', 'typecode'])['AUM'].sum().reset_index()

    return pivot_table(aum_by_code_and_date, 'AUM')


def create_mgrs_df(cleaned_df):
    unique_mgr_counts_by_type = (cleaned_df.groupby(['fdate', 'typecode'])
                                 .apply(lambda x: x.drop_duplicates(['mgrno', 'mgrname']).shape[0]).reset_index(name='UniqueMgrCounts'))
    return pivot_table(unique_mgr_counts_by_type, 'UniqueMgrCounts')


def create_stats(start_date, end_date):
    '''
    Creates three data frames that contain useful plotting information. The three dataframes are the
    total number of institutions at each quarter, the total AUM by institution type per quarter, and
    the number of unqiue manager name/number pairs per quarter.
    '''
    cleaned_df = clean_data.clean_data((pd.to_datetime(start_date), pd.to_datetime(end_date)))
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


def plot_stats_data(stats_df, value_name, title, file_name, condense=False):
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
    
    plot.save(filename=file_name, path=str(plot_path), dpi=300)


if __name__ == '__main__':
    type_counts_df, aum_df, mgrs_df = create_stats('1980-03-31', '2024-12-31')

    plot_stats_data(type_counts_df, 'Count', 'Type Counts Over Time', 'type_counts.png')
    plot_stats_data(aum_df, 'AUM', 'AUM Over Time', 'aum.png', True)
    plot_stats_data(mgrs_df, 'UniqueMgrCounts', 'Managers Over Time', 'mgrs.png')
    
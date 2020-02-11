import psycopg2
import pandas as pd

def interval_width_transitions(interval_df):
    """
    Given a DataFrame of interval load data, return a zip object
    identifying when there is a transition from one interval_width to another with tuples
    containing the timestamps of the transition start (i.e. last value with the previous width)
    and transition end (i.e. first value with the next width)
    """
    filler_start = interval_df['interval_width'].iloc[-1]
    filler_end = interval_df['interval_width'].iloc[0]
    # compares shifted interval_widths to identify a transition
    transitions_start = (interval_df['interval_width'] 
                         != interval_df['interval_width'].shift(-1,
                                                                axis=0,
                                                                fill_value=filler_start))
    transitions_end = (interval_df['interval_width'] 
                       != interval_df['interval_width'].shift(1,
                                                              axis=0,
                                                              fill_value=filler_end))
    transitions = zip(interval_df.loc[transitions_start, 'interval_end'],
                      interval_df.loc[transitions_end, 'interval_end'])
    return transitions

def resample_intervals(interval_df):
    """
    Given a DataFrame of interval load data, return a DataFrame with 
    resampled data at its provided frequency such that gaps get filled with nulls.
    """ 
    time_series = interval_df.drop_duplicates()
    time_series = time_series.set_index(interval_df['interval_end']).sort_index()
    interval_widths = time_series['interval_width'].unique()
    resampled_series = pd.DataFrame()
    # separately resampling segments with different interval_widths
    for interval in interval_widths:
        interval_time_series = time_series.loc[time_series['interval_width'] 
                                                           == interval].asfreq(f'{interval}S')
        resampled_series = pd.concat([resampled_series, 
                                      interval_time_series])
    # resampling the time between a transition from different interval_widths
    transitions = interval_width_transitions(interval_df)
    for transition in transitions:
        min_interval = min(time_series.loc[transition[0], 'interval_width'],
                           time_series.loc[transition[1], 'interval_width'])
        interval_time_series = time_series.loc[((time_series['interval_end'] == transition[0])
                                                | (time_series['interval_end'] == transition[1]))
                                               ].asfreq(f'{min_interval}S')
        # the first and last value are already in the data so dropped to prevent duplicates
        interval_time_series.drop([transition[0], transition[1]], inplace=True)
        resampled_series = pd.concat([resampled_series, 
                                      interval_time_series])
    return resampled_series.sort_index()

def data_gap_start_stop(interval_df):
    """
    Given a DataFrame of interval load data, 
    returns the timestamps at the beginning and end of data gaps.
    """
    null_ixs = interval_df.loc[interval_df['interval_end'].isnull()].index
    pre_nulls = interval_df.shift(-1, axis=0, fill_value=0)
    post_nulls = interval_df.shift(1, axis=0, fill_value=0)

    pre_null_ixs = pre_nulls.loc[pre_nulls['interval_end'].isnull()]
    post_null_ixs = post_nulls.loc[post_nulls['interval_end'].isnull()]
    gap_ixs = pre_null_ixs.merge(post_null_ixs,
                                 how='outer',
                                 left_index=True,
                                 right_index=True)
    gap_ixs.drop(null_ixs,
                 inplace=True,
                 errors='ignore')
    return gap_ixs.index

def gap_date_df(interval_df):
    """
    Given a DataFrame of interval load data, 
    returns a DataFrame with all days that include a data gap greater than 1 hour.
    If the gap is greater than 1 hour, but the amount of that gap occurring on a given date
    is less than 1 hour, then that date still is included because of the overall gap length.
    """
    working_df = resample_intervals(interval_df)
    gap_starts_stops = data_gap_start_stop(working_df)
    gap_dates = pd.DataFrame()
    if len(gap_starts_stops) == 0:
        pass
    else:
        range_len = int(len(gap_starts_stops)/2 + 1)
        # checking whether the gap is over an hour in length
        # considers the gap between and interval_end and the start of the next interval
        # not just the gap between interval_end
        for n in range(0, range_len, 2):
            gap_length = gap_starts_stops[n+1] - gap_starts_stops[n]
            gap_end_interval = working_df.loc[gap_starts_stops[n+1],
                                              'interval_width']
            gap_length -= pd.Timedelta(gap_end_interval, unit='s')
            if gap_length > pd.Timedelta(3600, unit='s'):
                temp_gap_dates = pd.date_range(gap_starts_stops[n],
                                               gap_starts_stops[n+1])
                temp_gap_dates = pd.DataFrame(temp_gap_dates.strftime('%Y-%m-%d'),
                                              columns=['gap_dates'])
                gap_dates = pd.concat([gap_dates,
                                       temp_gap_dates])
        gap_dates['site_id'] = working_df['site_id'].iloc[0]
    return gap_dates

def multi_site_gap_date_df(list_of_sites):
    """
    Given a list of site_ids, connect to the provided database and loop through 
    querying of each site's data, creating and then returning a DataFrame
    with all days that include a data gap greater than 1 hour.
    """
    connection = psycopg2.connect(
                                  database="interval_load_data",
                                  user='postgres',
                                  password='Onei9yepahShac0renga',
                                  host="test-interval-load-data.cwr8xr5dhgm1.us-west-2.rds.amazonaws.com",
                                  port="5432")
    gap_dates_df = pd.DataFrame()
    for site in list_of_sites:
        interval_df = pd.read_sql_query(f"SELECT * \
                                          FROM intervals \
                                          WHERE site_id='{site}';"
                                        , connection)
        temp_gap_dates_df = gap_date_df(interval_df)
        gap_dates_df = pd.concat([gap_dates_df,
                                  temp_gap_dates_df])
    return gap_dates_df.reset_index(drop=True)
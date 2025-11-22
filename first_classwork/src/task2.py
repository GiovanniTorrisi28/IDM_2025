import pandas as pd

def filter_by_date_range(df, start_date, end_date):
    df['data'] = pd.to_datetime(df['data']) # cast della colonna data in datetime
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    return df[(df['data'] >= start) & (df['data'] <= end)]

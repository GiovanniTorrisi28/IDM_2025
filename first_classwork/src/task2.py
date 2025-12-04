import pandas as pd

def filter_by_date_range(df, start_date, end_date):
    """
    Filtra i record della colonna 'data' di un dataframe che si trovano in un certo range
    
    :param df: Dataframe dei dati
    :param start_date: Data di inizio range
    :param end_date: Data di fine range
    """

    df['data'] = pd.to_datetime(df['data']) # conversione della colonna 'data' nel formato datetime per fare il confronto
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    return df[(df['data'] >= start) & (df['data'] <= end)]

def filter_by_hour_range(df, start_time, end_time):
    """
    Filtra i record della colonna 'ora' di un dataframe che si trovano in un certo range
    
    :param df: Dataframe dei dati
    :param start_time: Orario di inizio range
    :param end_time: Orario di fine range
    """
    return df[(df['ora'] >= start_time) & (df['ora'] < end_time)]


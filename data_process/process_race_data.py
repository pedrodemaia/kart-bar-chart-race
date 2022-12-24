'''
Read raw race tables and convert into data ready to be printed
'''

import pandas as pd
from operator import itemgetter
import datetime

def get_time_from_string(value: str, format: str = '%M:%S.%f') -> datetime.time:
    '''
    Return time object from string
    '''

    if pd.isna(value):
        return value

    return datetime.datetime.strptime(value, format).time()

def get_course_length(summary: pd.DataFrame) -> float:
    '''
    Get course length in km
    '''

    total_time = get_time_from_string(summary.iloc[0]['T.T'], '%H:%M:%S.%f')
    speed = float(summary.iloc[0]['V.M.(km/h)'].replace(',', '.'))
    laps = int(summary.iloc[0]['VLTS'])
    avg_lap_time = (total_time.minute + total_time.second/60)/60/laps

    return speed * avg_lap_time

def create_unified_table(summary: pd.DataFrame, detailed: pd.DataFrame) -> pd.DataFrame:
    '''
    Create single table with all relevant data from raw tables
    '''

    summary['NICKNAME'] = summary['NOME'].apply(lambda x: ' '.join(itemgetter(0, -1)(x.split(' '))).title())
    car_pilots = summary[['#', 'NICKNAME']].set_index(['#'])['NICKNAME'].to_dict()

    detailed.drop('VLT/COMP', axis=1, inplace=True)
    detailed.rename(columns=car_pilots, inplace=True)

    return detailed.applymap(get_time_from_string)

def get_cumulative_time(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Create table with cumulative times for each car each lap
    '''

    cumulative = df.copy()

    for pilot in df.columns:
        sum = datetime.datetime.min
        for lap, laptime in df[pilot].iteritems():
            if pd.isna(laptime):
                break
            sum += datetime.timedelta(seconds=laptime.minute * 60 + laptime.second, microseconds=laptime.microsecond)
            cumulative.loc[lap, pilot] = sum.time()

    return cumulative

def process_data(summary: pd.DataFrame, detailed: pd.DataFrame) -> None:
    '''
    Process raw data to prepare print
    '''

    times = create_unified_table(summary, detailed)
    cumulative = get_cumulative_time(times)

    a = 1
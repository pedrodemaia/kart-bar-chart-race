'''
Read raw race tables and convert into data ready to be printed
'''
from typing import Dict, Tuple

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

def get_timedelta_from_time(value: datetime.time) -> datetime.timedelta:
    '''
    Return timedelta from time
    '''

    return datetime.timedelta(minutes=value.minute, seconds=value.second, microseconds=value.microsecond)

def time_in_hour(value: datetime.time) -> float:
    '''
    Get the time of a lap in hours
    '''

    return (value.minute + (value.second + value.microsecond / 10000000) / 60) / 60

def get_course_length(summary: pd.DataFrame) -> float:
    '''
    Get course length in km
    '''

    total_time = get_time_from_string(summary.iloc[0]['T.T'], '%H:%M:%S.%f')
    speed = float(summary.iloc[0]['V.M.(km/h)'].replace(',', '.'))
    laps = int(summary.iloc[0]['VLTS'])
    avg_lap_time = time_in_hour(total_time) / laps

    return speed * avg_lap_time

def get_lap_speed(distance: float, time: datetime.time) -> float:
    '''
    Get average lap speed
    '''

    if pd.isna(time):
        return time
    return distance / time_in_hour(time)

def get_total_time(summary: pd.DataFrame) -> Dict[str,datetime.time]:
    '''
    Get total race time by pilot
    '''

    return summary[['NICKNAME', 'T.T']].set_index('NICKNAME')['T.T'].apply(
        lambda x: get_time_from_string(x, '%H:%M:%S.%f')
    ).to_dict()

def get_lap_count(df: pd.DataFrame) -> Dict[str, int]:
    '''
    Return the laps completed by each pilot
    '''

    lap_count = {}
    for pilot in df.columns:
        lap_count[pilot] = df[pilot][~pd.isna(df[pilot])].index.max()

    return lap_count

def create_unified_table(summary: pd.DataFrame, detailed: pd.DataFrame) -> pd.DataFrame:
    '''
    Create single table with all relevant data from raw tables
    '''

    summary['NICKNAME'] = summary['NOME'].apply(lambda x: ' '.join(itemgetter(0, -1)(x.split(' '))).title())
    car_pilots = summary[['#', 'NICKNAME']].set_index(['#'])['NICKNAME'].to_dict()

    detailed.drop('VLT/COMP', axis=1, inplace=True)
    detailed.rename(columns=car_pilots, inplace=True)
    detailed = detailed.applymap(get_time_from_string)
    detailed.loc['total'] = get_total_time(summary)

    return detailed

def get_cumulative_time(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Create table with cumulative times for each car each lap
    '''

    cumulative = df.copy()

    offsets = {}
    for pilot in df.columns:
        sum = datetime.datetime.min
        for lap, laptime in df[pilot].iteritems():
            if lap != 'total':
                if pd.isna(laptime):
                    continue
                sum += get_timedelta_from_time(laptime)
                cumulative.loc[lap, pilot] = sum.time()
            else:
                offsets[pilot] = get_timedelta_from_time(df[pilot]['total']) - get_timedelta_from_time(sum)

        # add offset time to all pilots
        sum = datetime.datetime.min + offsets[pilot]
        for lap, laptime in df[pilot].iteritems():
            if lap == 'total' or pd.isna(laptime):
                continue
            sum += get_timedelta_from_time(laptime)
            cumulative.loc[lap, pilot] = sum.time()

    return cumulative.drop(index='total')

def get_order_on_lap(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Order pilots on each lap
    '''

    orders = pd.DataFrame(columns=df.columns)
    for lap, times in df.iterrows():
        pos = {pilot: order + 1 for order, pilot in enumerate(times.sort_values().index)}
        orders.loc[lap] = pos

    # fix values for uncompleted laps
    lap_count = get_lap_count(df)
    max_laps = max(lap_count.values())
    for pilot, num_laps in lap_count.items():
        last_value = orders[pilot][num_laps]
        for lap in range(num_laps, max_laps+1):
            orders[pilot][lap] = last_value

    return orders

def get_average_speeds(times: pd.DataFrame, distance: float) -> pd.DataFrame:
    '''
    Get average lap spped for each lap and each pilot for course distance and lap times
    '''

    speeds = times.copy()

    for pilot in times.columns:
        speeds[pilot] = times[pilot].apply(lambda x: get_lap_speed(distance, x))

    return speeds

def process_data(summary: pd.DataFrame, detailed: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
    Process raw data to prepare print
    '''

    times = create_unified_table(summary, detailed)
    cumulative = get_cumulative_time(times)
    positions = get_order_on_lap(cumulative)
    fast_laps = get_order_on_lap(times.drop(index='total'))
    speed = get_average_speeds(times.drop(index='total'), get_course_length(summary))

    return times, cumulative, positions, fast_laps, speed
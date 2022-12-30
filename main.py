'''
This module prints a kart race evolution from mylaptime.com.
'''

from data_import.import_data import download_race_data
from data_process.process_race_data import process_data
from data_print.print_race_evolution import create_gif

if __name__ == '__main__':
    race_link = 'http://www.mylaptime.com/laptime/clientes/214V20106819C9780G1X1P108/results/r3.html?evt=11226&epg=6018'

    (summary_df, detailed_df) = download_race_data(race_link)
    times, cumulative, positions, fast_laps, speed = process_data(summary_df, detailed_df)
    create_gif(positions, speed)


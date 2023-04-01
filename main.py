'''
This module prints a kart race evolution from mylaptime.com.
'''

from data_import.import_data import download_race_data
from data_process.process_race_data import process_data
from data_print.print_race_evolution import create_gif

import argparse

if __name__ == '__main__':

    default_link = 'http://www.mylaptime.com/laptime/clientes/214V20106819C9780G1X1P108/results/r3.html?evt=11303&epg=6512'

    parser = argparse.ArgumentParser(description='Kart timer race link')
    parser.add_argument('race_link', type=str, default=default_link, help='Race link')

    args = parser.parse_args()

    (summary_df, detailed_df) = download_race_data(args.race_link)
    times, cumulative, positions, fast_laps, speed = process_data(summary_df, detailed_df)
    create_gif(positions, speed)


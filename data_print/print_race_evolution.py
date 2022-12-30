'''
Print bar chart race from kart race data
'''
from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
import numpy as np


def expand_data(positions: pd.DataFrame, speed: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    expanded_positions = positions.copy().fillna(0)
    expanded_speed = speed.copy().fillna(0)

    factor = 10
    num_laps = speed.shape[0]

    # convert each lap into 10 frames
    expanded_speed.index = range(1, num_laps * factor, factor)
    expanded_positions.index = range(1, num_laps * factor, factor)

    # add extra frames to last lap
    expanded_speed.loc[num_laps*factor] = expanded_speed.iloc[-1]
    expanded_positions.loc[num_laps * factor] = expanded_positions.iloc[-1]

    # interpolate created frames
    row_nums = [i for i in range(1, num_laps*factor) if i % 10 != 1]
    empty = pd.DataFrame(np.nan, index=row_nums, columns=speed.columns)
    expanded_speed = pd.concat([expanded_speed, empty]).sort_index().interpolate()
    expanded_positions = pd.concat([expanded_positions, empty]).sort_index().interpolate()

    return expanded_positions, expanded_speed

def print_lap_charts(positions: pd.DataFrame, speed: pd.DataFrame) -> None:
    '''
    Create a single lap bar chart
    '''

    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))

    def update(idx: int) -> None:
        ax.clear()
        ax.set_facecolor(plt.cm.Greys(0.2))
        [spine.set_visible(False) for spine in ax.spines.values()]
        hbars = ax.barh(
            y=positions.loc[idx + 1],
            tick_label=positions.loc[idx + 1].index,
            width=speed.loc[idx + 1].values,
            height=0.8,
            color=plt.cm.YlOrRd(rescale(speed.loc[idx + 1].values))
        )
        ax.invert_yaxis()
        ax.set_title(f'{int(np.floor(idx/10))+1}a volta', fontsize='larger')
        ax.bar_label(hbars, fmt='%.2f km/h')
        ax.get_xaxis().set_visible(False)

    fig, ax = plt.subplots(
        figsize=(10,7),
        facecolor=plt.cm.Greys(0.2),
        dpi=150,
        tight_layout=True
    )

    animation = FuncAnimation(
        fig=fig,
        func=update,
        frames=len(speed),
        interval=0.1
    )

    gif_writer = PillowWriter(fps=10)
    animation.save('race_evolution.gif', writer=gif_writer)

def create_gif(positions: pd.DataFrame, speed: pd.DataFrame) -> None:
    '''
    Create gif of each pilot's position on each lap with average speed
    '''

    expanded_positions, expanded_speed = expand_data(positions, speed)
    print_lap_charts(expanded_positions, expanded_speed)


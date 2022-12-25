'''
Print bar chart race from race data
Source: https://pythoninoffice.com/how-to-create-the-bar-chart-race-plot-in-python/
'''

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

def print_lap_charts(positions: pd.DataFrame, speed: pd.DataFrame) -> None:
    '''
    Create a single lap bar chart
    '''

    fig, axs = plt.subplots(nrows=1, ncols=speed.shape[0], figsize=(10, 5), tight_layout=True)
    for i, ax in enumerate(axs):
        ax.barh(y=speed.iloc[i].rank(),
                tick_label=speed.iloc[i].index,
                width=speed.iloc[i].values,
                color=plt.cm.Set1(range(speed.shape[1])))
        ax.set_title(f'{i}-th lap', fontsize='larger')
        [spine.set_visible(False) for spine in ax.spines.values()]  # remove chart outlines


    def update(i: int) -> None:
        ax.clear()
        ax.set_facecolor(plt.cm.Greys(0.2))
        [spine.set_visible(False) for spine in ax.spines.values()]
        hbars = ax.barh(y=speed.iloc[i].rank().values,
                        tick_label=speed.iloc[i].index,
                        width=speed.iloc[i].values,
                        height=0.8,
                        color=plt.cm.Set1(range(11))
                        )
        ax.set_title(f'Frame: {i}')
        # ax.bar_label(hbars, fmt='%.2d')


    fig, ax = plt.subplots(  # figsize=(10,7),
        facecolor=plt.cm.Greys(0.2),
        dpi=150,
        tight_layout=True
    )

    data_anime = FuncAnimation(
        fig=fig,
        func=update,
        frames=len(speed),
        interval=300
    )

    fig.show()

def create_gif(positions: pd.DataFrame, speed: pd.DataFrame) -> None:
    '''
    Create gif of each pilot's position on each lap with average speed
    '''

    print_lap_charts(positions, speed)


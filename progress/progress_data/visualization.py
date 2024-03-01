import matplotlib.pyplot as plt
from progress.logger import logging
from progress.utils import os







def plot_visualization(X, Y, Z, visualization_path: str) -> tuple[plt.figure, plt.Axes]:
    '''
    Create a PColorMesh of given data.

    Parameters
    ----------
    `X`: X-Axis

    `Y`: Y-Axis

    `Z`: Values

    Returns
    -------
    fig: `Figure`
    
    ax: `Axes`
    '''
    # Creating a Plot of size 16x8  
    fig, ax = plt.subplots(figsize=(24, 12))

    logging.info('Generating Visualization')
    # Plotting a PColorMesh it is similar to a Heatmap
    # Setting edge color to black so every box in visualization looks seperated
    ax.pcolormesh(X, Y, Z, edgecolors='black')

    # Setting the X-Axis Label
    ax.set_xlabel('Days', fontsize=15)
    plt.xticks(X, fontsize=13)
    plt.yticks(fontsize=13)

    # Maximum value in the data
    max_value = int(Z.max().max()) + 1

    # legend labels 
    legend_labels = ['No Data'] + list(map(lambda x: f'{x} Time' if x<2 else f'{x} Times', range(max_value)))

    # color of legends
    legend_color = ['white', '#440154', '#21918c', '#fde725']

    # creating a rectangle for legend
    legend_handles = [plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor='black') for color in legend_color]

    # setting the legend on the top center of visualization
    ax.legend(
        legend_handles, 
        legend_labels, 
        loc='upper center', 
        bbox_to_anchor=(0.5, 1.15), 
        ncol=len(legend_labels),
        fontsize=13
        )

    # Writing Text on the right side of Visuation
    for i in Y.index:
        # sum of non zero values in row
        row_sum = Z.iloc[i].sum()
        streaks, streak = [], 0

        # Counting the maximum number of zeros present in continous
        for val in Z.iloc[i]:
            if val == 0.0:
                streak += 1
            else:
                streaks.append(streak)
                streak = 0
        else:
            streaks.append(streak)
            streak = 0

        max_streak = max(streaks)
        streaks = []

        # writing text on the rigth side of visualization
        ax.text(
            x=32, 
            y=i, 
            s=f'Streak {max_streak} - Fapped {row_sum:.0f}', 
            fontdict={'fontsize': 13},
            verticalalignment='center'
            )

    logging.info(f'Saving Visualization at {visualization_path}')
    # Saving the Visualization in a Png file
    dir_name = os.path.dirname(visualization_path)
    os.makedirs(dir_name, exist_ok=True)
    fig.savefig(visualization_path, pad_inches=0.2)
    logging.info(f'Visualization saved at {visualization_path}')

    return fig, ax








if __name__ == '__main__':

    # data = utils.load_dataset()
    pass

import matplotlib.pyplot as plt
from logger import logging
import utils

config = utils.Config()





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
    fig, ax = plt.subplots(figsize=(16, 8))

    logging.info('Generating Visualization')
    # Plotting a PColorMesh it is similar to a Heatmap
    # Setting edge color to black so every box in visualization looks seperated
    ax.pcolormesh(X, Y, Z, edgecolors='black')

    # Setting the X-Axis Label
    ax.set_xlabel('Days')
    ax.set_xticks(X)

    logging.info(f'Saving Visualization at {visualization_path}')
    # Saving the Visualization in a Png file

    fig.savefig(visualization_path, pad_inches=0.2)
    logging.info(f'Visualization saved at {visualization_path}')

    return fig, ax








if __name__ == '__main__':

    # data = utils.load_dataset()
    pass

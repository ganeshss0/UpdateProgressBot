from utils import CURRENT_DATE, extract_data, save_dataset, ONE_DAY_TIMEDELTA
from visualization import plot_visualization
from CreateTemplate import add_month_row
from utils import pd, logging


def main(data:pd.DataFrame, dataset_file_path, visualization_path) -> None:
    '''Creates visualization.'''


    x, y, Z = extract_data(data)
    plot_visualization(x, y, Z, visualization_path)


    # Checking when Next day Number [1, 2, ... 31] is smaller than current day
    # Which Only True when Next day first day of month
    # Then adds a new row corrospond to Next Month
    next_day = CURRENT_DATE + ONE_DAY_TIMEDELTA

    logging.info('Syncing Last Month Row')
    if next_day.day < CURRENT_DATE.day:
        data
        data = add_month_row(data, CURRENT_DATE)
    else:
        logging.info('Last Month Row is already Updated')
        
    save_dataset(data, dataset_file_path)
    logging.info('Sync Complete')
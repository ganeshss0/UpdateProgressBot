from logger import logging
from calendar import month_abbr
import datetime as dt
import pandas as pd
import json
import os
from CreateTemplate import create


######## Constants #######
CONFIG_FILE = 'config.json'

DATASET_FILE_KEY = 'dataset_file_name'
DATASET_DIR_KEY = 'dataset_directory'
VISUAlZ_FILE_KEY = 'visualization_file_name'
VISUAlZ_DIR_KEY = 'visualization_directory'

# Current Date When the file is Running
CURRENT_DATE = dt.datetime.now()
ONE_DAY_TIMEDELTA = dt.timedelta(days=1)

# Date Format Used in CSV File
DATE_FORMAT = '%Y-%m'
##########################

class Config:
    def __init__(self) -> None:
        self.config_file = CONFIG_FILE
        self.config = self.read_config(self.config_file)
        self.visualization_path = self.get_visualization_path()  
        self.dataset_path = self.get_dataset_path()

    @staticmethod
    def read_config(file_path:str) -> dict:
        with open(file_path, mode='r', encoding='utf-8') as config:
            configuration = json.load(config)
        return configuration

    @staticmethod
    def write_config(obj: dict, file_path:str = CONFIG_FILE) -> None:
        with open(file_path, mode='w', encoding='utf-8') as config:
            json.dump(obj, config)


    def get_visualization_path(self) -> str:
        '''Returns the Path of Visualization.'''

        visual_file_name = self.config[VISUAlZ_FILE_KEY]
        visual_dir = self.config[VISUAlZ_DIR_KEY]

        return os.path.join(visual_dir, visual_file_name)

    def get_dataset_path(self) -> str:
        '''Returns the Path of the dataset.'''

        dataset_file_name = self.config[DATASET_FILE_KEY]
        dataset_dir = self.config[DATASET_DIR_KEY]

        return os.path.join(dataset_dir, dataset_file_name)


def load_dataset(filepath:str) -> pd.DataFrame:
    '''Read the CSV file and return into a dataframe object.'''

    # Reading the CSV File
    # NaN Values in CSV are filled with 'x'
    # Column [0] is the Date column
    logging.info(f'Checking {filepath} exists')
    if os.path.exists(filepath):
        logging.info(f'Loading {filepath} into DataFrame')

        return pd.read_csv(
            filepath, 
            na_values='x', 
            parse_dates=[0], 
            date_format=DATE_FORMAT,
            )
    else:
        logging.warning(f'Filepath {filepath} does not exists')
        logging.warning('Loading Dataset Template')
        return create(CURRENT_DATE)
        


def save_dataset(data:pd.DataFrame, filepath:str) -> None:
    '''Save the Dataframe Object to given path.'''

    # Changing the Date column from '2023-12-01' to '2023-12'
    # As the days are present in columns
    data['Date'] = data['Date'].dt.strftime(DATE_FORMAT)

    # Saving the data to CSV file
    # Replacing the NaN values with 'x'
    logging.info(f'Saving Data to {filepath}')
    data.to_csv(
        filepath, 
        na_rep='x', 
        float_format='%.0f', 
        index=False
        )

def extract_data(data:pd.DataFrame) -> tuple[pd.RangeIndex, pd.Series, pd.DataFrame]:
    '''Seperates the Date, columns and values.'''

    # Extracting Only those column which have data
    Z = data.iloc[:, 1:]

    # X Axis Range of Visualization
    x = pd.RangeIndex(1, 32)

    # Y Axis of Visualization
    # The month in Date column are transformed from [9, 10, 11, 12] to ['Sep', 'Oct', 'Nov', 'Dec']
    # Adding Both month and year [2023-12] --> 'Dec 2023'
    y = data['Date'].dt.month.apply(month_abbr.__getitem__) + ' ' + data['Date'].dt.year.astype(str)

    return x, y, Z
    
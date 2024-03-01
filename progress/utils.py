from progress.logger import logging
from calendar import month_abbr
import datetime as dt
import pandas as pd
import json
from progress.progress_data.CreateTemplate import create
from progress.entity import *



class Config:
    '''Configuration Class'''
    def __init__(self) -> None:
        logging.info('Initializing Configuration')

        self.config_file_path = os.path.join(CONFIG_DIR, CONFIG_FILE)
        self.config = self.read_config(self.config_file_path)
        self.visualization_path = self.get_visualization_path()  
        self.dataset_path = self.get_dataset_path()
        self.temp_data_dir = self.get_temporary_dataset_dir()
        self.response_path = self.get_response_path()
        self.bot_token = os.environ.get(BOT_TOKEN_ENVIR_KEY)
        self.super_user = self.config.get(SUPER_USER_KEY)
        self.message_time = pd.Timestamp('08:11', tz='Asia/Kolkata')

    @staticmethod
    def read_config(file_path:str) -> dict:
        return read_json(file_path)

    @staticmethod
    def write_config(obj: dict, file_path:str = CONFIG_FILE) -> None:
        write_json(obj, file_path)


    def get_visualization_path(self) -> str:
        '''Returns the Path of Visualization.'''

        visual_file_name = self.config.get(VISUALZ_FILE_KEY)
        visual_dir = self.config.get(VISUALZ_DIR_KEY)

        return os.path.join(visual_dir, visual_file_name)

    def get_dataset_path(self) -> str:
        '''Returns the Path of the dataset.'''

        dataset_file_name = self.config.get(DATASET_FILE_KEY)
        dataset_dir = self.config.get(DATASET_DIR_KEY)

        return os.path.join(dataset_dir, dataset_file_name)

    def get_response_path(self) -> str:
        '''Returns the Path of Response File'''
        
        response_file_name = self.config.get(RESPONSE_FILE_KEY)
        response_dir = self.config.get(RESPONSE_DIR_KEY)

        return os.path.join(response_dir, response_file_name)
    
    def get_temporary_dataset_dir(self) -> str:
        
        dataset_dir = self.config.get(DATASET_DIR_KEY)
        temp_data_dir = self.config.get(TEMP_DATA_DIR_KEY)

        return os.path.join(dataset_dir, temp_data_dir)


def load_dataset(filepath:str, load_default: bool = True) -> pd.DataFrame:
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
        if load_default:
            logging.warning('Loading Dataset Template')
            return create(CURRENT_DATE)
        


def save_dataset(data:pd.DataFrame, filepath:str) -> None:
    '''Save the Dataframe Object to given path.'''

    # Changing the Date column from '2023-12-01' to '2023-12'
    # As the days are present in columns
    data['Date'] = data['Date'].dt.strftime(DATE_FORMAT)

    # Saving the data to CSV file
    # Replacing the NaN values with 'x'
    dir_name = os.path.dirname(filepath)
    os.makedirs(dir_name, exist_ok=True)

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
    # [2023-12] --> 'Dec 2023'
    y = data['Date'].dt.strftime(DATE_FORMAT_VIZ)

    return x, y, Z.astype(float)
    

def read_json(file_path: str) -> dict:
    if os.path.exists(file_path):
        with open(file=file_path, mode='r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data
    else:
        return dict()

def write_json(obj: dict, file_path:str) -> None:
    parent_dir = os.path.dirname(file_path)
    os.makedirs(parent_dir, exist_ok=True)
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(obj, file)
    except Exception as e:
        logging.error(e)

    
def Validate_CSV(file_path: str) -> bool:
    
    FileExists = os.path.exists(file_path)
    ValidFileName = file_path.endswith('.csv')
    data = load_dataset(file_path)
    isDataLoaded = data != None
    isColumnCount32 = data.columns.size == 32
    

    # csv_content = io.StringIO()/
    # CSV_file.download(out=csv_content)
    # csv_content.seek(0)

    # data = pd.read_csv(csv_content)
    data.to_csv('./download.csv')
    return ValidFileName
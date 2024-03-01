import datetime as dt
import os
import inspect


CURRENT_DIR = os.path.dirname(inspect.getfile(inspect.currentframe()))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
os.chdir(ROOT_DIR)

CONFIG_DIR = 'Config'
CONFIG_FILE = 'config.json'
 

BOT_TOKEN_ENVIR_KEY = 'UPDATE_PROGRESS_TELEGRAM_BOT'

DATASET_FILE_KEY = 'dataset_file_name'
DATASET_DIR_KEY = 'dataset_directory'
TEMP_DATA_DIR_KEY = 'temporary_data_directory'
VISUALZ_FILE_KEY = 'visualization_file_name'
VISUALZ_DIR_KEY = 'visualization_directory'
RESPONSE_FILE_KEY = 'response_file_name'
RESPONSE_DIR_KEY = 'response_directory'
SUPER_USER_KEY = 'super_user'


# Current Date When the file is Running
CURRENT_DATE = dt.datetime.now()
ONE_DAY_TIMEDELTA = dt.timedelta(days=1)
ONE_MONTH_TIMEDELTA = dt.timedelta(days=30)

# Date Format Used in CSV File
DATE_FORMAT = '%Y-%m'
DATE_FORMAT_VIZ = '%b %Y'



import logging
from progress.entity import CURRENT_DATE
import os

#####################
### LOGGING FILE ####
#####################
LOG_FILE = CURRENT_DATE.strftime('%Y%m%d_%H%M%S') + '.log'
LOG_DIR = 'Logs'
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format='[%(asctime)s] - %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO
    )
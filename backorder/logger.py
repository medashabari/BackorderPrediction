import logging 
import os 
from datetime import datetime

# create log file name 

LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%y__%H_%M_%S')}.log"

LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

# Creating the logs directory if not exists

os.makedirs(LOG_FILE_DIR,exist_ok=True)

# Creating the path for log file 

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

# Configuring the log file 

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s -%(message)s",
    level = logging.INFO
)
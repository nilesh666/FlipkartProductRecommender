import logging
import os
from datetime import datetime

LOGFILE_PATH = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"
logfile = os.path.join(os.getcwd(), "logs", LOGFILE_PATH)

os.makedirs(logfile, exist_ok=True)

LOG_FILE_PATH_CURRENT = os.path.join(logfile, LOGFILE_PATH)

logging.basicConfig(
    filename=LOG_FILE_PATH_CURRENT,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)
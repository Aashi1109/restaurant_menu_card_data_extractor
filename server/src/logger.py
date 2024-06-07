import logging.handlers
import os

from server.src.config import LOG_LEVEL, LOG_PATH

# Define the log file name
log_file = "application.log"

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)  # Set the minimum level of messages to log

# create dir if not exists
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

log_file_path = os.path.join(LOG_PATH, log_file)

# Create a file handler that logs messages to a file
# The file handler will append to the file if it already exists
file_handler = logging.FileHandler(log_file_path, mode='a')

# Create a formatter to specify the log format
formatter = logging.Formatter(
    '{"asctime": "%(asctime)s", "service": "%(funcName)s", "levelname": "%(levelname)s", "message": "%(message)s", '
    '"detail": "[%(funcName)s:%(lineno)d]"}'
)

# Attach the formatter to the file handler
file_handler.setFormatter(formatter)

# Attach the file handler to the logger
logger.addHandler(file_handler)

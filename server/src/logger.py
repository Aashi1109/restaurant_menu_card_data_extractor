import json
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


# Custom formatter to handle exception details in JSON format
class JsonFormatter(logging.Formatter):
    def format(self, record):
        if record.funcName == '<module>':
            service_name = os.path.basename(record.pathname)
        else:
            service_name = record.funcName

        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "levelname": record.levelname,
            "service": service_name,
            "message": record.getMessage(),
            "detail": f"[{record.funcName}:{record.lineno}]"
        }

        # Check if the log record contains exception information
        if record.exc_info:
            exc_info = self.formatException(record.exc_info)
            log_record["message"] = exc_info.replace("\n", " ").replace('"', "'").replace(
                "^", ""
            )  # Format exception to a single line

        return json.dumps(log_record)


# Create and set the custom formatter
formatter = JsonFormatter()

# Attach the formatter to the file handler
file_handler.setFormatter(formatter)

# Attach the file handler to the logger
logger.addHandler(file_handler)

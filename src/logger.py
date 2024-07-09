# Importing necessary libraries:
import logging
import os
from datetime import datetime


LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE_NAME)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    logging.info("logging started")
    logging.info("logging completed")

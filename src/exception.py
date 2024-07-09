# Importing necessary libraries:
import sys
from logger import logging

# Creating a class to handle exceprion by inheriting Exception class:
class CustomException(Exception):

    def __init__(self, msg):
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        message = str(msg)
        self.error_message = (
            f"Error occured in Python script name: [{file_name}], "
            f"line number: [{line_number}] and error message: [{message}]"
        )

    def __str__(self) -> str:
        return self.error_message


if __name__ == "__main__":
    try:
        print("Hello")
        9 / 0
    except Exception as e:
        logging.info(CustomException(e))

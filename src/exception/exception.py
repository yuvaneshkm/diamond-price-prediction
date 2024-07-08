# Importing necessary libraries:
import sys


# function for custom exception message:
def error_message_detail(msg, error_detail) -> str:
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    message = str(msg)
    # Error Message:
    error_message = (
        "Error occured in Python script name: [{}], "
        "line number: [{}] and error message: [{}]"
    ).format(file_name, line_number, message)
    return error_message


# Creating a class to handle exceprion by inheriting Exception class:
class CustomException(Exception):
    # constructor:
    def __init__(self, msg, error_detail):

        super().__init__(msg)
        self.error_message = error_message_detail(msg, error_detail)

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        print("Hello")
        9 / "k"
    except Exception as e:
        print(CustomException(e, sys))

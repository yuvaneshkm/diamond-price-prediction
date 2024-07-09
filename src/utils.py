# Importing necessary libraries:
import os
import sys
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
import pickle



# saving whether a model or a preprocessing object:
def save_object(directory:Path, filename:str, object):
    try:
        directory = Path(directory)
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(object, f)
        f.close()
    except Exception as ex:
        logging.info(CustomException(ex))

# loading the model or preprocessing object:

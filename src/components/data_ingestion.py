# Importing necessary libraries:
import os
import sys
from pathlib import Path
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


# Inputs related to data_ingestion component:
@dataclass
class DataIngestionConfig:
    pass

class DataIngestion:

    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        try:
            pass
        except Exception as ex:
            logging.info(CustomException(ex))
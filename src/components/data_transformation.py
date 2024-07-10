# Importing necessary libraries:
import os
import sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle
import warnings
warnings.filterwarnings('ignore')


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:

    # Constructor:
    def __init__(self):
        pass


    # Get Data Transformation:
    def get_data_transformation(self):
        try:
            pass
        except Exception as ex:
            logging.info(CustomException(ex))


    # Initiate Data Transformation:
    def initiate_data_transformation(self, train_data_path, test_data_path):
        try:
            # loading train and test data:
            logging.info("Loading train and test data")
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            logging.info(f"Train DataFrame: \n {train_df.head()}")
            logging.info(f"Test DataFrame: \n {test_df.head()}")



            pass
        except Exception as ex:
            logging.info(CustomException(ex))
# Importing necessary libraries:
import os
import sys
from pathlib import Path
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor



@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')


# Model trainer:
class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, pre_train_df, pre_test_df):
        try:
            # Getting Transformed Train and Test Data:
            logging.info(f"Getting Transformed Train Data \n {pre_train_df.head()}")
            logging.info(f"Getting Transformed Test Data \n {pre_test_df.head()}")

            # Splitting Dependent dand Independent variables:
            X_train = pre_train_df.drop('price', axis=1)
            y_train = pre_train_df['price']
            X_test = pre_test_df.drop('price', axis=1)
            y_test = pre_test_df['price']

            models = {
                'decisiontree': DecisionTreeRegressor(),
                'randomforest': RandomForestRegressor(),
                'xgboost': XGBRegressor()
            }

            


            


        except Exception as ex:
            logging.info(CustomException(ex))

# Importing necessary libraries:
import os
from pathlib import Path
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from src.utils import model_trainer, save_object
import warnings

warnings.filterwarnings("ignore")


@dataclass
class ModelTrainerConfig:
    trained_model_file_name = "model.pkl"


# Model trainer:
class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(
        self, preprocessed_train_df: pd.DataFrame, raw_data_path: Path
    ):
        logging.info("Initiating Model Trainer")
        try:
            # Getting Transformed Train and Test Data:
            logging.info(
                f"Getting Transformed Train Data\n{preprocessed_train_df.head()}"
            )

            # Models to be used:
            models = {
                "linearregression": (LinearRegression(), {}),
                "lasso": (Lasso(), {"alpha": [0.1, 1.0, 10.0]}),
                "ridge": (Ridge(), {"alpha": [0.1, 1.0, 10.0]}),
                "elasticnet": (
                    ElasticNet(),
                    {"alpha": [0.1, 1.0, 10.0], "l1_ratio": [0.1, 0.5, 0.9]},
                ),
                "decisiontree": (
                    DecisionTreeRegressor(),
                    {"max_depth": [None, 10, 20, 30]},
                ),
                "randomforest": (
                    RandomForestRegressor(),
                    {"n_estimators": [10, 50, 100], "max_depth": [None, 10, 20, 30]},
                ),
                "xgboost": (
                    XGBRegressor(),
                    {"n_estimators": [10, 50, 100], "learning_rate": [0.01, 0.1, 0.2]},
                ),
            }
            logging.info(f"Training Different Models\nModels: {list(models.keys())}")

            # Report of all the models performance
            models_report = model_trainer(preprocessed_train_df, models, 10)
            logging.info(f"Models Performance Report:\n{models_report}")

            # choosing the best model:
            best_model_name = models_report.loc[0, "model_name"]
            logging.info(f"The best model is: {best_model_name}")
            best_model = models_report.loc[0, "model"]

            # saving the best model to the artifacts folder:
            logging.info("Saving the best model")
            directory = Path(os.path.dirname(raw_data_path))
            save_object(
                directory, self.model_trainer_config.trained_model_file_name, best_model
            )

        except Exception as ex:
            logging.info(CustomException(ex))

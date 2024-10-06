# Importing necessary libraries:
import os
from pathlib import Path
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from src.utils import model_trainer, save_object
import warnings

warnings.filterwarnings("ignore")


@dataclass
class ModelTrainerConfig:
    trained_model_path = os.path.join("artifacts", "model.pkl")


# Model trainer:
class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(
        self,
        preprocessed_train_df: pd.DataFrame,
        preprocessed_test_df: pd.DataFrame,
    ):
        logging.info("Model Training Initiated")
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
            }
            logging.info(f"Training Different Models\nModels: {list(models.keys())}")

            # Report of all the models performance
            models_report = model_trainer(
                preprocessed_train_df, preprocessed_test_df, models, 10
            )
            logging.info(f"Models Performance Report:\n{models_report}")

            # choosing the best model:
            best_model_name = models_report.loc[0, "model_name"]
            logging.info(f"The best model is: {best_model_name}")
            best_model = models_report.loc[0, "model"]

            # saving the best model to the artifacts folder:
            logging.info("Saving the best model")
            model_path = Path(self.model_trainer_config.trained_model_path)
            save_object(model_path, best_model)
            # 
            

        except Exception as ex:
            raise CustomException(ex)

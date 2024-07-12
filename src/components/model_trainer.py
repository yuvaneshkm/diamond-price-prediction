# Importing necessary libraries:
import os
from pathlib import Path
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from src.utils import evaluate_model, save_object
import warnings

warnings.filterwarnings("ignore")


@dataclass
class ModelTrainerConfig:
    trained_model_file_name = "model.pkl"


# Model trainer:
class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, pre_train_df, raw_data_path: Path):
        logging.info("Initiating Model Trainer")
        try:
            # Getting Transformed Train and Test Data:
            logging.info(f"Getting Transformed Train Data\n{pre_train_df.head()}")

            # Splitting train data into Dependent and Independent Variables:
            logging.info(
                "Splitting the Train data into Independent(X) and Dependent(y) Variables"
            )
            X = pre_train_df.drop("price", axis=1)
            y = pre_train_df["price"]

            # Splitting into Train and Validation datasets:
            logging.info("Splitting Train Data into Training and Validation set")
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=0.2, random_state=45
            )

            # Models to be used:
            models = {
                "linearregression": LinearRegression(),
                "lasso": Lasso(),
                "ridge": Ridge(),
                "elasticnet": ElasticNet(),
                "decisiontree": DecisionTreeRegressor(),
                "randomforest": RandomForestRegressor(),
                "xgboost": XGBRegressor(),
            }
            logging.info(f"Training Different Models\nModels: {list(models.keys())}")

            # Report of all the models performance
            models_report = evaluate_model(X_train, y_train, X_val, y_val, models)
            logging.info(f"Models Performance Report:\n{models_report}")

            # Finding the best model:
            logging.info("Finding the best model")
            best_model_name = (
                models_report.sort_values(by="r2_score", ascending=False)
                .reset_index(drop=True)
                .loc[0, "ModelName"]
            )
            best_model = (
                models_report.sort_values(by="r2_score", ascending=False)
                .reset_index(drop=True)
                .loc[0, "Model"]
            )
            logging.info(f"The Best Model is: {best_model_name}")

            # saving the best model:
            logging.info("Saving the best model as a pickle file in artifacts folder")
            directory = Path(os.path.dirname(raw_data_path))
            save_object(
                directory, self.model_trainer_config.trained_model_file_name, best_model
            )
            logging.info("Model Training Completed")

        except Exception as ex:
            logging.info(CustomException(ex))

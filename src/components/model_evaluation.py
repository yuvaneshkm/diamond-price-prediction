# Importing necessary libraries:
import os
from pathlib import Path
from typing import Tuple
import pandas as pd
import mlflow
import mlflow.sklearn
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class ModelEvaluation:

    def __init__(self):
        pass

    def evaluate_metrics(self, y_test, y_pred) -> Tuple[float, float, float]:
        """The Output of the method is
        (mean_squared_error, mean_absolute_error, r2_score)"""

        try:
            # mean squared error:
            logging.info("MSE calculated")
            MSE = mean_squared_error(y_test, y_pred)

            # mean absolute error:
            logging.info("MAE calculated")
            MAE = mean_absolute_error(y_test, y_pred)

            # r square value (accuracy):
            logging.info("R2_Score calculated")
            R2_Score = r2_score(y_test, y_pred)

        except Exception as ex:
            raise CustomException(ex)

        return (MSE, MAE, R2_Score)

    def initiate_model_evaluation(self, test_data: pd.DataFrame):
        logging.info("Model Evaluation Initiated")
        try:
            logging.info("Test data imported")
            X_test = test_data.drop("price")
            y_test = test_data["price"]

            # model path:
            script_dir = os.path.dirname(os.path.abspath(__name__))
            base_dir = os.path.abspath(os.path.join(script_dir, "../../"))
            model_path = Path(os.path.join(base_dir, "artifacts/model.pkl"))

            # loading the model:
            logging.info("Model imported")
            model = load_object(model_path)

            # parameters of the model:
            model_params = model.get_params()

            # set the registry uri:
            mlflow.set_registry_uri("")

            # start the mlflow run:
            with mlflow.start_run():

                # prediction of test data (X_test):
                logging.info("Predicting the test data (X_test values)")
                y_pred = model.predict(X_test)

                # calculating mse mae and r2_score:
                logging.info("Calculating MAE, MSE and R2_Score")
                (mse, mae, r2) = self.evaluate_metrics(y_test, y_pred)

                # logging the metrice:
                logging.info("Logging Metrics to MLflow")
                mlflow.log_metrics({"mse": mse, "mae": mae, "r2_score": r2})

                # logging the parameters:
                logging.info("Logging Model Parameters to MLflow")
                mlflow.log_params(model_params)

            pass
        except Exception as ex:
            raise CustomException(ex)

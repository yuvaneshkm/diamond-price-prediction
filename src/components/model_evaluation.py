# Importing necessary libraries:
import os
from pathlib import Path
from urllib.parse import urlparse
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
            MSE = mean_squared_error(y_test, y_pred)
            logging.info("MSE calculated")

            # mean absolute error:
            MAE = mean_absolute_error(y_test, y_pred)
            logging.info("MAE calculated")

            # r square value (accuracy):
            R2_Score = r2_score(y_test, y_pred)
            logging.info("R2_Score calculated")

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

            # prediction of test data (X_test):
            logging.info("Predicting the test data (X_test values)")
            y_pred = model.predict(X_test)

            # calculating mse mae and r2_score:
            logging.info("Calculating MAE, MSE and R2_Score")
            (mse, mae, r2) = self.evaluate_metrics(y_test, y_pred)

            # set the remote server uri for tracking and model registry:
            # remote_server_uri = ""
            # mlflow.set_tracking_uri(remote_server_uri)

            # start the mlflow run:
            with mlflow.start_run():

                # logging the metrice:
                logging.info("Logging Metrics to MLflow")
                mlflow.log_metrics({"mse": mse, "mae": mae, "r2_score": r2})

                # logging the parameters:
                logging.info("Logging Model Parameters to MLflow")
                mlflow.log_params(model_params)

                # type of the tracking uri:
                tracking_uri_type_store = urlparse(mlflow.get_tracking_uri()).scheme

                # model registry doesnot work with file source:
                if tracking_uri_type_store != "file":
                    mlflow.sklearn.log_model(
                        model, "model", registered_model_name="diamond-price-predictor"
                    )
                    logging.info("Registered the model")
                else:
                    mlflow.sklearn.log_model(model, "model")
                    logging.info("Logged the model")

        except Exception as ex:
            raise CustomException(ex)

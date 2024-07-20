# Importing necessary libraries:
import os
import sys
import mlflow
import mlflow.sklearn
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



class ModelEvaluation:

    def __init__(self):
        pass

    def evaluate_metrics(self, y_test, y_pred):

        # mean squared error:
        mse = mean_squared_error(y_test, y_pred)
        # mean absolute error:
        mae = mean_absolute_error(y_test, y_pred)
        # r square value (accuracy):
        r2 = r2_score(y_test, y_pred)

        return (mse, mae, r2)

    def initiate_model_evaluation(self):
        pass



if __name__=='__main__':
    pass
    print(os.path.abspath(__name__))
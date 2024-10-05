# importing necessary libraries:
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from src.components import (
    data_ingestion,
    data_transformation,
    model_trainer,
    model_evaluation,
)
from src.exception import CustomException
import warnings

warnings.filterwarnings("ignore")

# creating objects:
di_obj = data_ingestion.DataIngestion()
dt_obj = data_transformation.DataTransformation()
mt_obj = model_trainer.ModelTrainer()
me_obj = model_evaluation.ModelEvaluation()


# setting default arguments of the airflow:
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 10, 4),
    "email": ["yuvaneshkm05@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

# DAG:
with DAG(
    "diamond_price_prediction_training_pipeline",
    default_args=default_args,
    description="This is the Model training Pipeline",
    schedule="@weekly",
    catchup=False,
    tags=["Machine Learning", "Data Science"],
) as dag:

    """
    ## Diamond Price Prediction Training Pipeline
    This dag orchestrates the data ingestion, data transformation, model training and model evaluation steps for predicting diamond prices.
    """

    @task
    def start_data_ingestion():
        try:
            raw_data_path, train_data_path, test_data_path = (
                di_obj.initiate_data_ingestion()
            )
        except Exception as ex:
            raise CustomException(ex)
        return {
            "raw_path": raw_data_path,
            "train_path": train_data_path,
            "test_path": test_data_path,
        }

    @task
    def start_data_transformation(data_ingestion_artifact):
        try:
            raw_path = data_ingestion_artifact["raw_path"]
            train_path = data_ingestion_artifact["train_path"]
            test_path = data_ingestion_artifact["test_path"]
            preprocessed_train_df, preprocessed_test_df = (
                dt_obj.initiate_data_transformation(raw_path, train_path, test_path)
            )
        except Exception as ex:
            raise CustomException(ex)
        return {
            "pre_train_df": preprocessed_train_df,
            "pre_test_df": preprocessed_test_df,
        }

    @task
    def start_model_training(data_ingestion_artifact, data_transformation_artifact):
        try:
            raw_path = data_ingestion_artifact["raw_path"]
            pre_train_df = data_transformation_artifact["pre_train_df"]
            pre_test_df = data_transformation_artifact["pre_test_df"]
            mt_obj.initiate_model_training(pre_train_df, pre_test_df, raw_path)
        except Exception as ex:
            raise CustomException(ex)

    @task
    def start_model_evaluation(data_transformation_artifact):
        try:
            pre_test_df = data_transformation_artifact["pre_test_df"]
            me_obj.initiate_model_evaluation(pre_test_df)
        except Exception as ex:
            raise CustomException(ex)

    # defining the tasks:
    data_ingestion_task = start_data_ingestion()
    data_transformation_task = start_data_transformation(data_ingestion_task)
    model_training_task = start_model_training(
        data_ingestion_task, data_transformation_task
    )
    model_evaluation_task = start_model_evaluation(data_transformation_task)

    # task execution flow:
    (
        data_ingestion_task
        >> data_transformation_task
        >> model_training_task
        >> model_evaluation_task
    )

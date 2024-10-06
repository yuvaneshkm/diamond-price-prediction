# Importing necessary packages
from pathlib import Path
import pandas as pd
from src.exception import CustomException
from src.components import (
    data_ingestion,
    data_transformation,
    model_trainer,
    model_evaluation,
)
import warnings

warnings.filterwarnings("ignore")


class TrainingPipeline:

    # data ingestion:
    def start_data_ingestion(self):
        '''return (train_data_path, test_data_path)'''
        try:
            data_ingestion_obj = data_ingestion.DataIngestion()
            train_data_path, test_data_path = (
                data_ingestion_obj.initiate_data_ingestion()
            )
        except Exception as ex:
            raise CustomException(ex)
        return (train_data_path, test_data_path)

    # data transformation:
    def start_data_transformation(
        self, train_data_path: Path, test_data_path: Path
    ):
        '''return (preprocessed_train_df, preprocessed_test_df)'''
        try:
            data_transformation_obj = data_transformation.DataTransformation()
            preprocessed_train_df, preprocessed_test_df = (
                data_transformation_obj.initiate_data_transformation(
                    train_data_path, test_data_path
                )
            )
        except Exception as ex:
            raise CustomException(ex)
        return (preprocessed_train_df, preprocessed_test_df)

    # model training:
    def start_model_training(
        self,
        preprocessed_train_df: pd.DataFrame,
        preprocessed_test_df: pd.DataFrame,
    ):
        '''return model_path'''
        try:
            model_training_obj = model_trainer.ModelTrainer()
            model_path = model_training_obj.initiate_model_training(
                preprocessed_train_df, preprocessed_test_df
            )
        except Exception as ex:
            raise CustomException(ex)
        return model_path

    # model evaluation:
    def start_model_evaluation(self, preprocessed_test_data: pd.DataFrame, model_path: Path):
        try:
            model_evaluation_obj = model_evaluation.ModelEvaluation()
            model_evaluation_obj.initiate_model_evaluation(preprocessed_test_data, model_path)
        except Exception as ex:
            raise CustomException(ex)

    # start training:
    def start_training(self):
        try:
            train_path, test_path = self.start_data_ingestion()
            pre_train, pre_test = self.start_data_transformation(
                train_path, test_path
            )
            model_path = self.start_model_training(pre_train, pre_test)
            self.start_model_evaluation(pre_test, model_path)
        except Exception as ex:
            raise CustomException(ex)


if __name__ == "__main__":
    obj = TrainingPipeline()
    obj.start_training()

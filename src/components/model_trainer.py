# Importing necessary libraries:
import os
from pathlib import Path
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from src.utils import model_trainer, save_object, data_versioning
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
    ) -> Path:
        """The output of this method is model_path"""
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
            # versioning the model using dvc:
            data_versioning(str(model_path), "versioning_model_object")
            logging.info("Versioned the Model Object using DVC")

        except Exception as ex:
            raise CustomException(ex)

        return model_path


if __name__ == "__main__":
    from src.components import data_ingestion, data_transformation

    di_obj = data_ingestion.DataIngestion()
    train_data_path, test_data_path = di_obj.initiate_data_ingestion()

    dt_obj = data_transformation.DataTransformation()
    pre_train_df, pre_test_df = dt_obj.initiate_data_transformation(
        train_data_path, test_data_path
    )

    mt_obj = ModelTrainer()
    mt_obj.initiate_model_training(pre_train_df, pre_test_df)

# Importing necessary libraries:
import os
from typing import Tuple
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.utils import (
    numeric_categoric_columns,
    categoric_col_order,
    save_object,
    data_versioning,
)
import warnings

warnings.filterwarnings("ignore")


@dataclass
class DataTransformationConfig:
    preprocessor_obj_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    # Get Data Transformation:
    def get_data_transformer(self, train_data_path: Path):
        """This method will return the Preprocessing object"""

        try:
            # data transformation:
            logging.info("Creating Data Preprocessor")

            # get numeric and categoric columns:
            logging.info("Getting Numeric and Categoric columns")
            num_cols, cate_cols = numeric_categoric_columns(train_data_path)
            logging.info("Getting catrgorical columns order")
            cut_order, color_order, clarity_order = categoric_col_order()

            # Preprocessor Pipeline construction:
            logging.info("Constructing Preprocessor Pipeline")

            # Numeric Pipeline:
            num_step = [
                ("impute_missing", SimpleImputer(strategy="median")),
                ("feature_scaling", RobustScaler()),
            ]
            numeric_pipeline = Pipeline(num_step)
            logging.info("Numeric Pipeline Constructed")

            # Categoric Pipeline:
            cate_step = [
                ("impute_missing", SimpleImputer(strategy="most_frequent")),
                (
                    "encoding",
                    OrdinalEncoder(categories=[cut_order, color_order, clarity_order]),
                ),
            ]
            categoric_pipeline = Pipeline(cate_step)
            logging.info("Categoric Pipeline Constructed")

            # Final Preprocessor Pipeline:
            final_pre_step = [
                ("num_pre", numeric_pipeline, num_cols),
                ("cate_pre", categoric_pipeline, cate_cols),
            ]
            preprocessor = ColumnTransformer(final_pre_step, remainder="passthrough")
            preprocessor.set_output(transform="pandas")
            logging.info("Final Preprocessor Pipeline Constructed")

        except Exception as ex:
            raise CustomException(ex)

        return preprocessor

    # Initiate Data Transformation:
    def initiate_data_transformation(
        self, train_data_path: Path, test_data_path: Path
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        * The Output of the method is (preprocessed_train_df, preprocessed_test_df)"""

        logging.info("Data Transformation Started")
        try:
            # loading train and test data:
            logging.info("Loading train and test data")
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            logging.info(f"Train DataFrame:\n{train_df.head()}")
            logging.info(f"Test DataFrame:\n{test_df.head()}")

            # get preprocessing object:
            logging.info("Loading Preprocessor object")
            preprocessor_obj = self.get_data_transformer(train_data_path)
            logging.info("Preprocessor object Loaded")

            # Train data --> Dependent and Independent features:
            logging.info("Split Dependent and Independent variable of Train Data")
            X_train_df = train_df.drop("price", axis=1)
            y_train_df = train_df[["price"]]
            # Test data --> Dependent and Independent features:
            logging.info("Split Dependent and Independent variable of Test Data")
            X_test_df = test_df.drop("price", axis=1)
            y_test_df = test_df[["price"]]

            # preprocessing on test and train data:
            logging.info("Preprocess Train and Test data")

            # Train data:
            preprocessed_X_train_df = preprocessor_obj.fit_transform(X_train_df)
            preprocessed_train_df = pd.concat(
                [preprocessed_X_train_df, y_train_df], axis=1
            )
            logging.info(f"Preprocessed Train data\n{preprocessed_train_df.head()}")

            # Test data:
            preprocessed_X_test_df = preprocessor_obj.transform(X_test_df)
            preprocessed_test_df = pd.concat(
                [preprocessed_X_test_df, y_test_df], axis=1
            )
            logging.info(f"Preprocessed Test data\n{preprocessed_test_df.head()}")

            logging.info("Data Preprocessing completed")

            # save the preprocessor object in artifact folder:
            preprocessor_path = Path(
                self.data_transformation_config.preprocessor_obj_path
            )
            save_object(preprocessor_path, preprocessor_obj)
            logging.info("Saved the Preprocessor Object to the artifacts folder")

            # versioning the preprocessor object:
            data_versioning(str(preprocessor_path), "versioning_preprocessor_object")
            logging.info("Versioned the Preprocessor Object using DVC")

        except Exception as ex:
            raise CustomException(ex)

        return (preprocessed_train_df, preprocessed_test_df)


if __name__ == "__main__":
    from src.components import data_ingestion

    di_obj = data_ingestion.DataIngestion()
    train_path, test_path = di_obj.initiate_data_ingestion()
    obj = DataTransformation()
    obj.initiate_data_transformation(train_path, test_path)

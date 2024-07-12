# Importing necessary libraries:
import os
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.utils import numeric_categoric_columns, categoric_col_order, save_object
import warnings

warnings.filterwarnings("ignore")


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_name = "preprocessor.pkl"


class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    # Get Data Transformation:
    def get_data_transformer(self, raw_data_path: Path):
        try:
            # data transformation:
            logging.info("Data Preprocessing initiated")

            # get numeric and categoric columns:
            logging.info("Getting Numeric and Categoric columns")
            num_cols, cate_cols = numeric_categoric_columns(raw_data_path)
            logging.info("Catrgorical columns order")
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

            return preprocessor

        except Exception as ex:
            logging.info(CustomException(ex))

    # Initiate Data Transformation:
    def initiate_data_transformation(
        self, raw_data_path: Path, train_data_path: Path, test_data_path: Path
    ):
        try:
            # loading train and test data:
            logging.info("Loading train and test data")
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            logging.info(f"Train DataFrame: \n {train_df.head()}")
            logging.info(f"Test DataFrame: \n {test_df.head()}")

            # get preprocessing object:
            logging.info("Loading Preprocessor object")
            preprocessor_obj = self.get_data_transformer(raw_data_path)

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
            pre_X_train_df = preprocessor_obj.fit_transform(X_train_df)
            logging.info(f"Preprocessed Train data \n {pre_X_train_df.head()}")
            pre_X_test_df = preprocessor_obj.transform(X_test_df)
            logging.info(f"Preprocessed Test data \n {pre_X_test_df.head()}")

            # Final Preprocessed Train and Test data:
            pre_train_df = pd.concat([pre_X_train_df, y_train_df], axis=1)
            pre_test_df = pd.concat([pre_X_test_df, y_test_df], axis=1)

            # save the preprocessor object in artifact folder:
            directory = Path(os.path.dirname(raw_data_path))
            save_object(
                directory,
                self.data_transformation_config.preprocessor_obj_file_name,
                preprocessor_obj,
            )
            logging.info("Saved the Preprocessor Object at artifacts folder")

            return (pre_train_df, pre_test_df)

        except Exception as ex:
            logging.info(CustomException(ex))

# Importing necessary libraries:
import os
from typing import Tuple
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from dbsconnector import databases
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")


# Inputs related to data_ingestion component:
@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join("artifacts", "raw.csv")
    train_data_path = os.path.join("artifacts", "train.csv")
    test_data_path = os.path.join("artifacts", "test.csv")


class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> Tuple[str, str, str]:
        """
        * This method will ingest data from Google Drive and split data into
        Train and Test set and store the data in the artifacts folder.
        * The output of this method is a tuple of
        (raw_data_path, train_data_path, test_data_path)
        """

        logging.info("Data Ingestion Started")
        try:
            # Initializing mongodb connector:
            df = databases.load_gsheet("1TzMe3bHBVclnm-a7o-Yh9XqPLA9Hwr8NDC79w48mT38", "diamond_price_data")
            df.drop("id", axis=1, inplace=True)

            # creating artifact directory:
            parent_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))
            artifact_dir = os.path.join(
                parent_dir, os.path.dirname(self.ingestion_config.raw_data_path)
            )
            os.makedirs(artifact_dir, exist_ok=True)

            # saving raw data in artifacts folder:
            raw_df_path = os.path.join(parent_dir, self.ingestion_config.raw_data_path)
            df.to_csv(raw_df_path, index=False)
            logging.info("Saved raw data in artifact folder")

            # train test split:
            logging.info("Performing train test split")
            train_df, test_df = train_test_split(df, test_size=0.25, random_state=25)

            # saving train data in artifacts folder:
            train_df_path = os.path.join(
                parent_dir, self.ingestion_config.train_data_path
            )
            train_df.to_csv(train_df_path, index=False)
            logging.info("Saved train data in artifact folder")

            # saving test data in artifacts folder:
            test_df_path = os.path.join(
                parent_dir, self.ingestion_config.test_data_path
            )
            test_df.to_csv(test_df_path, index=False)
            logging.info("Saved test data in artifact folder")

            logging.info("Data Ingestion Completed")

        except Exception as ex:
            raise CustomException(ex)

        return (raw_df_path, train_df_path, test_df_path)

# Importing necessary libraries:
import os
from typing import Tuple
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from dbsconnector import databases
from sklearn.model_selection import train_test_split
import warnings
from pathlib import Path

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
            df = databases.load_mongodbdata(
                host="localhost", database="diamond-price-data", collection="raw-data"
            )
            df.drop("id", axis=1, inplace=True)

            # Ensuring the artifacts directory exists:
            artifact_dir = Path(self.ingestion_config.raw_data_path).parent
            artifact_dir.mkdir(parents=True, exist_ok=True)

            # Saving raw data in artifacts folder:
            raw_df_path = Path(self.ingestion_config.raw_data_path)
            df.to_csv(raw_df_path, index=False)
            logging.info(f"Saved raw data to {raw_df_path}")

            # Performing train test split:
            logging.info("Performing train test split")
            train_df, test_df = train_test_split(df, test_size=0.3, random_state=45)

            # Saving train data in artifacts folder:
            train_df_path = Path(self.ingestion_config.train_data_path)
            train_df.to_csv(train_df_path, index=False)
            logging.info(f"Saved train data to {train_df_path}")

            # Saving test data in artifacts folder:
            test_df_path = Path(self.ingestion_config.test_data_path)
            test_df.to_csv(test_df_path, index=False)
            logging.info(f"Saved test data to {test_df_path}")

            logging.info("Data Ingestion Completed")

        except Exception as ex:
            raise CustomException(ex)

        return (str(raw_df_path), str(train_df_path), str(test_df_path))


if __name__=="__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
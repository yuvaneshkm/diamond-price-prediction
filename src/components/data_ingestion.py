# Importing necessary libraries:
import os
from typing import Tuple
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from mdb_connect_pkg import mongo_crud
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
        * This method will ingest data from MongoDB database and split data into
        Train and Test set and store the data in the artifacts folder.
        * The output of this method is a tuple of
        (raw_data_path, train_data_path, test_data_path)
        """

        logging.info("Data Ingestion Started")
        try:
            # Initializing mongodb connector:
            logging.info("Initializing mongodb connector")
            URL = "mongodb://localhost:27017"
            DATABASE_NAME = "projectdb"
            COLLECTION_NAME = "diamond_price_data"
            mongo = mongo_crud.MongoDBConnection(URL, DATABASE_NAME, COLLECTION_NAME)

            # Creating mongodb client:
            logging.info("Creating mongodb client")
            mongo.create_mongo_client()
            mongo.database_()
            mongo.collection_()

            # Loading data from mongodb:
            logging.info("Loading data from mongodb")
            df = mongo.load_data()
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
            train_df, test_df = train_test_split(df, test_size=0.3, random_state=21)

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
            logging.info(CustomException(ex))

        return (raw_df_path, train_df_path, test_df_path)


if __name__ == "__main__":
    obj = DataIngestion()
    print(obj.initiate_data_ingestion())

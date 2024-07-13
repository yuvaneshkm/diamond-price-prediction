# Importing necessary libraries:
import os
from pathlib import Path
from typing import List, Tuple
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import pickle
# from sklearn.model_selection import KFold, cross_val_score


# saving whether a model or a preprocessing object:
def save_object(directory: Path, filename: str, object):
    """This function will save ML model and Preprocessing object as a pickle file"""
    try:
        directory = Path(directory)
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as file_obj:
            pickle.dump(object, file_obj)
        file_obj.close()
    except Exception as ex:
        logging.info(CustomException(ex))


# loading the model or preprocessing object:
def load_object(filepath: Path):
    """This function will load the ML model and Preprocessing object"""
    try:
        filepath = Path(filepath)
        with open(filepath, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as ex:
        logging.info(CustomException(ex))


# numeric and categoric columns:
def numeric_categoric_columns(raw_data_path: Path) -> Tuple[List[str], List[str]]:
    """
    * This function will give list of all the Numeric and Categoric columns in the dataset
    * The Output of the function is (numeric_col, categoric_col)"""
    # reading raw data:
    raw_df = pd.read_csv(raw_data_path)
    raw_df.drop("price", axis=1, inplace=True)
    # numeric and categoric columns:
    numeric_col = []
    categoric_col = []
    for col in raw_df.columns:
        if raw_df[col].dtype == "object":
            categoric_col.append(col)
        else:
            numeric_col.append(col)
    # returning numeric and categoric columns:
    return (numeric_col, categoric_col)


# categoric columns order:
def categoric_col_order() -> Tuple[List[str], List[str], List[str]]:
    """
    * This function will give the order of weight of items present in the categoric columns.
    * Order of the output: ([cut_order], [color_order], [clarity_order])"""

    cut_order = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
    color_order = ["J", "I", "H", "G", "F", "E", "D"]
    clarity_order = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

    return (cut_order, color_order, clarity_order)

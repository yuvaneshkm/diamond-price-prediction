# Importing necessary libraries:
import os
import sys
from pathlib import Path
from typing import List
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


def predict(diamond_data: pd.DataFrame):

    # path of the preprocessor and the model:
    preprocessor_path = Path(
        os.path.abspath(os.path.join(os.getcwd(), "../../artifacts/preprocessor.pkl"))
    )
    model_path = Path(
        os.path.abspath(os.path.join(os.getcwd(), "../../artifacts/model.pkl"))
    )

    # loading the preprocessor and the model:
    preprocessor = load_object(preprocessor_path)
    model = load_object(model_path)

    preprocessed_features = preprocessor.transform(diamond_data)
    price = model.predict(preprocessed_features)

    return price


def custom_data(
    carat: float,
    depth: float,
    table: float,
    x: float,
    y: float,
    z: float,
    cut: object,
    color: object,
    clarity: object
) -> pd.DataFrame:

    diamond_details = {
        "carat": [carat],
        "cut": [cut],
        "color": [color],
        "clarity": [clarity],
        "depth": [depth],
        "table": [table],
        "x": [x],
        "y": [y],
        "z": [z]
    }
    diamond_details_df = pd.DataFrame(diamond_details)

    return diamond_details_df

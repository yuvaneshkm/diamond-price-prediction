# Importing necessary libraries:
import os
from pathlib import Path
from typing import List, Tuple
from src.exception import CustomException
import pandas as pd
import pickle
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


# saving whether a model or a preprocessing object:
def save_object(directory: Path, filename: str, object):
    """This function will save ML model and Preprocessing object as a pickle file"""
    try:
        directory = Path(directory)
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as file_obj:
            pickle.dump(object, file_obj)
    except Exception as ex:
        raise CustomException(ex)


# loading the model or preprocessing object:
def load_object(filepath: Path):
    """This function will load the ML model and Preprocessing object"""
    try:
        with open(filepath, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as ex:
        raise CustomException(ex)


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


# Training different ML models and finding the best suit model for the data:
def model_trainer(
    train_data: pd.DataFrame, test_data: pd.DataFrame, models: dict, n_splits: int
) -> pd.DataFrame:
    """
    * This function will train different models and create a
    performance dataframe of all the models
    * Output is a dataframe with columns
    [model_name, model, train_R2Score(train_accuracy), R2Score(test_accuracy), MSE, MAE]
    """

    # kfold cross validation:
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=45)

    trained_model_name_list = []
    trained_model_list = []
    train_r2score_list = []
    r2score_list = []
    mse_list = []
    mae_list = []

    X_test = test_data.drop("price", axis=1)
    y_test = test_data["price"]

    for train_index, val_index in kfold.split(train_data):
        train, validation = train_data.iloc[train_index], train_data.iloc[val_index]

        X_train = train.drop("price", axis=1)
        y_train = train["price"]
        X_val = validation.drop("price", axis=1)
        y_val = validation["price"]

        for name, (model, params) in models.items():
            if params:
                grid_search = GridSearchCV(
                    estimator=model, param_grid=params, scoring="r2"
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_
            else:
                model.fit(X_train, y_train)
                best_model = model

            y_val_pred = best_model.predict(X_val)
            train_R2 = r2_score(y_val, y_val_pred)

            y_test_pred = best_model.predict(X_test)
            R2_ = r2_score(y_test, y_test_pred)
            mse_ = mean_squared_error(y_test, y_test_pred)
            mae_ = mean_absolute_error(y_test, y_test_pred)

            trained_model_name_list.append(name)
            trained_model_list.append(best_model)
            train_r2score_list.append(train_R2)
            r2score_list.append(R2_)
            mse_list.append(mse_)
            mae_list.append(mae_)

    performance = pd.DataFrame()
    performance["model_name"] = trained_model_name_list
    performance["model"] = trained_model_list
    performance["R2Score"] = r2score_list
    performance["MSE"] = mse_list
    performance["MAE"] = mae_list

    performance_df = performance.sort_values(by="R2Score", ascending=False).reset_index(
        drop=True
    )

    return performance_df

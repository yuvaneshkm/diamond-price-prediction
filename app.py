# importing necessary libraries:
import streamlit as st
from src.utils import categoric_col_order
from src.exception import CustomException
from src.logger import logging
from src.pipeline.prediction_pipeline import DataPreparation, PredictionPipeline


# ---------------------- frontent application ----------------------
# page configuration:
st.set_page_config(page_title="diamond-price-predictor", page_icon="💎")

# title:
st.title("💎 Diamond Price Predictor")

# elements of categoric columns:
cut_order, color_order, clarity_order = categoric_col_order()

# Form for data collection from the user:
st.subheader("Diamond Details")
form = st.form("Diamond Details")
with form:
    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        carat = st.number_input("Diamond Carat")
        clarity = st.selectbox("Diamond Clarity", clarity_order)
        x = st.number_input("Dimension X")
    with col2:
        cut = st.selectbox("Diamond Cut", cut_order)
        depth = st.number_input("Diamond Depth")
        y = st.number_input("Dimension Y")
    with col3:
        color = st.selectbox("Diamond Color", color_order)
        table = st.number_input("Diamond Table")
        z = st.number_input("Dimension Z")

    if st.form_submit_button("Predict Price"):
        try:
            details = DataPreparation(
                float(carat),
                str(cut),
                str(color),
                str(clarity),
                float(depth),
                float(table),
                float(x),
                float(y),
                float(z),
            )
            details_df = details.custom_data()

            pred_price = PredictionPipeline()
            price = pred_price.predict(details_df)

            st.success(f"Predicted Price of the Diamond: $ {price[0]:,.2f}")

        except Exception as ex:
            logging.info(CustomException(ex))

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

col1, col2, col3 = st.columns(3, gap="small")

with col1:
    carat = st.number_input("Diamond Carat", min_value=0.00, max_value=5.00, step=0.1)
    clarity = st.selectbox("Diamond Clarity", clarity_order)
    x = st.number_input("Dimension X", min_value=0.00, max_value=12.00, step=0.01)
with col2:
    cut = st.selectbox("Diamond Cut", cut_order)
    depth = st.number_input("Diamond Depth", min_value=40.00, max_value=80.00, step=0.1)
    y = st.number_input("Dimension Y", min_value=0.00, max_value=12.00, step=0.01)
with col3:
    color = st.selectbox("Diamond Color", color_order)
    table = st.number_input("Diamond Table", min_value=40, max_value=85, step=1)
    z = st.number_input("Dimension Z", min_value=0.00, max_value=32.00, step=0.01)


if st.button("Predict Price"):
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

        if price is not None:
            st.success(f"Predicted Price: ${price[0]:,.2f}")
        else:
            st.error(
                "Failed to predict the price. Please check the logs for more details."
            )

    except Exception as ex:
        logging.info(CustomException(ex))

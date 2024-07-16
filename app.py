# importing necessary libraries:
import streamlit as st
from src.utils import categoric_col_order
from src.pipeline.prediction_pipeline import custom_data, predict


# ---------------------- frontent application ----------------------
# page configuration:
st.set_page_config(
    page_title = "diamond-price-predictor",
    page_icon = "💎"
)

# title:
st.title("💎 Diamond Price Predictor")

# elements of categoric columns:
cut_order, color_order, clarity_order= categoric_col_order()

# Form for data collection from the user:
st.subheader("Diamond Details")
data_form = st.form("Diamond Details", clear_on_submit=False)


col1, col2, col3 = st.columns(3, gap="small")

with col1:
    carat = st.number_input('Diamond Carat', min_value=0.00, max_value=5.00, step=0.1)
    x = st.number_input("Dimension X", min_value=0.00, max_value=12.00, step=0.01)
    cut = st.selectbox("Diamond Cut", cut_order)
with col2:
    depth = st.number_input('Diamond Depth', min_value=40.00, max_value=80.00, step=0.1)
    y = st.number_input("Dimension Y", min_value=0.00, max_value=12.00, step=0.01)
    color = st.selectbox("Diamond Color", color_order)
with col3:
    table = st.number_input('Diamond Table', min_value=40, max_value=85, step=1)
    z = st.number_input("Dimension Z", min_value=0.00, max_value=32.00, step=0.01)
    clarity = st.selectbox("Diamond Clarity", clarity_order)

prediction = st.button("Predict")

if prediction:
    diamond_detail = custom_data(
            float(carat), float(depth), float(table), float(x), 
            float(y), float(z), cut, color, clarity
        )

    predicted_price = predict(diamond_detail)
    st.write(predicted_price)


st.markdown("---")
c1,c2,c3 = st.columns(3, gap="large")
c2.write("@yuvaneshkm")

# 💎 Diamond Price Prediction 💎
This project predicts diamond prices using machine learning models. The project workflow involves data ingestion, exploration, experimentation, and deployment using modular code organization, MLOps tools, and a Dockerized application.

# Project Overview

## Data Ingestion: 
The initial data was sourced from a MongoDB database. Data exploration and experimentation were conducted using Jupyter Notebook.

## Exploratory Data Analysis (EDA): 
Detailed analysis to understand the data distribution, key patterns, and insights.

## Model Experimentation:
- **Models tested:** Linear Regression, Lasso Regression, Ridge Regression, and ElasticNet.
- Lasso Regression achieved the highest accuracy of 93%.
- Various hyperparameters and cross-validation techniques were applied to optimize each model.

## Modular ML Code Organization:
- **Data Ingestion:** Handling and versioning input data.
- **Data Transformation:** Data cleaning and feature engineering.
- **Model Training:** Training and optimizing models.
- **Model Evaluation:** Evaluating and selecting the best model.
- Source code management was done using **Git**, and **DVC** was used for data versioning.
- **MLflow** was used for tracking parameters, metrics, and model registry. The final Lasso model is registered in the **MLflow Model Registry**.

## Pipelines:
- **Training Pipeline:** Automated workflow for data ingestion, transformation, and model training.
- **Prediction Pipeline:** Pipeline for model inference.

## User Interface (UI):
- A user-friendly web UI built with HTML and CSS.
- Developed a Flask app to serve the UI and prediction functionalities.

## Dockerized Deployment:
- The Flask app was Dockerized and pushed to Docker Hub.

## To pull and run the Docker image:
```bash
docker pull yuvaneshkm05/diamond-price-predictor
docker run -d -p 5000:5000 yuvaneshkm05/diamond-price-predictor
```
- After running, visit http://localhost:5000 to access the Diamond Price Predictor app.

## Demo:
### User Input
![User Input](https://github.com/yuvaneshkm/diamond-price-prediction/blob/main/images/uese_input.png)
### Result
![User Input](https://github.com/yuvaneshkm/diamond-price-prediction/blob/main/images/result.png)


# Project Impact:

## Informed Pricing for Jewelers and Retailers
- By predicting diamond prices accurately, jewelers and retailers can set competitive, data-driven prices. This helps them avoid undervaluing high-quality stones or overpricing lower-quality ones, resulting in better profit margins and customer satisfaction.

## Transparency and Trust for Customers
- The model helps create transparency in pricing by basing predictions on objective factors (cut, clarity, carat, etc.), reducing the subjectivity often associated with diamond valuation.
- Customers benefit from consistent, fair pricing, which fosters trust and loyalty to the retailer or brand.

## Enhanced Online Diamond Marketplaces
- For e-commerce platforms specializing in diamonds, this model can integrate seamlessly to provide instant price predictions for listed diamonds, enhancing the shopping experience for customers.

In summary, the Diamond Price Prediction project can transform the diamond industry by making pricing more transparent, accessible, and data-driven, while also setting a benchmark for using machine learning in luxury goods pricing and inventory management. This real-world impact makes it a valuable tool for businesses, consumers, and investors alike.

---
This project demonstrates the end-to-end implementation of a machine learning solution, including MLOps practices and Dockerized deployment for scalable and reproducible results.
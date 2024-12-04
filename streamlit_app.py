import pandas as pd
import streamlit as st
from datarobot import Client
from datarobot.client import set_client
import datarobot as dr
import matplotlib.pyplot as plt
from constants import *
from utils import initiate_session_state
import seaborn as sns
import tempfile
import os
# from dotenv import load_dotenv

# load_dotenv()

# Basic application page configuration, modify values in `constants.py`
st.set_page_config(page_title=I18N_APP_NAME, page_icon=APP_FAVICON, layout="wide",
                   initial_sidebar_state=SIDEBAR_DEFAULT_STATE)

# st.set_page_config(layout="wide")

def start_streamlit():
    # initiate_session_state()

    # Setup DR client
    # set_client(Client(token=st.session_state.token, endpoint=st.session_state.endpoint))
    # set_client(Client(token=st.session_state.token, endpoint=st.session_state.endpoint))

    st.logo(APP_LOGO)
    st.header('Gasoline Price Predictor')
    st.text(
        'Welcome to the Gasoline Price Predictor! This Streamlit application allows users to predict '
        'and analyze gasoline prices based on historical data and machine learning insights. '
        'Get started by uploading your data to see predictions and visualizations.'
    )


if __name__ == "__main__":
    start_streamlit()

dr.Client(
    endpoint="https://app.datarobot.com/api/v2",
    token="Njc0ZTk3NzkwMmZlZWJhZmRjNzk2YTA3OkNvOTNUR3Nsek9RaGxwUllHZVJ6QlMxSjVCeFE5TFg4b2lmdURyQU1CWDg9",
)

# dr.Client(
#     endpoint=st.secrets["DATAROBOT_API_ENDPOINT"],
#     token=st.secrets["DATAROBOT_API_TOKEN"],
# )

# dr.Client(
#     endpoint=os.getenv("DATAROBOT_API_ENDPOINT"),
#     token=os.getenv("DATAROBOT_API_TOKEN"),
# )

# deployment_id = "674eb2d6b41d83844bb2316d"



# deployment_id = "6746e98f6f60d517726b32cd"

deployment_id = st.secrets["DEPLOYMENT_ID"]

# deployment_id = os.getenv("DEPLOYMENT_ID")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv') as temp_input_file:
        # Write the uploaded content into the temporary file
        temp_input_file.write(uploaded_file.getvalue().decode('utf-8'))
        temp_input_file_path = temp_input_file.name

        # Read the CSV file into a pandas DataFrame (for preview or processing)
        df = pd.read_csv(temp_input_file_path)
        
        # Display the uploaded file
        st.write("Data Preview:")
        st.dataframe(df)

        # Output file
        output_file = "predicted.csv"

        # Replace input_file with the temporary file path
        job = dr.BatchPredictionJob.score_to_file(
            deployment_id,
            temp_input_file_path,  # Use the temp file as input
            output_file,
            passthrough_columns_set="all"
        )

        st.write("Started scoring...", job)
        job.wait_for_completion()

        st.write("Prediction job completed!")
        st.write(job)


try:
    # Read the CSV file
    data = pd.read_csv(output_file)
    
    # Extract the actual and predicted columns
    date= "Date"
    actual_col = "U_S_ Regular Gasoline Through Company Outlets Price by All Sellers (Dollars per Gallon)"
    predicted_col = "U_S_ Total Gasoline Through Company Outlets Price by All Sellers (Dollars per Gallon)_PREDICTION"
    
    # Check if required columns exist
    if date in data.columns and actual_col in data.columns and predicted_col in data.columns:
        
        # st.write("Data Preview:")
        # st.dataframe(data[[date,actual_col, predicted_col]])
        
        # # Create a line chart
        # st.write("Line Chart: Actual vs Predicted Gasoline Prices")
        # fig, ax = plt.subplots(figsize=(10, 6))
        # ax.plot(data[actual_col], label="Actual Price", color="blue")
        # ax.plot(data[predicted_col], label="Predicted Price", color="orange")
        # ax.set_title("Actual vs Predicted Gasoline Prices")
        # ax.set_xlabel("Index")
        # ax.set_ylabel("Price (Dollars per Gallon)")
        # ax.legend()
        # st.pyplot(fig)

        columns_to_plot = [
            "U_S_ Finished Motor Gasoline Stocks at Refineries, Bulk Terminals, and Natural Gas Plants (Thousand Barrels)",
            "U_S_ Reformulated Motor Gasoline Stocks at Refineries, Bulk Terminals, and Natural Gas Plants (Thousand Barrels)",
            "U_S_ Conventional Motor Gasoline Stocks at Refineries, Bulk Terminals, and Natural Gas Plants (Thousand Barrels)",
            "U_S_ Total Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
            "U_S_ Regular Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
            "U_S_ Gasoline Midgrade All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
            "U_S_ Premium Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
            "U_S_ Aviation Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
            "U_S_ Kerosene_Type Jet Fuel All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
            "U_S_ Total Gasoline Through Company Outlets Price by All Sellers (Dollars per Gallon)",
            "U_S_ Regular Gasoline Through Company Outlets Price by All Sellers (Dollars per Gallon)",
            "U_S_ Gasoline Midgrade Through Company Outlets Price by All Sellers (Dollars per Gallon)",
            "U_S_ Premium Gasoline Through Company Outlets Price by All Sellers (Dollars per Gallon)",
            "U_S_ Aviation Gasoline Retail Sales by Refiners (Dollars per Gallon)",
        ]


        st.header("Gasoline Price Predictor Dashboard")
        st.subheader("Data Preview:")
        # st.dataframe(data[[date, actual_col, predicted_col]])
        st.dataframe(data[[date,actual_col,predicted_col]])
        
        # KPI Cards
        st.subheader("Key Performance Indicators (KPIs):")
        avg_actual = data[actual_col].mean()
        avg_predicted = data[predicted_col].mean()
        mae = (data[actual_col] - data[predicted_col]).abs().mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Actual Price", f"${avg_actual:.2f}")
        col2.metric("Average Predicted Price", f"${avg_predicted:.2f}")
        col3.metric("Mean Absolute Error (MAE)", f"${mae:.2f}")
        
        col1, col2 = st.columns(2)
        # Line Chart: Actual vs Predicted Prices
        with col1:
            st.subheader("Line Chart: Actual vs Predicted Gasoline Prices")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data[date], data[actual_col], label="Actual Price", color="blue", marker='o')
            ax.plot(data[date], data[predicted_col], label="Predicted Price", color="orange", linestyle='--', marker='x')
            ax.set_title("Actual vs Predicted Gasoline Prices")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (Dollars per Gallon)")
            ax.legend()
            st.pyplot(fig)
            st.write("This line chart compares the Actual Prices and Predicted Prices of gasoline over time, helping identify trends and discrepancies. The blue line represents actual prices, while the orange dashed line shows predictions, enabling performance evaluation of the predictive model.")
        
        with col2:
            # Residuals Plot
            st.subheader("Residual Plot (Prediction Errors)")
            residuals = data[actual_col] - data[predicted_col]
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x=data[date], y=residuals, ax=ax, color="red")
            ax.axhline(0, color="black", linestyle="--", linewidth=1)
            ax.set_title("Residuals Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Residuals (Actual - Predicted)")
            st.pyplot(fig)
            st.write("The residual plot visualizes the prediction errors (difference between actual and predicted prices) over time. Points above or below the zero line indicate overprediction or underprediction, highlighting the accuracy and bias of the model.")

        # Comparison Heatmap
        st.subheader("Correlation Heatmap of Selected Columns")
        filtered_data = data[columns_to_plot]
        filtered_data = filtered_data.dropna()  # Remove missing values for heatmap
        corr_matrix = filtered_data.corr()

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)
        st.write("The correlation heatmap displays the relationships between selected columns, with color intensity indicating the strength of correlation. Positive correlations are shown in warmer colors, while negative correlations appear cooler, helping to identify patterns and dependencies between variables.")
            
        # Distribution Plot
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Distribution of Actual vs Predicted Prices")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data[actual_col], label="Actual Price", color="blue", kde=True, ax=ax)
            sns.histplot(data[predicted_col], label="Predicted Price", color="orange", kde=True, ax=ax)
            ax.set_title("Distribution of Prices")
            ax.set_xlabel("Price (Dollars per Gallon)")
            ax.set_ylabel("Frequency")
            ax.legend()
            st.pyplot(fig)
            st.write("This distribution plot compares the actual and predicted gasoline prices, showing their frequency distributions. The blue curve represents actual prices, while the orange curve shows predicted prices, with the overlayed KDE indicating the overall price trends.")
            
        # Heatmap: Correlation Matrix
        # st.subheader("Correlation Heatmap")
        # corr_data = data[[actual_col, predicted_col]].corr()
        # fig, ax = plt.subplots(figsize=(8, 6))
        # sns.heatmap(corr_data, annot=True, cmap="coolwarm", ax=ax)
        # ax.set_title("Correlation Between Actual and Predicted Prices")
        # st.pyplot(fig)


        # # Loop through columns and create line charts
        # for col in columns_to_plot:
        #     if col in data.columns:
        #         st.subheader(f"{col} Over Time")
        #         fig, ax = plt.subplots(figsize=(10, 6))
        #         ax.plot(data[date], data[col], label=col, color="green", marker="o")
        #         ax.set_title(f"{col} Over Time")
        #         ax.set_xlabel("Date")
        #         ax.set_ylabel("Value")
        #         ax.legend()
        #         st.pyplot(fig)

        

        # Top Categories Bar Chart (Example)
        with col2:
            st.subheader("Top Gasoline Sales/Deliveries by Type")
            top_sales_columns = [
                "U_S_ Total Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
                "U_S_ Regular Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
                "U_S_ Gasoline Midgrade All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
                "U_S_ Premium Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
                "U_S_ Aviation Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)",
            ]

            avg_sales = {col: data[col].mean() for col in top_sales_columns if col in data.columns}
            avg_sales = sorted(avg_sales.items(), key=lambda x: x[1], reverse=True)

            # Bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            sales_categories, sales_values = zip(*avg_sales)
            ax.barh(sales_categories, sales_values, color="skyblue")
            ax.set_title("Average Sales/Deliveries by Type (Thousand Gallons per Day)")
            ax.set_xlabel("Thousand Gallons per Day")
            ax.set_ylabel("Fuel Type")
            st.pyplot(fig)
            st.write("This bar chart compares the average sales or deliveries of various gasoline types by prime suppliers. The fuel types are listed on the vertical axis, while the horizontal axis represents the average amount sold or delivered (in thousand gallons per day), with the chart sorted by sales volume.")


    
except FileNotFoundError:
    st.error("The specified file could not be found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {e}")


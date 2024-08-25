import streamlit as st
import pandas as pd
from scripts.model import train_model, predict
from scripts.visualization import create_scatter_plot, create_line_chart, create_bar_chart, create_heatmap

# Initialize Streamlit app
st.title("DataSage: AI-Powered Business Intelligence Dashboard")

# Sidebar for user controls
st.sidebar.header("Settings")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV data file", type=["csv"])

if uploaded_file is not None:
    # Load and process data
    data = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.write(data.head())

    # Display data summary
    st.write("### Data Summary")
    st.write(data.describe())
    
    # Missing values summary
    st.write("### Missing Values Summary")
    st.write(data.isnull().sum())

    # Feature and target selection
    columns = data.columns.tolist()
    st.sidebar.header("Feature and Target Selection")
    feature_columns = st.sidebar.multiselect("Select Feature Columns", options=columns)
    target_column = st.sidebar.selectbox("Select Target Column", options=columns)
    
    # Model selection
    st.sidebar.header("Model Selection")
    model_type = st.sidebar.selectbox("Select Model Type", ["RandomForest", "LinearRegression", "HistGradientBoosting"])
    
    # Model parameters input
    model_params = {}
    if model_type == "RandomForest":
        n_estimators = st.sidebar.number_input("Number of Estimators", value=100)
        max_depth = st.sidebar.number_input("Max Depth", value=None)
        model_params = {"n_estimators": n_estimators, "max_depth": max_depth}
    elif model_type == "LinearRegression":
        # LinearRegression does not have additional parameters in this context
        pass
    elif model_type == "HistGradientBoosting":
        max_iter = st.sidebar.number_input("Max Iterations", value=100)
        model_params = {"max_iter": max_iter}
    
    # Train model
    if st.sidebar.button("Train Model"):
        if not feature_columns or target_column not in data.columns:
            st.error("Please select valid feature and target columns.")
        else:
            try:
                mse, model_path = train_model(data, feature_columns, target_column, model_type, model_params)
                st.write(f"Model Training Complete. Mean Squared Error: {mse:.2f}")
                st.write(f"Model saved to {model_path}")
            except Exception as e:
                st.error(f"Error during model training: {e}")

    # Make predictions
    if st.sidebar.button("Make Predictions"):
        if not feature_columns or target_column not in data.columns:
            st.error("Please select valid feature and target columns.")
        else:
            try:
                model_path = f'models/{model_type.lower()}.pkl'
                predictions = predict(data, feature_columns, model_path)
                data['Predictions'] = predictions
                st.write("### Predictions")
                st.write(data[[feature_columns[0], 'Predictions']])
                
                # Visualization of predictions
                st.write("### Predictions vs Feature")
                st.scatter_chart(data[[feature_columns[0], 'Predictions']])
            except Exception as e:
                st.error(f"Error during prediction: {e}")

    # Visualization options
    st.sidebar.header("Visualization Options")
    if columns:
        chart_type = st.sidebar.selectbox("Choose chart type", ["None", "Scatter Plot", "Line Chart", "Bar Chart", "Correlation Heatmap"])
        if chart_type:
            try:
                if chart_type == "Scatter Plot" and len(feature_columns) == 2:
                    fig = create_scatter_plot(data, feature_columns[0], feature_columns[1])
                elif chart_type == "Line Chart" and len(feature_columns) == 2:
                    fig = create_line_chart(data, feature_columns[0], feature_columns[1])
                elif chart_type == "Bar Chart" and len(feature_columns) == 2:
                    fig = create_bar_chart(data, feature_columns[0], feature_columns[1])
                elif chart_type == "Correlation Heatmap":
                    fig = create_heatmap(data)
                else:
                    st.warning("Select exactly two columns for the selected chart type.")
                    fig = None
                
                if fig:
                    st.write("### Data Visualization")
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Error during visualization: {e}")

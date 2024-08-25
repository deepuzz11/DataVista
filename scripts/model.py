import pandas as pd
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

def preprocess_data(df, feature_columns, target_column=None):
    """Preprocess the data including missing value imputation and feature scaling."""
    # Handle missing values in features
    imputer = SimpleImputer(strategy='mean')
    df[feature_columns] = imputer.fit_transform(df[feature_columns])
    
    if target_column:
        # Handle missing values in target
        if df[target_column].isnull().any():
            df = df.dropna(subset=[target_column])  # Drop rows where target is NaN

        y = df[target_column]
        X = df[feature_columns]
    else:
        X = df[feature_columns]
        y = None

    # Scale features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    return X, y

def train_model(df, feature_columns, target_column, model_type='RandomForest', model_params=None):
    """Train a regression model and save it."""
    X, y = preprocess_data(df, feature_columns, target_column)
    
    if y is None or len(y) == 0:
        raise ValueError("Target column is missing or contains only NaN values after preprocessing.")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the model
    if model_type == 'RandomForest':
        model = RandomForestRegressor(**(model_params if model_params else {}))
    elif model_type == 'LinearRegression':
        model = LinearRegression(**(model_params if model_params else {}))
    elif model_type == 'HistGradientBoosting':
        model = HistGradientBoostingRegressor(**(model_params if model_params else {}))
    else:
        raise ValueError("Unsupported model type. Choose 'RandomForest', 'LinearRegression', or 'HistGradientBoosting'.")
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Ensure the 'models' directory exists
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    model_path = f'models/{model_type.lower()}.pkl'
    joblib.dump(model, model_path)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse, model_path

def predict(df, feature_columns, model_path='models/random_forest.pkl'):
    """Make predictions using the trained model with preprocessing."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"The model file '{model_path}' does not exist. Please train the model first.")
    
    model = joblib.load(model_path)
    X, _ = preprocess_data(df, feature_columns)  # No target column needed for prediction
    
    predictions = model.predict(X)
    return predictions

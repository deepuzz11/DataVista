import pandas as pd

def clean_data(df):
    """Clean the dataset by dropping missing values and converting data types."""
    df = df.dropna()
    # Convert columns to appropriate data types if necessary
    # Example: Convert date columns to datetime
    for col in df.columns:
        if df[col].dtype == 'object' and 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def feature_engineering(df, feature_columns, new_feature_expr):
    """Perform feature engineering by creating new features based on provided expression."""
    for feature_col in feature_columns:
        if feature_col not in df.columns:
            raise ValueError(f"Required column '{feature_col}' is missing from the dataset")
    df['new_feature'] = eval(new_feature_expr)  # Note: eval is used for demo purposes; be cautious with user inputs
    return df

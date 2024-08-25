import matplotlib.pyplot as plt
import seaborn as sns

def create_scatter_plot(df, x_column, y_column):
    """Create a scatter plot for two columns."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df[x_column], df[y_column], alpha=0.7)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Scatter Plot of {y_column} vs {x_column}')
    plt.grid(True)
    return plt

def create_line_chart(df, x_column, y_column):
    """Create a line chart for two columns."""
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_column], df[y_column], marker='o')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Line Chart of {y_column} vs {x_column}')
    plt.grid(True)
    return plt

def create_bar_chart(df, x_column, y_column):
    """Create a bar chart for two columns."""
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Bar Chart of {y_column} vs {x_column}')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    return plt

def create_heatmap(df):
    """Create a heatmap of the correlation matrix."""
    plt.figure(figsize=(12, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    return plt

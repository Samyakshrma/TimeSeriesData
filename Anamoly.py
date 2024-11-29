# Mount Google Drive to access the file
from google.colab import drive

drive.mount('/content/drive')

# Now load your dataset from the specified path in Google Drive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Increase the chunksize for better handling of large datasets
plt.rcParams['agg.path.chunksize'] = 10000  # Adjust as needed

# Path to the dataset (in your case, the file is located in Google Drive)
file_path = '/content/drive/MyDrive/Time_Series_Data/synthetic_time_series.csv'  # Adjust the name if needed

# Load the dataset from the CSV file
df = pd.read_csv(file_path)

# Convert the timestamp column to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Optionally downsample the data (for performance reasons)
df_sampled = df[::100]  # Select every 100th row for faster plotting

# Anomaly Detection with Isolation Forest
features = ['cpu_temperature', 'cpu_usage', 'cpu_load', 'memory_usage', 'battery_level', 'cpu_power']
X = df_sampled[features]
model = IsolationForest(contamination=0.2)  # Adjust contamination rate as needed
df_sampled['anomaly'] = model.fit_predict(X)

# Visualize Data
for feature in features:
    plt.figure(figsize=(10, 6))

    # Set the linewidth to a small value to make the blue lines thinner
    plt.plot(df_sampled['timestamp'], df_sampled[feature], label=feature, color='blue', linewidth=0.5)

    anomalies = df_sampled[df_sampled['anomaly'] == -1]

    # Adjust the size of the red dots (anomalies) here with the 's' parameter
    plt.scatter(anomalies['timestamp'], anomalies[feature], color='red', label='Anomaly', zorder=5,
                s=10)  # smaller size

    plt.title(f'{feature} Over Time with Anomalies')
    plt.xlabel('Timestamp')
    plt.ylabel(feature)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

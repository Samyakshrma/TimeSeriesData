import wmi
import psutil
import pandas as pd
import datetime
import time
import random
import numpy as np
import os

# Settings
duration_minutes = 120  # Duration in minutes
sampling_rate_hz = 10  # Samples per second
num_samples = duration_minutes * 60 * sampling_rate_hz  # Total number of samples
output_file = "synthetic_hardware_data.csv"

# Initialize WMI client
w = wmi.WMI(namespace="root\\OpenHardwareMonitor")

# Initialize lists to store data
timestamps = []
cpu_temperatures = []
cpu_usages = []
cpu_loads = []
memory_usages = []
battery_levels = []
cpu_powers = []

# Generate Data
start_time = datetime.datetime.now()

for i in range(num_samples):
    try:
        # Get current time
        current_time = datetime.datetime.now()
        timestamps.append(current_time)

        # Generate normal data
        cpu_temp = np.random.normal(50, 5)  # Mean 50°C, SD 5°C
        cpu_usage = np.random.normal(50, 10)  # Mean 50%, SD 10%
        cpu_load = np.random.normal(1.5, 0.3)  # Mean 1.5, SD 0.3
        memory_usage = np.random.normal(50, 10)  # Mean 50%, SD 10%
        battery_level = np.random.uniform(20, 100)  # Between 20% and 100%
        cpu_power = np.random.normal(25, 5)  # Mean 25W, SD 5W

        # Randomly introduce anomalies (10% chance for each variable)
        if np.random.rand() < 0.1:
            cpu_temp = np.random.uniform(90, 105)  # High temperature
        if np.random.rand() < 0.1:
            cpu_usage = np.random.uniform(90, 100)  # High CPU usage
        if np.random.rand() < 0.1:
            memory_usage = np.random.uniform(95, 100)  # High memory usage
        if np.random.rand() < 0.1:
            battery_level = np.random.uniform(0, 10)  # Low battery level
        if np.random.rand() < 0.1:
            cpu_power = np.random.uniform(50, 100)  # High CPU power

        # Append to lists
        cpu_temperatures.append(cpu_temp)
        cpu_usages.append(cpu_usage)
        cpu_loads.append(cpu_load)
        memory_usages.append(memory_usage)
        battery_levels.append(battery_level)
        cpu_powers.append(cpu_power)

    except Exception as e:
        print(f"Error collecting data: {e}")
        cpu_temperatures.append(None)
        cpu_usages.append(None)
        cpu_loads.append(None)
        memory_usages.append(None)
        battery_levels.append(None)
        cpu_powers.append(None)

# Create a DataFrame
data = {
    'timestamp': timestamps,
    'cpu_temperature': cpu_temperatures,
    'cpu_usage': cpu_usages,
    'cpu_load': cpu_loads,
    'memory_usage': memory_usages,
    'battery_level': battery_levels,
    'cpu_power': cpu_powers
}
df = pd.DataFrame(data)

# Estimate the size of a single row (in bytes)
# Assuming 1 timestamp (24 bytes), 6 float64 values (6 * 8 bytes each)
row_size_estimate = 24 + 6 * 8  # timestamp + 6 float64 columns

# Calculate the number of rows needed to reach 1GB
target_size_min = 1 * 1024 ** 3  # 1 GB in bytes
target_size_max = 2 * 1024 ** 3  # 2 GB in bytes

# We will multiply the dataframe to reach the target size
while df.memory_usage(deep=True).sum() < target_size_max:
    df = pd.concat([df, df], ignore_index=True)

# Trim to a size between 1GB and 2GB by removing some rows if necessary
current_size = df.memory_usage(deep=True).sum()
if current_size > target_size_min:
    df = df.head(int(len(df) * (target_size_min / current_size)))

# Save to CSV file
df.to_csv(output_file, index=False)

# Output the result
print(f"Data generated and saved to {output_file} with a size of {current_size / (1024 ** 2):.2f} MB")

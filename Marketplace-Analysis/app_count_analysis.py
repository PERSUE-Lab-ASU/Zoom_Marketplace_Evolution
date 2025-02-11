import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Folder containing the JSON files
data_folder = "Data"

# List to store records of number of apps per date
apps_count_per_date = []

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        # Extract date from filename (assuming the format is zoom_marketplace_YYYY-MM-DD.json)
        date_str = filename.split('_')[-1].replace('.json', '')
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                apps_count = len(data)
                apps_count_per_date.append({"date": date_str, "count": apps_count})
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Convert the collected data to a DataFrame
df = pd.DataFrame(apps_count_per_date)

# Convert 'date' column to datetime type for easier plotting
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Sort by date
df = df.sort_values(by='date')

# Calculate trend line
x = np.arange(len(df['date']))
y = df['count'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
trend_line = slope * x + intercept

# Create the plot
plt.figure(figsize=(12, 7))

# Plot the actual data points and line
plt.plot(x, df['count'], marker='o', markersize=8, linestyle='-', label='Actual Count', color='blue')
plt.plot(x, trend_line, linestyle='--', color='red', label=f'Trend Line (R² = {r_value**2:.3f})')

# Add value labels to each point with improved positioning and formatting
for i, count in enumerate(df['count']):
    plt.annotate(f'{count}', 
                xy=(i, count),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='gray', alpha=0.7),
                fontsize=9)

# Customize the plot
plt.title("Number of Apps Available Over Time", fontsize=14, pad=20)
plt.xlabel("Date", fontsize=12)  # changed back to "Date"
plt.ylabel("Number of Apps", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Set x-ticks to show dates
plt.xticks(x, df['date'].dt.strftime('%Y-%m-%d'), rotation=45, ha='right')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Show the plot
plt.show() 
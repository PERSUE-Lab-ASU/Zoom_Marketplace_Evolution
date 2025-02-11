import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Folder containing the JSON files
data_folder = "Data"

# List to store app records with dates
apps_data = []

# List to store records of number of apps per date
apps_count_per_date = []

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        # Extract date from filename (assuming the format is zoom_marketplace_YYYY-MM-DD.json)
        date_str = filename.split('_')[-1].replace('.json', '')  # Extracting date part from filename
        try:
            # Open JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Count the number of apps in the JSON file
                apps_count = len(data)
                # Append the date and count to the list
                apps_count_per_date.append({"date": date_str, "count": apps_count})
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Convert the collected data to a DataFrame
df = pd.DataFrame(apps_count_per_date)

# Convert 'date' column to datetime type for easier plotting
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Sort by date
df = df.sort_values(by='date')

# Plotting the number of apps over time
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['count'], marker='o', linestyle='-', color='brown', label='Number of Apps')

# Add a regression line
# Convert dates to ordinal for linear regression
dates_ordinal = df['date'].map(datetime.toordinal)
# Fit a linear model to the data
slope, intercept = np.polyfit(dates_ordinal, df['count'], 1)
# Create regression line values
regression_line = slope * dates_ordinal + intercept
plt.plot(df['date'], regression_line, color='blue', linestyle='--', label='Trend Line (Regression)')

plt.title("Number of Apps Available Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Apps")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

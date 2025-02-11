import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import re

# Folder containing the JSON files
data_folder = "Data"

# Keywords to search for in app descriptions
education_keywords = ["teaching", "children", "education", "student", "classroom", "learning", "kids", "tutor", "school", "homework", "lesson"]

# Initialize lists to store data for each date
dates = []
education_apps_counts = []
total_apps_counts = []

# Compile a regex pattern to match any of the education keywords
education_pattern = re.compile(r'\b(?:' + '|'.join(education_keywords) + r')\b', re.IGNORECASE)

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        # Extract date from filename (assuming the format is zoom_marketplace_YYYY-MM-DD.json)
        date_str = filename.split('_')[-1].replace('.json', '')
        
        try:
            # Open JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Count total apps and education-related apps
                total_apps_count = len(data)
                education_apps_count = sum(
                    1 for app in data if education_pattern.search(app.get('description', '').lower())
                )
                
                # Append counts to lists
                dates.append(date_str)
                education_apps_counts.append(education_apps_count)
                total_apps_counts.append(total_apps_count)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Convert lists to DataFrame for easier plotting
df = pd.DataFrame({
    'Date': pd.to_datetime(dates),
    'Education Apps': education_apps_counts,
    'Total Apps': total_apps_counts
})

# Sort DataFrame by date
df = df.sort_values(by='Date')

# Plot stacked bar chart
plt.figure(figsize=(10, 6))
bar_width = 5  # Increase bar width to make bars thicker
plt.bar(df['Date'], df['Education Apps'], width=bar_width, label='Education Apps', color='#8B4513')
plt.bar(df['Date'], df['Total Apps'] - df['Education Apps'], width=bar_width, bottom=df['Education Apps'], label='Other Apps', color='#D2B48C')
plt.title("Number of Apps on Store by Date")
plt.xlabel("Date")
plt.ylabel("Number of Apps")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

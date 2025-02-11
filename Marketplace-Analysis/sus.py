import os
import json
from collections import defaultdict
import pandas as pd

# Folder containing the JSON files
data_folder = "Data"

# Dictionary to store descriptions and corresponding app names with links
description_to_apps_with_links = defaultdict(list)

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        date_str = filename.split('_')[-1].replace('.json', '')
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                for app in data:
                    description = app.get('description', '').strip()
                    app_name = app.get('appName', 'Unknown App')
                    app_link = app.get('link', 'No Link Available')
                    if description:
                        description_to_apps_with_links[description].append((app_name, app_link))
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Find apps with the same description but different names and collect their links
suspicious_apps_with_links = []
for description, apps in description_to_apps_with_links.items():
    unique_apps = set(apps)
    if len(unique_apps) > 1:  # Check for multiple apps with the same description
        for app_name, app_link in unique_apps:
            suspicious_apps_with_links.append({
                "Description": description,
                "App Name": app_name,
                "App Link": app_link
            })

# Convert to DataFrame
suspicious_apps_with_links_df = pd.DataFrame(suspicious_apps_with_links)

# Get the unique names of apps
unique_app_names = suspicious_apps_with_links_df['App Name'].unique()
unique_app_names.tolist()

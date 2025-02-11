import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Folder containing the JSON files
data_folder = "Data"

# Initialize counters for view, manage permissions, and user requirements for specific dates
view_permissions_2023_12_22 = Counter()
manage_permissions_2023_12_22 = Counter()
user_requirements_2023_12_22 = Counter()
view_permissions_2024_11_03 = Counter()
manage_permissions_2024_11_03 = Counter()
user_requirements_2024_11_03 = Counter()

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
                
                # Count permissions and user requirements for specific dates
                if date_str == "2023-12-22":
                    for app in data:
                        view_permissions_2023_12_22.update(app.get('viewPermissions', []))
                        manage_permissions_2023_12_22.update(app.get('managePermissions', []))
                        user_requirements_2023_12_22.update(app.get('userRequirements', []))
                elif date_str == "2024-11-03":
                    for app in data:
                        view_permissions_2024_11_03.update(app.get('viewPermissions', []))
                        manage_permissions_2024_11_03.update(app.get('managePermissions', []))
                        user_requirements_2024_11_03.update(app.get('userRequirements', []))
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Convert counters to DataFrames for plotting
view_permissions_2023_12_22_df = pd.DataFrame(view_permissions_2023_12_22.items(), columns=['Permission', 'Count'])
manage_permissions_2023_12_22_df = pd.DataFrame(manage_permissions_2023_12_22.items(), columns=['Permission', 'Count'])
user_requirements_2023_12_22_df = pd.DataFrame(user_requirements_2023_12_22.items(), columns=['Requirement', 'Count'])
view_permissions_2024_11_03_df = pd.DataFrame(view_permissions_2024_11_03.items(), columns=['Permission', 'Count'])
manage_permissions_2024_11_03_df = pd.DataFrame(manage_permissions_2024_11_03.items(), columns=['Permission', 'Count'])
user_requirements_2024_11_03_df = pd.DataFrame(user_requirements_2024_11_03.items(), columns=['Requirement', 'Count'])

# Plotting view permissions for 2023-12-22
plt.figure(figsize=(10, 6))
view_permissions_2023_12_22_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False, color='#8B4513')
plt.title("View Permissions Count for 2023-12-22")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=60, ha='right')
plt.ylim(0, max(view_permissions_2023_12_22_df['Count'].max(), 
                manage_permissions_2023_12_22_df['Count'].max(),
                user_requirements_2023_12_22_df['Count'].max(),
                view_permissions_2024_11_03_df['Count'].max(),
                manage_permissions_2024_11_03_df['Count'].max(),
                user_requirements_2024_11_03_df['Count'].max()) + 5)
plt.tight_layout()
plt.show()

# Plotting manage permissions for 2023-12-22
plt.figure(figsize=(10, 6))
manage_permissions_2023_12_22_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False, color='#A0522D')
plt.title("Manage Permissions Count for 2023-12-22")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=60, ha='right')
plt.ylim(0, max(view_permissions_2023_12_22_df['Count'].max(), 
                manage_permissions_2023_12_22_df['Count'].max(),
                user_requirements_2023_12_22_df['Count'].max(),
                view_permissions_2024_11_03_df['Count'].max(),
                manage_permissions_2024_11_03_df['Count'].max(),
                user_requirements_2024_11_03_df['Count'].max()) + 5)
plt.tight_layout()
plt.show()

# Plotting user requirements for 2023-12-22
plt.figure(figsize=(10, 6))
user_requirements_2023_12_22_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Requirement', y='Count', legend=False, color='#D2691E')
plt.title("User Requirements Count for 2023-12-22")
plt.xlabel("Requirement")
plt.ylabel("Count")
plt.xticks(rotation=60, ha='right')
plt.ylim(0, max(view_permissions_2023_12_22_df['Count'].max(), 
                manage_permissions_2023_12_22_df['Count'].max(),
                user_requirements_2023_12_22_df['Count'].max(),
                view_permissions_2024_11_03_df['Count'].max(),
                manage_permissions_2024_11_03_df['Count'].max(),
                user_requirements_2024_11_03_df['Count'].max()) + 5)
plt.tight_layout()
plt.show()

# Plotting view permissions for 2024-11-03
plt.figure(figsize=(10, 6))
view_permissions_2024_11_03_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False, color='#8B4513')
plt.title("View Permissions Count for 2024-11-03")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=60, ha='right')
plt.ylim(0, max(view_permissions_2023_12_22_df['Count'].max(), 
                manage_permissions_2023_12_22_df['Count'].max(),
                user_requirements_2023_12_22_df['Count'].max(),
                view_permissions_2024_11_03_df['Count'].max(),
                manage_permissions_2024_11_03_df['Count'].max(),
                user_requirements_2024_11_03_df['Count'].max()) + 5)
plt.tight_layout()
plt.show()

# Plotting manage permissions for 2024-11-03
plt.figure(figsize=(10, 6))
manage_permissions_2024_11_03_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False, color='#A0522D')
plt.title("Manage Permissions Count for 2024-11-03")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=60, ha='right')
plt.ylim(0, max(view_permissions_2023_12_22_df['Count'].max(), 
                manage_permissions_2023_12_22_df['Count'].max(),
                user_requirements_2023_12_22_df['Count'].max(),
                view_permissions_2024_11_03_df['Count'].max(),
                manage_permissions_2024_11_03_df['Count'].max(),
                user_requirements_2024_11_03_df['Count'].max()) + 5)
plt.tight_layout()
plt.show()

# Plotting user requirements for 2024-11-03
plt.figure(figsize=(10, 6))
user_requirements_2024_11_03_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Requirement', y='Count', legend=False, color='#D2691E')
plt.title("User Requirements Count for 2024-11-03")
plt.xlabel("Requirement")
plt.ylabel("Count")
plt.xticks(rotation=60, ha='right')
plt.ylim(0, max(view_permissions_2023_12_22_df['Count'].max(), 
                manage_permissions_2023_12_22_df['Count'].max(),
                user_requirements_2023_12_22_df['Count'].max(),
                view_permissions_2024_11_03_df['Count'].max(),
                manage_permissions_2024_11_03_df['Count'].max(),
                user_requirements_2024_11_03_df['Count'].max()) + 5)
plt.tight_layout()
plt.show()
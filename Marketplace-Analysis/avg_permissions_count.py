import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import re

# Folder containing the JSON files
data_folder = "Data"

# Initialize lists to store data for each date
dates = []
total_apps_counts = []
view_permissions_counts = []
manage_permissions_counts = []
permissions_per_app_2023_12_22 = []
permissions_per_app_2024_11_03 = []

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
                
                # Count total apps and permissions
                total_apps_count = len(data)
                view_permissions_count = sum(
                    len(app.get('viewPermissions', [])) for app in data
                )
                manage_permissions_count = sum(
                    len(app.get('managePermissions', [])) for app in data
                )
                
                # Track number of permissions per app
                for app in data:
                    total_permissions = len(app.get('viewPermissions', [])) + len(app.get('managePermissions', []))
                    if date_str == "2023-12-22":
                        permissions_per_app_2023_12_22.append(total_permissions)
                    elif date_str == "2024-11-03":
                        permissions_per_app_2024_11_03.append(total_permissions)
                
                # Append counts to lists
                dates.append(date_str)
                total_apps_counts.append(total_apps_count)
                view_permissions_counts.append(view_permissions_count)
                manage_permissions_counts.append(manage_permissions_count)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Convert lists to DataFrame for easier plotting
df = pd.DataFrame({
    'Date': pd.to_datetime(dates),
    'Total Apps': total_apps_counts,
    'View Permissions': view_permissions_counts,
    'Manage Permissions': manage_permissions_counts
})

# Sort DataFrame by date
df = df.sort_values(by='Date')

# Plot line chart for total number of apps over time
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Total Apps'], marker='o', linestyle='-', color='#1f77b4')
plt.title("Total Number of Apps Over Time")
plt.xlabel("Date")
plt.ylabel("Total Number of Apps")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot line charts for view and manage permissions over time
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['View Permissions'], marker='o', linestyle='-', color='#ff7f0e', label='View Permissions')
plt.plot(df['Date'], df['Manage Permissions'], marker='o', linestyle='-', color='#2ca02c', label='Manage Permissions')
plt.title("Number of View and Manage Permissions Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Permissions")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot line chart showing average number of permissions per app over time
df['Average View Permissions per App'] = df['View Permissions'] / df['Total Apps']
df['Average Manage Permissions per App'] = df['Manage Permissions'] / df['Total Apps']

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Average View Permissions per App'], marker='o', linestyle='-', color='#ff7f0e', label='Average View Permissions per App')
plt.plot(df['Date'], df['Average Manage Permissions per App'], marker='o', linestyle='-', color='#2ca02c', label='Average Manage Permissions per App')
plt.title("Average Number of Permissions per App Over Time")
plt.xlabel("Date")
plt.ylabel("Average Number of Permissions per App")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot histogram of view and manage permissions
plt.figure(figsize=(10, 6))
plt.hist(df['View Permissions'], bins=10, alpha=0.5, label='View Permissions', color='#ff7f0e')
plt.hist(df['Manage Permissions'], bins=10, alpha=0.5, label='Manage Permissions', color='#2ca02c')
plt.title("Distribution of View and Manage Permissions")
plt.xlabel("Number of Permissions")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()

# Determine common x-axis range for both dates
max_permissions = max(max(permissions_per_app_2023_12_22, default=0), max(permissions_per_app_2024_11_03, default=0))
x_ticks = range(0, max_permissions + 1)

# Plot a bar chart for 2023-12-22 where the x-axis is the number of permissions an app asks for and the y-axis is the number of apps asking for that many permissions
plt.figure(figsize=(10, 6))
permissions_count_series_2023_12_22 = pd.Series(permissions_per_app_2023_12_22).value_counts().reindex(x_ticks, fill_value=0)
plt.bar(permissions_count_series_2023_12_22.index, permissions_count_series_2023_12_22.values, color='#8B4513')
plt.title("Number of Apps by Number of Permissions Requested (2023-12-22)")
plt.xlabel("Number of Permissions")
plt.ylabel("Number of Apps")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot a bar chart for 2024-11-03 where the x-axis is the number of permissions an app asks for and the y-axis is the number of apps asking for that many permissions
plt.figure(figsize=(10, 6))
permissions_count_series_2024_11_03 = pd.Series(permissions_per_app_2024_11_03).value_counts().reindex(x_ticks, fill_value=0)
plt.bar(permissions_count_series_2024_11_03.index, permissions_count_series_2024_11_03.values, color='#8B4513')
plt.title("Number of Apps by Number of Permissions Requested (2024-11-03)")
plt.xlabel("Number of Permissions")
plt.ylabel("Number of Apps")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

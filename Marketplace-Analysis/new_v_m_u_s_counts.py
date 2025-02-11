import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Folder containing the JSON files
data_folder = "Data"

# Initialize counters for only 2024-12-15
view_permissions_by_category_2024_12_15 = {}
manage_permissions_2024_12_15 = Counter()
user_requirements_2024_12_15 = Counter()
scopes_2024_12_15 = Counter()

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        date_str = filename.split('_')[-1].replace('.json', '')
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Only process 2024-12-15 data
                if date_str == "2024-12-15":
                    for app in data:
                        categories = app.get('categories', ['Uncategorized'])  # Get array of categories
                        permissions = app.get('viewPermissions', [])
                        
                        # Initialize category in the dictionary if it doesn't exist
                        for permission in permissions:
                            if permission not in view_permissions_by_category_2024_12_15:
                                view_permissions_by_category_2024_12_15[permission] = Counter()
                            # Update count for each category
                            for category in categories:
                                view_permissions_by_category_2024_12_15[permission][category] += 1
                            
                        manage_permissions_2024_12_15.update(app.get('managePermissions', []))
                        user_requirements_2024_12_15.update(app.get('userRequirements', []))
                        scopes_2024_12_15.update(app.get('scopes', []))
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Reset and recalculate view permissions
view_permissions_2024_12_15 = Counter()

# Directly count from the raw data
with open('Data/zoom_marketplace_2024-12-15.json', 'r') as file:
    data = json.load(file)
    for app in data:
        view_permissions_2024_12_15.update(app.get('viewPermissions', []))

# Convert to DataFrame
view_permissions_df = pd.DataFrame(view_permissions_2024_12_15.items(), columns=['Permission', 'Count'])

# Plotting view permissions
plt.figure(figsize=(20, 6))
ax = view_permissions_df.sort_values(by='Count', ascending=False).plot(
    kind='barh',
    x='Permission',
    y='Count',
    legend=False,
    color='#3B0D0D'
)
plt.margins(x=0.1)
plt.title("View Permissions Count for 2024-12-15")
plt.ylabel("Permission")
plt.xlabel("Count")
for i, v in enumerate(view_permissions_df.sort_values(by='Count', ascending=False)['Count']):
    ax.text(v, i, f' {v}', va='center')
plt.tight_layout()
plt.show()

# Optional: Print the raw counts to verify
print("\nView Permissions Counts:")
for permission, count in view_permissions_2024_12_15.most_common():
    print(f"{permission}: {count}")

# Convert counters to DataFrames for plotting
manage_permissions_df = pd.DataFrame(manage_permissions_2024_12_15.items(), columns=['Permission', 'Count'])
user_requirements_df = pd.DataFrame(user_requirements_2024_12_15.items(), columns=['Requirement', 'Count'])
scopes_df = pd.DataFrame(scopes_2024_12_15.items(), columns=['Scope', 'Count'])

# Calculate max value for consistent y-axis
max_count = max(
    view_permissions_df['Count'].max() if not view_permissions_df.empty else 0,
    manage_permissions_df['Count'].max() if not manage_permissions_df.empty else 0,
    user_requirements_df['Count'].max() if not user_requirements_df.empty else 0
) + 5

# Plotting manage permissions
plt.figure(figsize=(20, 6))
ax = manage_permissions_df.sort_values(by='Count', ascending=True).plot(
    kind='barh',
    x='Permission',
    y='Count',
    legend=False,
    color='#2B0000'
)
plt.margins(x=0.1)
plt.title("Manage Permissions Count for 2024-12-15")
plt.ylabel("Permission")
plt.xlabel("Count")
for i, v in enumerate(manage_permissions_df.sort_values(by='Count', ascending=True)['Count']):
    ax.text(v, i, f' {v}', va='center')
plt.tight_layout()
plt.show()

# Plotting user requirements
plt.figure(figsize=(20, 6))
ax = user_requirements_df.sort_values(by='Count', ascending=True).plot(
    kind='barh',
    x='Requirement',
    y='Count',
    legend=False,
    color='#4A0404'
)
plt.margins(x=0.1)
plt.title("User Requirements Count for 2024-12-15")
plt.ylabel("Requirement")
plt.xlabel("Count")
for i, v in enumerate(user_requirements_df.sort_values(by='Count', ascending=True)['Count']):
    ax.text(v, i, f' {v}', va='center')
plt.tight_layout()
plt.show()

# Plotting scopes
plt.figure(figsize=(20, 6))
ax = scopes_df.sort_values(by='Count', ascending=True).plot(
    kind='barh',
    x='Scope',
    y='Count',
    legend=False,
    color='#1A0033'
)
plt.margins(x=0.1)
plt.title("Scopes Count for 2024-12-15")
plt.ylabel("Scope")
plt.xlabel("Count")
for i, v in enumerate(scopes_df.sort_values(by='Count', ascending=True)['Count']):
    ax.text(v, i, f' {v}', va='center')
plt.tight_layout()
plt.show()

# After the other plots, add the stacked bar chart for view permissions by category
# Convert the nested dictionary to a DataFrame
categories = set()
for permission_data in view_permissions_by_category_2024_12_15.values():
    categories.update(permission_data.keys())

data = []
for permission, category_counts in view_permissions_by_category_2024_12_15.items():
    row = {'Permission': permission}
    row.update({cat: category_counts.get(cat, 0) for cat in categories})
    data.append(row)

view_permissions_category_df = pd.DataFrame(data)
view_permissions_category_df.set_index('Permission', inplace=True)

# Create stacked horizontal bar chart
plt.figure(figsize=(20, 12))  # Increased height to accommodate more space for legend
ax = view_permissions_category_df.sort_index().plot(
    kind='barh',
    stacked=True,
    legend=True,
    colormap='Reds'  # Using a red colormap to stay consistent with the theme
)

plt.title("View Permissions Count by Category for 2024-12-15")
plt.xlabel("Count")
plt.ylabel("Permission")
plt.margins(x=0.1)

# Add value labels on the bars
for c in ax.containers:
    # Add labels
    ax.bar_label(c, label_type='center')

# Move legend outside of plot and adjust to show all categories
plt.legend(title="Categories", 
          bbox_to_anchor=(1.05, 1),  # Position legend to the right of the plot
          loc='upper left',
          borderaxespad=0,
          ncol=1)  # Display in one column for better readability

# Adjust layout to prevent legend cutoff
plt.tight_layout()
plt.subplots_adjust(right=0.85)  # Make room for the legend
plt.show()
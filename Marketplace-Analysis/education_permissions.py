import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Folder containing the JSON files
data_folder = "Data"

# Initialize counters for only 2024-05-12
view_permissions_by_category_2024_05_12 = {}
manage_permissions_2024_05_12 = Counter()
user_requirements_2024_05_12 = Counter()
scopes_2024_05_12 = Counter()

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        date_str = filename.split('_')[-1].replace('.json', '')
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                # Only process 2024-05-12 data
                if date_str == "2024-05-12":
                    for app in data:
                        categories = app.get('categories', ['Uncategorized'])  # Get array of categories
                        permissions = app.get('viewPermissions', [])
                        
                        # Initialize category in the dictionary if it doesn't exist
                        for permission in permissions:
                            if permission not in view_permissions_by_category_2024_05_12:
                                view_permissions_by_category_2024_05_12[permission] = Counter()
                            # Update count for each category
                            for category in categories:
                                view_permissions_by_category_2024_05_12[permission][category] += 1
                            
                        manage_permissions_2024_05_12.update(app.get('managePermissions', []))
                        user_requirements_2024_05_12.update(app.get('userRequirements', []))
                        scopes_2024_05_12.update(app.get('scopes', []))
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Convert the nested dictionary to a DataFrame
# Get all categories and ensure Education is included
categories = set()
for permission_data in view_permissions_by_category_2024_05_12.values():
    categories.update(permission_data.keys())
categories = sorted(list(categories))

# Create DataFrame with all categories
data = []
for permission, category_counts in view_permissions_by_category_2024_05_12.items():
    row = {'Permission': permission}
    row.update({cat: category_counts.get(cat, 0) for cat in categories})
    data.append(row)

view_permissions_category_df = pd.DataFrame(data)
view_permissions_category_df.set_index('Permission', inplace=True)

# Create stacked horizontal bar chart
plt.figure(figsize=(20, 12))

# Create color map: Education in light brown, others in gray
colors = ['#D2B48C' if cat == 'Education' else '#D3D3D3' for cat in categories]

ax = view_permissions_category_df.sort_index().plot(
    kind='barh',
    stacked=True,
    legend=True,
    color=colors
)

plt.title("View Permissions Count by Category (Education Highlighted) for 2024-05-12")
plt.xlabel("Count")
plt.ylabel("Permission")
plt.margins(x=0.1)

# Add value labels only for Education category
for i, container in enumerate(ax.containers):
    if categories[i] == 'Education':
        ax.bar_label(container, label_type='center')
    else:
        ax.bar_label(container, label_type='center', labels=[''] * len(container))

plt.legend(title="Categories", 
          bbox_to_anchor=(1.05, 1),
          loc='upper left',
          borderaxespad=0)

plt.tight_layout()
plt.subplots_adjust(right=0.85)
plt.show()

# Print the Education category data
print("\nEducation Category Permissions and Counts:")
for permission in view_permissions_category_df.index:
    if 'Education' in view_permissions_category_df.columns:
        count = int(view_permissions_category_df.loc[permission, 'Education'])
        if count > 0:
            print(f"{permission}: {count}") 
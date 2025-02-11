import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# Folder containing the JSON files
data_folder = "Data"

# Initialize dictionaries to store permission data by category
view_permissions_by_category = defaultdict(lambda: defaultdict(int))
manage_permissions_by_category = defaultdict(lambda: defaultdict(int))

# Process the data
print(f"Looking in folder: {data_folder}")  # Debug print
print(f"Files in folder: {os.listdir(data_folder)}")  # Debug print

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    print(f"Checking file: {filename}")  # Debug print
    if filename == "zoom_marketplace_2024-12-15.json":  # Match exact filename
        print(f"Processing file: {filename}")  # Debug print
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(f"Number of apps found: {len(data)}")  # Debug print

            for app in data:
                categories = app.get('categories', ['Uncategorized'])
                view_permissions = app.get('viewPermissions', [])
                manage_permissions = app.get('managePermissions', [])
                
                print(f"App: {app.get('name', 'Unknown')}")  # Debug print
                print(f"Categories: {categories}")  # Debug print
                print(f"View Permissions: {view_permissions}")  # Debug print
                print(f"Manage Permissions: {manage_permissions}")  # Debug print

                # Count each permission for each category
                for category in categories:
                    for permission in view_permissions:
                        view_permissions_by_category[permission][category] += 1
                    for permission in manage_permissions:
                        manage_permissions_by_category[permission][category] += 1

print("\nView Permissions Data:")  # Debug print
print(dict(view_permissions_by_category))  # Debug print
print("\nManage Permissions Data:")  # Debug print
print(dict(manage_permissions_by_category))  # Debug print

# Function to create subplot for a permission
def plot_permission_subplot(ax, permission, category_counts, permission_type):
    # Convert the category counts to a DataFrame and sort
    df = pd.DataFrame.from_dict(category_counts, orient='index', columns=['Count'])
    df = df.sort_values('Count', ascending=True)
    
    # Create horizontal bar chart
    df.plot(kind='barh', legend=False, color='#8B4513', ax=ax)
    
    ax.set_title(f"{permission}")
    ax.set_xlabel("Number of Apps")
    ax.set_ylabel("Category")
    
    # Add value labels on the bars
    for i, v in enumerate(df['Count']):
        if v > 0:  # Only show non-zero values
            ax.text(v, i, f' {int(v)}', va='center')

def create_permission_subplots(permissions_dict, permission_type):
    # Filter out permissions with no data
    active_permissions = {
        perm: counts for perm, counts in permissions_dict.items() 
        if any(count > 0 for count in counts.values())
    }

    if active_permissions:
        num_permissions = len(active_permissions)
        # Calculate number of rows and columns for subplots
        num_cols = min(2, num_permissions)  # Maximum 2 columns
        num_rows = (num_permissions + num_cols - 1) // num_cols
        
        # Create figure with subplots
        fig, axes = plt.subplots(num_rows, num_cols, 
                                figsize=(15, 5 * num_rows),
                                squeeze=False)
        fig.suptitle(f"{permission_type} Permissions by Category", fontsize=16, y=1.02)
        
        # Plot each permission in its subplot
        for idx, (permission, category_counts) in enumerate(active_permissions.items()):
            row = idx // num_cols
            col = idx % num_cols
            plot_permission_subplot(axes[row, col], permission, category_counts, permission_type)
        
        # Remove empty subplots if any
        for idx in range(len(active_permissions), num_rows * num_cols):
            row = idx // num_cols
            col = idx % num_cols
            fig.delaxes(axes[row, col])
        
        plt.tight_layout()
        plt.show()

# Create subplot figures for both permission types
print("\nGenerating View Permission Charts...")
create_permission_subplots(view_permissions_by_category, "View")

print("\nGenerating Manage Permission Charts...")
create_permission_subplots(manage_permissions_by_category, "Manage")
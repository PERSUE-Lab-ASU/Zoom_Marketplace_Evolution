import os
import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Folder containing the JSON files
data_folder = "Data"

# Initialize counters for scopes for specific dates
scopes_2024_06_09 = Counter()
scopes_2023_12_22 = Counter()

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        # Extract date from filename (assuming the format is zoom_marketplace_YYYY-MM-DD.json)
        date_str = filename.split('_')[-1].replace('.json', '')
        if date_str in ["2024-06-09", "2023-12-22"]:
            try:
                # Open JSON file
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    # Count scopes for specific dates
                    if date_str == "2024-06-09":
                        for app in data:
                            scopes_2024_06_09.update(app.get('scopes', []))
                    elif date_str == "2023-12-22":
                        for app in data:
                            scopes_2023_12_22.update(app.get('scopes', []))
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Convert counters to lists for plotting
scopes_2024_06_09_items = scopes_2024_06_09.items()
scopes_2023_12_22_items = scopes_2023_12_22.items()

# Plotting scopes for 2024-06-09
plt.figure(figsize=(10, 6))
scopes_2024_06_09_df = pd.DataFrame(scopes_2024_06_09_items, columns=['Scope', 'Count'])
scopes_2024_06_09_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Scope', y='Count', color='#8B4513', legend=False)
plt.title("Scopes Count for 2024-06-09")
plt.xlabel("Scope")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Plotting scopes for 2023-12-22
plt.figure(figsize=(10, 6))
scopes_2023_12_22_df = pd.DataFrame(scopes_2023_12_22_items, columns=['Scope', 'Count'])
scopes_2023_12_22_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Scope', y='Count', color='#8B4513', legend=False)
plt.title("Scopes Count for 2023-12-22")
plt.xlabel("Scope")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
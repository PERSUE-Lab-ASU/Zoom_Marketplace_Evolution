import os
import json
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Folder containing the JSON files
data_folder = "Data"

# Dictionary to store descriptions and corresponding app names
description_to_apps = defaultdict(list)
# Counter to store the number of apps with the same description over time
same_description_counter = Counter()

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
                
                # Store app names by their descriptions
                for app in data:
                    description = app.get('description', '').strip()
                    app_name = app.get('appName', 'Unknown App')
                    if description:
                        description_to_apps[description].append(app_name)
                
                # Count apps with the same description but different names for the given date
                same_description_count = sum(1 for desc, names in description_to_apps.items() if len(set(names)) > 1)
                same_description_counter[date_str] = same_description_count
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Find apps with the same description but different names
apps_with_same_description = {
    desc: names for desc, names in description_to_apps.items()
    if len(set(names)) > 1
}

# Create a visual representation using NetworkX
G = nx.Graph()

# Add nodes and edges for apps with the same description
for description, app_names in apps_with_same_description.items():
    unique_app_names = set(app_names)
    for app_name in unique_app_names:
        G.add_node(app_name, label=app_name)
    for i, app_name_1 in enumerate(unique_app_names):
        for app_name_2 in list(unique_app_names)[i + 1:]:
            G.add_edge(app_name_1, app_name_2, description=description[:100] + "...")

# Draw the graph with enhanced visualization
plt.figure(figsize=(15, 10))
pos = nx.spring_layout(G, seed=42, k=0.3)  # Adjust k for better spacing

# Draw nodes and edges with improved aesthetics
nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='#A0522D', width=1.5)
nx.draw_networkx_nodes(G, pos, node_color='#FF6347', node_size=4000, alpha=0.8)
nx.draw_networkx_labels(G, pos, font_size=12, font_color='white', font_weight='bold')

# Adding edge labels (optional)
edge_labels = {(u, v): d['description'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='#6B4226', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3'))

plt.title("Apps with the Same Description but Different Names", fontsize=16)
plt.tight_layout()
plt.show()

# Create a line graph showing the number of apps with the same description but different names over time
if same_description_counter:
    df = pd.DataFrame(list(same_description_counter.items()), columns=['Date', 'Count'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Count'], marker='o', linestyle='-', color='#8B4513')
    plt.title("Number of Apps with the Same Description but Different Names Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Apps")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
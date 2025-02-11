import os
import json
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import numpy as np

# Folder containing the JSON files
data_folder = "Data"

# Initialize counter for number of categories per app for 2024-05-12
category_counts_2024_05_12 = Counter()

# Count how many categories each app has for 2024-05-12
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        date_str = filename.split('_')[-1].replace('.json', '')
        if date_str == "2024-12-15":
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                for app in data:
                    num_categories = len(app.get('categories', []))
                    category_counts_2024_05_12[num_categories] += 1

# Create a bar chart for the distribution of number of categories per app
plt.figure(figsize=(12, 6))

# Convert counter to DataFrame
df_05_12 = pd.DataFrame.from_dict(category_counts_2024_05_12, orient='index', columns=['2024-12-15'])

# Plot bar chart
bars = df_05_12.plot(kind='bar', width=0.8)
plt.title('Distribution of Number of Categories per App for 2024-12-15')
plt.xlabel('Number of Categories')
plt.ylabel('Number of Apps')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Add numbers on top of the bars
for bar in bars.patches:
    bars.annotate(f'{int(bar.get_height())}', 
                  (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                  ha='center', va='bottom')

plt.show()

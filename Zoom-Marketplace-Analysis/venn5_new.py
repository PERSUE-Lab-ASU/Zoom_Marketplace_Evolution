import json
from pyvenn import venn
from pyvenn.venn import venn5
import matplotlib.pyplot as plt

# Load JSON data from file
file_path = "Data/zoom_marketplace_2024-05-12.json"
with open(file_path, 'r') as file:
    apps_data = json.load(file)

# Define the categories for the Venn diagram
categories = ["Productivity", "Scheduling", "Learning & Development", "Education", "CRM"]

# Map categories to apps
sets = {category: set() for category in categories}
for app in apps_data:
    for category in categories:
        if category in app.get("categories", []):
            sets[category].add(app["appName"])

# Generate Venn diagram labels
labels = venn.get_labels([sets[category] for category in categories], fill=["number", "logic"])

# Remove binary labels and keep only numbers
filtered_labels = {k: v.split(":")[-1].strip() for k, v in labels.items() if v != "0"}

# Create the Venn diagram
fig, ax = venn5(filtered_labels, names=categories)

# Adjust layout to prevent label cutoff
plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)
plt.title("5-Circle Venn Diagram: App Categories 05-12-2024")
plt.show()

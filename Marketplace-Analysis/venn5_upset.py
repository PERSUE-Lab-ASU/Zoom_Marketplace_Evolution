import os
import json
import pandas as pd
from upsetplot import UpSet
import matplotlib.pyplot as plt

# Folder containing the JSON files
data_folder = "Data"
target_date = "2024-05-12"

# Initialize sets for each category
productivity_apps = set()
scheduling_apps = set()
learning_development_apps = set()
education_apps = set()
crm_apps = set()

# Read the data and process categories
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json") and target_date in filename:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

                for app in data:
                    categories = app.get('categories', [])
                    app_name = app.get('appName', 'Unknown App')

                    # Add to sets using the exact category names from JSON
                    if 'Productivity' in categories:
                        productivity_apps.add(app_name)
                    if 'Scheduling' in categories:
                        scheduling_apps.add(app_name)
                    if 'Learning & Development' in categories:
                        learning_development_apps.add(app_name)
                    if 'Education' in categories:
                        education_apps.add(app_name)
                    if 'CRM' in categories:
                        crm_apps.add(app_name)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Create a dictionary of all apps and their categories
all_apps = set().union(productivity_apps, scheduling_apps, learning_development_apps, education_apps, crm_apps)
data_dict = {
    'Productivity': [app in productivity_apps for app in all_apps],
    'Scheduling': [app in scheduling_apps for app in all_apps],
    'Learning & Development': [app in learning_development_apps for app in all_apps],
    'Education': [app in education_apps for app in all_apps],
    'CRM': [app in crm_apps for app in all_apps]
}

# Create DataFrame
df = pd.DataFrame(data_dict, index=list(all_apps))

# Generate intersection data
intersection_data = df.value_counts()

# Create the plot using UpSet
upset = UpSet(intersection_data, sort_by='cardinality', show_counts=True)

# Draw the plot
plt.figure(figsize=(12, 8))
upset.plot()
plt.suptitle(f"App Category Intersections ({target_date})", y=1.05)

# Add a title to the graph
plt.title("Intersection of App Categories 2024-05-12")
plt.subplots_adjust(left=0.1, right=0.8, top=0.85)

print(f"\nTotal apps per category:")
print(f"Productivity: {len(productivity_apps)}")
print(f"Scheduling: {len(scheduling_apps)}")
print(f"Learning & Development: {len(learning_development_apps)}")
print(f"Education: {len(education_apps)}")
print(f"CRM: {len(crm_apps)}")

# Print key overlaps
print("\nKey overlaps:")
pairs = [
    (productivity_apps, scheduling_apps, "Productivity", "Scheduling"),
    (productivity_apps, learning_development_apps, "Productivity", "Learning & Development"),
    (productivity_apps, education_apps, "Productivity", "Education"),
    (productivity_apps, crm_apps, "Productivity", "CRM"),
    (scheduling_apps, learning_development_apps, "Scheduling", "Learning & Development"),
    (scheduling_apps, education_apps, "Scheduling", "Education"),
    (scheduling_apps, crm_apps, "Scheduling", "CRM"),
    (learning_development_apps, education_apps, "Learning & Development", "Education"),
    (learning_development_apps, crm_apps, "Learning & Development", "CRM"),
    (education_apps, crm_apps, "Education", "CRM")
]

for set1, set2, name1, name2 in pairs:
    overlap = len(set1 & set2)
    if overlap > 0:
        print(f"{name1} & {name2}: {overlap}")

plt.show()

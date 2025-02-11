import json
from collections import defaultdict

# Load JSON data
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Count app names and identify duplicates
def count_app_names(data):
    name_count = defaultdict(int)
    for app in data:
        name_count[app['appName']] += 1
    return name_count

# Load data for December 15, 2024
data_dec_15_2024 = load_data('Data/zoom_marketplace_2024-12-15.json')

# Count app names
app_name_counts = count_app_names(data_dec_15_2024)

# Print all app names and highlight duplicates
print("App names in the dataset for December 15, 2024:")
for name, count in app_name_counts.items():
    if count > 1:
        print(f"{name} (Duplicate, Count: {count})")
    else:
        print(name)
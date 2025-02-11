import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

# Load JSON data for each time point
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Compute viewPermissions differences and identify deleted apps
def compute_view_permissions_differences(data1, data2):
    permission_changes = defaultdict(int)
    app_names1 = {app['appName'] for app in data1}
    app_names2 = {app['appName'] for app in data2}

    # Identify deleted apps
    deleted_apps = app_names1 - app_names2

    # Only consider apps that exist in both datasets
    common_apps = app_names1.intersection(app_names2)

    for app_name in common_apps:
        permissions1 = next((app['viewPermissions'] for app in data1 if app['appName'] == app_name), [])
        permissions2 = next((app['viewPermissions'] for app in data2 if app['appName'] == app_name), [])

        change = len(permissions2) - len(permissions1)
        permission_changes[change] += 1

    return permission_changes, deleted_apps

# Plot the permission changes
def plot_permission_changes(changes, title):
    changes = dict(sorted(changes.items()))
    bars = plt.bar(changes.keys(), changes.values(), color='#654321')  # Dark brown color
    plt.xlabel('Change in Number of View Permissions')
    plt.ylabel('Number of Apps')
    plt.title(title)

    # Add numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center')

    # Set x-axis to display whole numbers
    plt.xticks(np.arange(min(changes.keys()), max(changes.keys()) + 1, 1))

    plt.show()

# Load data for each time point
data_dec_22_2023 = load_data('Data/zoom_marketplace_2023-12-22.json')
data_may_19_2024 = load_data('Data/zoom_marketplace_2024-05-19.json')
data_dec_15_2024 = load_data('Data/zoom_marketplace_2024-12-15.json')

# Compute viewPermissions changes and identify deleted apps
changes_dec22_may19, deleted_apps_dec22_may19 = compute_view_permissions_differences(data_dec_22_2023, data_may_19_2024)
changes_may19_dec15, deleted_apps_may19_dec15 = compute_view_permissions_differences(data_may_19_2024, data_dec_15_2024)

# Plot the results
plot_permission_changes(changes_dec22_may19, 'View Permissions Changes: Dec 22, 2023 to May 19, 2024')
plot_permission_changes(changes_may19_dec15, 'View Permissions Changes: May 19, 2024 to Dec 15, 2024')

# Print deleted apps
print("Deleted apps from Dec 22, 2023 to May 19, 2024:", deleted_apps_dec22_may19)
print("Deleted apps from May 19, 2024 to Dec 15, 2024:", deleted_apps_may19_dec15)
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

# Load JSON data for each time point
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Identify newly created apps and count their managePermissions
def compute_new_apps_permissions(data1, data2):
    app_names1 = {app['appName'] for app in data1}
    app_names2 = {app['appName'] for app in data2}

    # Identify newly created apps
    new_apps = app_names2 - app_names1

    # Count managePermissions for newly created apps
    new_apps_permissions = [len(app['managePermissions']) for app in data2 if app['appName'] in new_apps]

    return new_apps_permissions

# Plot the number of permissions in newly created apps
def plot_new_apps_permissions(permissions, title):
    bins = np.arange(-0.5, max(permissions) + 1.5, 1)
    counts, _, bars = plt.hist(permissions, bins=bins, color='#654321', edgecolor='black')
    plt.xlabel('Number of Manage Permissions')
    plt.ylabel('Number of Newly Created Apps')
    plt.title(title)
    plt.xticks(np.arange(0, max(permissions) + 1, 1))

    # Add numbers on top of the bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        if height > 0:  # Only annotate bars with a positive height
            plt.text(bar.get_x() + bar.get_width() / 2, height, int(count), va='bottom', ha='center')

    # Adjust layout to prevent title from being cut off
    plt.subplots_adjust(right=0.87)

    plt.show()

# Load data for each time point
data_dec_22_2023 = load_data('Data/zoom_marketplace_2023-12-22.json')
data_may_19_2024 = load_data('Data/zoom_marketplace_2024-05-19.json')
data_dec_15_2024 = load_data('Data/zoom_marketplace_2024-12-15.json')

# Compute managePermissions for newly created apps
new_apps_permissions_dec22_may19 = compute_new_apps_permissions(data_dec_22_2023, data_may_19_2024)
new_apps_permissions_may19_dec15 = compute_new_apps_permissions(data_may_19_2024, data_dec_15_2024)

# Plot the results
plot_new_apps_permissions(new_apps_permissions_dec22_may19, 'Manage Permissions in Newly Created Apps: Dec 22, 2023 to May 19, 2024')
plot_new_apps_permissions(new_apps_permissions_may19_dec15, 'Manage Permissions in Newly Created Apps: May 19, 2024 to Dec 15, 2024')
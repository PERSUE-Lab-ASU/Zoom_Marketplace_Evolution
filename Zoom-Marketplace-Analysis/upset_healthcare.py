import json
import matplotlib.pyplot as plt
from upsetplot import from_memberships, UpSet
import pandas as pd


def load_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def filter_healthcare_apps(data):
    """Filter apps in the Healthcare category."""
    return [app for app in data if "Healthcare" in app.get('categories', [])]


def prepare_combined_permissions_upset_data(apps):
    """Prepare UpSet data for view and manage permissions in Healthcare apps."""
    combined_permissions_memberships = []

    for app in apps:
        view_permissions = [f"{perm} (V)" for perm in app.get('viewPermissions', [])]
        manage_permissions = [f"{perm} (M)" for perm in app.get('managePermissions', [])]
        combined_permissions = view_permissions + manage_permissions

        if combined_permissions:
            combined_permissions_memberships.append(combined_permissions)

    if combined_permissions_memberships:
        upset_data = from_memberships(
            combined_permissions_memberships,
            data=pd.Series(1, index=range(len(combined_permissions_memberships)))
        )
    else:
        upset_data = pd.Series(dtype=int)  # Empty series if no data

    return upset_data


# Load data
data_file_path = 'Data/zoom_marketplace_2024-12-15.json'
data = load_data(data_file_path)

# Filter apps in the Healthcare category
healthcare_apps = filter_healthcare_apps(data)

# Prepare UpSet data for combined view and manage permissions
upset_data_combined_permissions = prepare_combined_permissions_upset_data(healthcare_apps)

# Create and display the UpSet plot
if not upset_data_combined_permissions.empty:
    plt.figure(figsize=(20, 10))
    upset_plot = UpSet(upset_data_combined_permissions,
                       subset_size='count',
                       show_counts=True,
                       sort_by='cardinality',
                       min_subset_size=1)
    upset_plot.plot()
    plt.title('View and Manage Permissions for Healthcare Apps (Dec 15, 2024)')
    plt.show()
else:
    print("No data available for view or manage permissions in Healthcare apps.")

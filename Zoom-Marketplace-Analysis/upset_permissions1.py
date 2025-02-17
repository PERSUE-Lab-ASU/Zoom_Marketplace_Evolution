import json
import matplotlib.pyplot as plt
import pandas as pd
from upsetplot import from_memberships, UpSet
from collections import Counter


def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def prepare_permissions_upset_data(data1, data2):
    app_permissions1 = {app['appName']: set(app.get('viewPermissions', [])) for app in data1}
    app_permissions2 = {app['appName']: set(app.get('viewPermissions', [])) for app in data2}

    # Track different types of permission changes
    new_app_permissions = []
    modified_permissions_added = []
    modified_permissions_removed = []
    deleted_app_permissions = []

    # Counters for single permission changes
    single_permission_new = Counter()
    single_permission_added = Counter()
    single_permission_removed = Counter()

    # Find deleted apps
    for app_name, permissions1 in app_permissions1.items():
        if app_name not in app_permissions2:
            if permissions1:  # Only include if it had permissions
                deleted_app_permissions.append(list(permissions1))

    # Identify new and modified apps
    for app_name, permissions2 in app_permissions2.items():
        if app_name not in app_permissions1:
            # This is a new app
            if permissions2:  # Only include if it has permissions
                new_app_permissions.append(list(permissions2))
                if len(permissions2) == 1:
                    single_permission_new[list(permissions2)[0]] += 1
        else:
            # This is an existing app
            permissions1 = app_permissions1[app_name]
            added_permissions = permissions2 - permissions1
            removed_permissions = permissions1 - permissions2

            if added_permissions:
                modified_permissions_added.append(list(added_permissions))
                if len(added_permissions) == 1:
                    single_permission_added[list(added_permissions)[0]] += 1

            if removed_permissions:
                modified_permissions_removed.append(list(removed_permissions))
                if len(removed_permissions) == 1:
                    single_permission_removed[list(removed_permissions)[0]] += 1

    # Create UpSet data
    upset_data_new = from_memberships(new_app_permissions, data=pd.Series(1, index=range(len(new_app_permissions))))
    upset_data_modified_added = from_memberships(modified_permissions_added,
                                               data=pd.Series(1, index=range(len(modified_permissions_added))))
    upset_data_modified_removed = from_memberships(modified_permissions_removed,
                                                 data=pd.Series(1, index=range(len(modified_permissions_removed))))
    upset_data_deleted = from_memberships(deleted_app_permissions,
                                        data=pd.Series(1, index=range(len(deleted_app_permissions))))

    return (upset_data_new.sort_values(ascending=False),
            upset_data_modified_added.sort_values(ascending=False),
            upset_data_modified_removed.sort_values(ascending=False),
            upset_data_deleted.sort_values(ascending=False),
            len(new_app_permissions),
            len(modified_permissions_added),
            len(modified_permissions_removed),
            len(deleted_app_permissions),
            single_permission_new,
            single_permission_added,
            single_permission_removed)


# Load data for each time point
data_dec_22_2023 = load_data('Data/zoom_marketplace_2023-12-22.json')
data_may_12_2024 = load_data('Data/zoom_marketplace_2024-05-12.json')

# Date strings for titles
date1 = "Dec 22, 2023"
date2 = "May 12, 2024"

# Prepare data for UpSet plots
(upset_data_new, upset_data_modified_added, upset_data_modified_removed, upset_data_deleted,
 new_count, modified_added_count, modified_removed_count, deleted_count,
 single_new, single_modified_added, single_modified_removed) = prepare_permissions_upset_data(
    data_dec_22_2023, data_may_12_2024)

# Create UpSet plots
plt.figure(figsize=(20, 10))
upset_new = UpSet(upset_data_new,
                  subset_size='count',
                  show_counts=True,
                  sort_by='cardinality',
                  min_subset_size=1)
upset_new.plot()
plt.title(f'View Permission Combinations in New Apps ({date1} to {date2})\nTotal New Apps with Permissions: {new_count}')
plt.show()

plt.figure(figsize=(20, 10))
upset_modified_added = UpSet(upset_data_modified_added,
                           subset_size='count',
                           show_counts=True,
                           sort_by='cardinality',
                           min_subset_size=1)
upset_modified_added.plot()
plt.title(f'View Permission Combinations Added to Existing Apps ({date1} to {date2})\nTotal Apps: {modified_added_count}')
plt.subplots_adjust(right=0.78)
plt.show()

plt.figure(figsize=(20, 10))
upset_modified_removed = UpSet(upset_data_modified_removed,
                             subset_size='count',
                             show_counts=True,
                             sort_by='cardinality',
                             min_subset_size=1)
upset_modified_removed.plot()
plt.title(f'View Permission Combinations Removed from Existing Apps ({date1} to {date2})\nTotal Apps: {modified_removed_count}')
plt.show()

plt.figure(figsize=(20, 10))
upset_deleted = UpSet(upset_data_deleted,
                     subset_size='count',
                     show_counts=True,
                     sort_by='cardinality',
                     min_subset_size=1)
upset_deleted.plot()
plt.title(f'View Permission Combinations in Deleted Apps ({date1} to {date2})\nTotal Apps: {deleted_count}')
plt.show()

# Print summary
print(f"\nSummary of View Permission Changes ({date1} to {date2}):")
print(f"New apps with permissions: {new_count}")
print(f"Existing apps that added permissions: {modified_added_count}")
print(f"Existing apps that removed permissions: {modified_removed_count}")
print(f"Deleted apps that had permissions: {deleted_count}")
print(f"Number of different permission combinations in new apps: {len(upset_data_new)}")
print(f"Number of different permission combinations added: {len(upset_data_modified_added)}")
print(f"Number of different permission combinations removed: {len(upset_data_modified_removed)}")
print(f"Number of different permission combinations in deleted apps: {len(upset_data_deleted)}")

print("\nSingle View Permission Additions in New Apps:")
for permission, count in single_new.most_common():
    print(f"{permission}: {count} apps")

print("\nSingle View Permission Additions in Modified Apps:")
for permission, count in single_modified_added.most_common():
    print(f"{permission}: {count} apps")

print("\nSingle View Permission Removals in Modified Apps:")
for permission, count in single_modified_removed.most_common():
    print(f"{permission}: {count} apps")
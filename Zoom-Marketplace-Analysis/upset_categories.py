import json
import matplotlib.pyplot as plt
import pandas as pd
from upsetplot import from_memberships, UpSet
from collections import Counter


# Load JSON data for each time point
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Prepare data for UpSet plot and track app changes
def prepare_upset_data(data1, data2):
    app_categories1 = {app['appName']: set(app['categories']) for app in data1}
    app_categories2 = {app['appName']: set(app['categories']) for app in data2}

    # Track different types of apps
    new_app_categories = []
    modified_app_categories_added = []
    modified_app_categories_removed = []  # New list for removed categories
    deleted_app_categories = []

    # Counters for single category changes
    single_category_new = Counter()
    single_category_modified_added = Counter()
    single_category_modified_removed = Counter()  # New counter for removed categories

    # Find deleted apps
    for app_name, categories1 in app_categories1.items():
        if app_name not in app_categories2:
            deleted_app_categories.append(list(categories1))

    # Identify new and modified apps
    for app_name, categories2 in app_categories2.items():
        if app_name not in app_categories1:
            # This is a new app
            if categories2:  # Only add if it has categories
                new_app_categories.append(list(categories2))
                if len(categories2) == 1:
                    single_category_new[list(categories2)[0]] += 1
        else:
            # This is an existing app
            categories1 = app_categories1[app_name]
            added_categories = categories2 - categories1
            removed_categories = categories1 - categories2  # Track removed categories

            if added_categories:  # Categories were added
                modified_app_categories_added.append(list(added_categories))
                if len(added_categories) == 1:
                    single_category_modified_added[list(added_categories)[0]] += 1

            if removed_categories:  # Categories were removed
                modified_app_categories_removed.append(list(removed_categories))
                if len(removed_categories) == 1:
                    single_category_modified_removed[list(removed_categories)[0]] += 1

    # Create UpSet data
    upset_data_new = from_memberships(new_app_categories, data=pd.Series(1, index=range(len(new_app_categories))))
    upset_data_modified_added = from_memberships(modified_app_categories_added,
                                               data=pd.Series(1, index=range(len(modified_app_categories_added))))
    upset_data_modified_removed = from_memberships(modified_app_categories_removed,
                                                 data=pd.Series(1, index=range(len(modified_app_categories_removed))))
    upset_data_deleted = from_memberships(deleted_app_categories,
                                        data=pd.Series(1, index=range(len(deleted_app_categories))))

    return (upset_data_new.sort_values(ascending=False),
            upset_data_modified_added.sort_values(ascending=False),
            upset_data_modified_removed.sort_values(ascending=False),
            upset_data_deleted.sort_values(ascending=False),
            len(new_app_categories),
            len(modified_app_categories_added),
            len(modified_app_categories_removed),
            len(deleted_app_categories),
            single_category_new,
            single_category_modified_added,
            single_category_modified_removed)


# Load data for each time point
data_may_12_2024 = load_data('Data/zoom_marketplace_2024-05-12.json')
data_dec_15_2024 = load_data('Data/zoom_marketplace_2024-12-15.json')

# Prepare data for UpSet plots
(upset_data_new, upset_data_modified_added, upset_data_modified_removed, upset_data_deleted,
 new_count, modified_added_count, modified_removed_count, deleted_count,
 single_new, single_modified_added, single_modified_removed) = prepare_upset_data(data_may_12_2024, data_dec_15_2024)

# Create UpSet plots
plt.figure(figsize=(20, 10))
upset_new = UpSet(upset_data_new,
                  subset_size='count',
                  show_counts=True,
                  sort_by='cardinality',
                  min_subset_size=1)
upset_new.plot()
plt.title(f'Category Combinations in New Apps (Total New Apps: {new_count})')
plt.show()

plt.figure(figsize=(20, 10))
upset_modified_added = UpSet(upset_data_modified_added,
                           subset_size='count',
                           show_counts=True,
                           sort_by='cardinality',
                           min_subset_size=1)
upset_modified_added.plot()
plt.title(f'Category Combinations Added to Existing Apps (Total Modified Apps: {modified_added_count})')
plt.show()

plt.figure(figsize=(20, 10))
upset_modified_removed = UpSet(upset_data_modified_removed,
                             subset_size='count',
                             show_counts=True,
                             sort_by='cardinality',
                             min_subset_size=1)
upset_modified_removed.plot()
plt.title(f'Category Combinations Removed from Existing Apps (Total Modified Apps: {modified_removed_count})')
plt.show()

plt.figure(figsize=(20, 10))
upset_deleted = UpSet(upset_data_deleted,
                     subset_size='count',
                     show_counts=True,
                     sort_by='cardinality',
                     min_subset_size=1)
upset_deleted.plot()
plt.title(f'Category Combinations in Deleted Apps (Total Deleted Apps: {deleted_count})')
plt.show()

# Print summary
print("\nSummary of App Changes:")
print(f"New apps created: {new_count}")
print(f"Existing apps that added categories: {modified_added_count}")
print(f"Existing apps that removed categories: {modified_removed_count}")
print(f"Apps deleted: {deleted_count}")
print(f"Number of different category combinations in new apps: {len(upset_data_new)}")
print(f"Number of different category combinations in added categories: {len(upset_data_modified_added)}")
print(f"Number of different category combinations in removed categories: {len(upset_data_modified_removed)}")
print(f"Number of different category combinations in deleted apps: {len(upset_data_deleted)}")

print("\nSingle Category Additions in New Apps:")
for category, count in single_new.most_common():
    print(f"{category}: {count} apps")

print("\nSingle Category Additions in Modified Apps:")
for category, count in single_modified_added.most_common():
    print(f"{category}: {count} apps")

print("\nSingle Category Removals in Modified Apps:")
for category, count in single_modified_removed.most_common():
    print(f"{category}: {count} apps")
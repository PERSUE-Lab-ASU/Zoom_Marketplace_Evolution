import json
import matplotlib.pyplot as plt

# Load JSON data for each time point
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Count apps that added specific categories
def count_added_categories(data1, data2, categories):
    app_categories1 = {app['appName']: set(app['categories']) for app in data1}
    app_categories2 = {app['appName']: set(app['categories']) for app in data2}

    added_category_counts = {category: 0 for category in categories}

    for app_name, categories2 in app_categories2.items():
        categories1 = app_categories1.get(app_name, set())
        added_categories = categories2 - categories1

        for category in categories:
            if category in added_categories:
                added_category_counts[category] += 1

    return added_category_counts

# Plot the number of apps with added categories
def plot_added_categories(counts, title):
    categories = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    plt.bar(categories, values, color='#654321')
    plt.xlabel('Category')
    plt.ylabel('Number of Apps')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Load data for each time point
data_may_12_2024 = load_data('Data/zoom_marketplace_2024-05-12.json')
data_dec_15_2024 = load_data('Data/zoom_marketplace_2024-12-15.json')

# Define the categories of interest
categories_of_interest = ['Learning & Development', 'Education', 'Healthcare', 'Health & Wellness', 'Financial Services', 'Government']

# Count apps that added the specified categories
added_category_counts = count_added_categories(data_may_12_2024, data_dec_15_2024, categories_of_interest)

# Plot the result
plot_added_categories(added_category_counts, 'Apps Adding Specific Categories: May 12, 2024 to Dec 15, 2024')
import os
import json
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import numpy as np

# Folder containing the JSON files
data_folder = "Data"

# Initialize counters for app categories for specific dates
categories_2024_03_09 = Counter()
categories_2024_04_14 = Counter()
categories_2024_05_12 = Counter()

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        # Extract date from filename (assuming the format is zoom_marketplace_YYYY-MM-DD.json)
        date_str = filename.split('_')[-1].replace('.json', '')
        if date_str in ["2024-03-09", "2024-04-14", "2024-05-12"]:
            try:
                # Open JSON file
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    # Count categories for specific dates
                    if date_str == "2024-03-09":
                        for app in data:
                            categories = app.get('categories', [])
                            for category in categories:
                                categories_2024_03_09.update([category])
                    elif date_str == "2024-04-14":
                        for app in data:
                            categories = app.get('categories', [])
                            for category in categories:
                                categories_2024_04_14.update([category])
                    elif date_str == "2024-05-12":
                        for app in data:
                            categories = app.get('categories', [])
                            for category in categories:
                                categories_2024_05_12.update([category])
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Convert counters to lists for plotting
categories_2024_03_09_items = categories_2024_03_09.items()
categories_2024_04_14_items = categories_2024_04_14.items()
categories_2024_05_12_items = categories_2024_05_12.items()

# Plotting categories for 2024-03-09
if categories_2024_03_09_items:
    plt.figure(figsize=(10, 6))
    categories_2024_03_09_df = pd.DataFrame(categories_2024_03_09_items, columns=['Category', 'Count'])
    categories_2024_03_09_df['Count'] = pd.to_numeric(categories_2024_03_09_df['Count'], errors='coerce')
    categories_2024_03_09_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Category', y='Count', color='#8B4513', legend=False)
    plt.title("App Categories Count for 2024-03-09")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No data available for 2024-03-09")

# Plotting categories for 2024-04-14
if categories_2024_04_14_items:
    plt.figure(figsize=(10, 6))
    categories_2024_04_14_df = pd.DataFrame(categories_2024_04_14_items, columns=['Category', 'Count'])
    categories_2024_04_14_df['Count'] = pd.to_numeric(categories_2024_04_14_df['Count'], errors='coerce')
    categories_2024_04_14_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Category', y='Count', color='#8B4513', legend=False)
    plt.title("App Categories Count for 2024-04-14")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No data available for 2024-04-14")

# Plotting categories for 2024-05-12
if categories_2024_05_12_items:
    plt.figure(figsize=(10, 6))
    categories_2024_05_12_df = pd.DataFrame(categories_2024_05_12_items, columns=['Category', 'Count'])
    categories_2024_05_12_df['Count'] = pd.to_numeric(categories_2024_05_12_df['Count'], errors='coerce')
    categories_2024_05_12_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Category', y='Count', color='#8B4513', legend=False)
    plt.title("App Categories Count for 2024-05-12")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No data available for 2024-05-12")

# Prepare data for line chart
categories_df_03_09 = pd.DataFrame(categories_2024_03_09.items(), columns=['Category', 'Count_03_09'])
categories_df_04_14 = pd.DataFrame(categories_2024_04_14.items(), columns=['Category', 'Count_04_14'])
categories_df_05_12 = pd.DataFrame(categories_2024_05_12.items(), columns=['Category', 'Count_05_12'])

# Merge dataframes on Category
combined_df = pd.merge(categories_df_03_09, categories_df_04_14, on='Category', how='outer').fillna(0)
combined_df = pd.merge(combined_df, categories_df_05_12, on='Category', how='outer').fillna(0)

# Plotting line chart for each category
if not combined_df.empty:
    plt.figure(figsize=(12, 8))  # Increased figure size for better visibility
    
    # Sort categories by their maximum count to plot larger ones first
    combined_df['max_count'] = combined_df[['Count_03_09', 'Count_04_14', 'Count_05_12']].max(axis=1)
    combined_df = combined_df.sort_values('max_count', ascending=True)
    
    # Create color map for better distinction between lines
    colors = plt.cm.rainbow(np.linspace(0, 1, len(combined_df)))
    
    for (index, row), color in zip(combined_df.iterrows(), colors):
        plt.plot(['2024-03-09', '2024-04-14', '2024-05-12'], 
                [row['Count_03_09'], row['Count_04_14'], row['Count_05_12']], 
                marker='o', 
                label=row['Category'],
                linewidth=2,
                color=color)
    
    plt.title("App Categories Count Over Time", fontsize=12, pad=20)
    plt.xlabel("Date", fontsize=10)
    plt.ylabel("Count", fontsize=10)
    plt.xticks(rotation=45, ha='right')
    
    # Adjust y-axis to show more detail
    max_value = combined_df[['Count_03_09', 'Count_04_14', 'Count_05_12']].max().max()
    plt.ylim(-max_value * 0.05, max_value * 1.2)  # Add padding above and below
    
    # Improve legend readability
    plt.legend(title='Category', 
              bbox_to_anchor=(1.15, 1),
              loc='upper left',
              fontsize=8,
              title_fontsize=10)
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
else:
    print("No data available for combined dates")

# Initialize counters for apps with valid and invalid privacy policy links for each date
valid_privacy_links_2023_12_22 = 0
invalid_privacy_links_2023_12_22 = 0
valid_privacy_links_2024_11_03 = 0
invalid_privacy_links_2024_11_03 = 0

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        # Extract date from filename (assuming the format is zoom_marketplace_YYYY-MM-DD.json)
        date_str = filename.split('_')[-1].replace('.json', '')
        if date_str in ["2023-12-22", "2024-11-03"]:
            try:
                # Open JSON file
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    # Count apps with valid privacy policy links
                    for app in data:
                        privacy_link = app.get('developerPrivacyPolicy')
                        if privacy_link and privacy_link.startswith("http"):
                            if date_str == "2023-12-22":
                                valid_privacy_links_2023_12_22 += 1
                            elif date_str == "2024-11-03":
                                valid_privacy_links_2024_11_03 += 1
                        else:
                            if date_str == "2023-12-22":
                                invalid_privacy_links_2023_12_22 += 1
                            elif date_str == "2024-11-03":
                                invalid_privacy_links_2024_11_03 += 1
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Debugging print statements to verify counts
print(f"2023-12-22 - Valid Links: {valid_privacy_links_2023_12_22}, Invalid Links: {invalid_privacy_links_2023_12_22}")
print(f"2024-11-03 - Valid Links: {valid_privacy_links_2024_11_03}, Invalid Links: {invalid_privacy_links_2024_11_03}")

# Visualize the count for 2023-12-22 using a bar graph
labels = ['Valid Privacy Policy Links', 'Invalid Privacy Policy Links']
counts_2023_12_22 = [valid_privacy_links_2023_12_22, invalid_privacy_links_2023_12_22]

plt.figure(figsize=(8, 5))
plt.bar(labels, counts_2023_12_22, color=['#4CAF50', '#F44336'])
plt.title("Number of Apps with Valid and Invalid Privacy Policy Links (2023-12-22)")
plt.xlabel("Privacy Policy Link Status")
plt.ylabel("Number of Apps")
plt.tight_layout()
plt.show()

# Visualize the count for 2024-11-03 using a bar graph
counts_2024_11_03 = [valid_privacy_links_2024_11_03, invalid_privacy_links_2024_11_03]

plt.figure(figsize=(8, 5))
plt.bar(labels, counts_2024_11_03, color=['#4CAF50', '#F44336'])
plt.title("Number of Apps with Valid and Invalid Privacy Policy Links (2024-11-03)")
plt.xlabel("Privacy Policy Link Status")
plt.ylabel("Number of Apps")
plt.tight_layout()
plt.show()

# Initialize Counter for categories of apps with valid privacy policies
categories_with_privacy = Counter()
total_apps_by_category = Counter()

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json") and "2024-05-12" in filename:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                for app in data:
                    privacy_link = app.get('developerPrivacyPolicy', '')
                    categories = app.get('categories', [])
                    
                    # Update total apps counter
                    for category in categories:
                        total_apps_by_category.update([category])
                    
                    # Check if privacy policy is valid
                    if privacy_link and privacy_link.startswith(('http://', 'https://')):
                        for category in categories:
                            categories_with_privacy.update([category])
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Create visualization for categories with privacy policies
if categories_with_privacy:
    plt.figure(figsize=(12, 6))
    categories_df = pd.DataFrame(categories_with_privacy.items(), columns=['Category', 'Count'])
    categories_df = categories_df.sort_values(by='Count', ascending=True)

    # Create horizontal bar chart
    bars = plt.barh(categories_df['Category'], categories_df['Count'], color='#4CAF50')  # Changed color to green
    plt.title("Number of Apps With Valid Privacy Policies by Category (2024-05-12)")
    plt.xlabel("Number of Apps")
    plt.ylabel("Category")

    # Add value labels on the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f' {int(width)}', 
                va='center')

    plt.tight_layout()
    plt.show()

    # Print statistics
    print(f"\nTotal number of apps with valid privacy policies: {sum(categories_with_privacy.values())}")
    print("\nBreakdown by category:")
    for category, count in sorted(categories_with_privacy.items(), key=lambda x: x[1], reverse=True):
        total = total_apps_by_category[category]
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"{category}: {count} out of {total} ({percentage:.1f}%)")
else:
    print("No data found for apps with privacy policies on 2024-05-12")

# Initialize Counters for successful and failed privacy policies by category
privacy_success_by_category = Counter()
privacy_failed_by_category = Counter()

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json") and "2024-05-12" in filename:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                for app in data:
                    categories = app.get('categories', [])
                    privacy_success = app.get('privacyPolicyLoadedSuccessfully', False)
                    
                    for category in categories:
                        if privacy_success:
                            privacy_success_by_category.update([category])
                        else:
                            privacy_failed_by_category.update([category])
                            
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Create visualization
if privacy_success_by_category or privacy_failed_by_category:
    plt.figure(figsize=(12, 8))
    
    # Convert to DataFrame for easier plotting
    categories = sorted(set(list(privacy_success_by_category.keys()) + 
                          list(privacy_failed_by_category.keys())))
    
    success_data = [privacy_success_by_category[cat] for cat in categories]
    failed_data = [privacy_failed_by_category[cat] for cat in categories]
    
    # Create positions for bars
    x = np.arange(len(categories))
    width = 0.35
    
    # Create bars
    plt.bar(x - width/2, success_data, width, label='Valid Privacy Policy', color='#4CAF50')
    plt.bar(x + width/2, failed_data, width, label='Invalid Privacy Policy', color='#F44336')
    
    plt.title("Privacy Policy Status by Category (2024-05-12)")
    plt.xlabel("Category")
    plt.ylabel("Number of Apps")
    plt.xticks(x, categories, rotation=45, ha='right')
    plt.legend()
    
    # Add value labels on the bars
    for i, v in enumerate(success_data):
        plt.text(i - width/2, v, str(v), ha='center', va='bottom')
    for i, v in enumerate(failed_data):
        plt.text(i + width/2, v, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Print statistics
    print("\nBreakdown by category:")
    for category in categories:
        success = privacy_success_by_category[category]
        failed = privacy_failed_by_category[category]
        total = success + failed
        success_rate = (success / total) * 100 if total > 0 else 0
        print(f"{category}: {success} valid, {failed} invalid ({success_rate:.1f}% success rate)")
else:
    print("No privacy policy data found for 2024-05-12")

# Create visualization for total apps per category
if total_apps_by_category:
    plt.figure(figsize=(12, 6))
    
    # Convert to DataFrame and sort
    total_categories_df = pd.DataFrame(total_apps_by_category.items(), columns=['Category', 'Count'])
    total_categories_df = total_categories_df.sort_values(by='Count', ascending=True)
    
    # Create horizontal bar chart
    bars = plt.barh(total_categories_df['Category'], total_categories_df['Count'], color='#1976D2')  # Blue color
    
    plt.title("Total Number of Apps by Category (2024-05-12)")
    plt.xlabel("Number of Apps")
    plt.ylabel("Category")
    
    # Add value labels on the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f' {int(width)}', 
                va='center')
    
    plt.tight_layout()
    plt.show()
else:
    print("No category data found for 2024-05-12")

# Initialize Counter for total apps by category for 2024-12-15
total_apps_by_category_2024_12_15 = Counter()  # Added counter for new date

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json") and "2024-12-15" in filename:  # Check for the new date
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

                for app in data:
                    categories = app.get('categories', [])

                    # Update total apps counter for 2024-12-15
                    for category in categories:
                        total_apps_by_category_2024_12_15.update([category])
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Now use the updated counter for plotting
if total_apps_by_category_2024_12_15:  # Ensure this is the counter for 2024-12-15
    plt.figure(figsize=(12, 6))

    # Convert to DataFrame and sort for 2024-12-15
    total_categories_df = pd.DataFrame(total_apps_by_category_2024_12_15.items(), columns=['Category', 'Count'])
    total_categories_df = total_categories_df.sort_values(by='Count', ascending=True)

    # Create horizontal bar chart
    bars = plt.barh(total_categories_df['Category'], total_categories_df['Count'], color='#1976D2')  # Blue color

    plt.title("Total Number of Apps by Category (2024-12-15)")  # Updated title for new date
    plt.xlabel("Number of Apps")
    plt.ylabel("Category")

    # Add value labels on the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2,
                 f' {int(width)}',
                 va='center')

    plt.tight_layout()
    plt.show()
else:
    print("No category data found for 2024-12-15")  # Updated message for new date

    
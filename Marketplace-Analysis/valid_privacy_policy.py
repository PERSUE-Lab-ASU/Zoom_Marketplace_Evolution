import os
import json
import matplotlib.pyplot as plt

# Folder containing the JSON files
data_folder = "Data"

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

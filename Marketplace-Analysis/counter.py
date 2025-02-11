import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from hashlib import md5

# Folder containing the JSON files
data_folder = "Data"

# List to store records of number of apps per date
apps_count_per_date = []

# Loop through each file in the folder
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        # Extract date from filename (assuming the format is zoom_marketplace_YYYY-MM-DD.json)
        date_str = filename.split('_')[-1].replace('.json', '')  # Extracting date part from filename
        try:
            # Open JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Count the number of apps in the JSON file
                apps_count = len(data)
                # Append the date and count to the list
                apps_count_per_date.append({"date": date_str, "count": apps_count})
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Convert the collected data to a DataFrame
df = pd.DataFrame(apps_count_per_date)

# Convert 'date' column to datetime type for easier plotting
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Sort by date
df = df.sort_values(by='date')

# Plotting the number of apps over time
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['count'], marker='o', linestyle='-')
plt.title("Number of Apps Available Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Apps")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# # Group by week and count the number of apps added each week
# df['week'] = df['date'].dt.to_period('W').dt.start_time
# weekly_apps = df.groupby('week').sum()['count']

# # Plotting the number of apps per week
# plt.figure(figsize=(10, 6))
# weekly_apps.plot(kind='line', marker='o')
# plt.title("Number of Apps Added Per Week")
# plt.xlabel("Week")
# plt.ylabel("Number of Apps")
# plt.xticks(rotation=45)
# plt.grid()
# plt.tight_layout()
# plt.show()

# Initialize counters for user-related permissions (view and manage)
view_permissions_counter = Counter()
manage_permissions_counter = Counter()

# Loop through each file in the folder to count permissions
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for app in data:
                view_permissions_counter.update(app.get('viewPermissions', []))
                manage_permissions_counter.update(app.get('managePermissions', []))

# Convert to DataFrame for plotting
view_permissions_df = pd.DataFrame(view_permissions_counter.items(), columns=['Permission', 'Count'])
manage_permissions_df = pd.DataFrame(manage_permissions_counter.items(), columns=['Permission', 'Count'])

# Plotting view permissions count
plt.figure(figsize=(10, 6))
view_permissions_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False)
plt.title("Number of Times Each Type of View Permission is Asked (User-related)")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotting manage permissions count
plt.figure(figsize=(10, 6))
manage_permissions_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False)
plt.title("Number of Times Each Type of Manage Permission is Asked (User-related)")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Filter participant-related permissions
participant_view_permissions_counter = Counter()
participant_manage_permissions_counter = Counter()

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for app in data:
                view_permissions = app.get('viewPermissions', [])
                manage_permissions = app.get('managePermissions', [])
                # Only count permissions related to participants
                participant_view_permissions_counter.update([perm for perm in view_permissions if 'Participant' in perm])
                participant_manage_permissions_counter.update([perm for perm in manage_permissions if 'Participant' in perm])

# Plotting participant view permissions count
participant_view_df = pd.DataFrame(participant_view_permissions_counter.items(), columns=['Permission', 'Count'])
plt.figure(figsize=(10, 6))
participant_view_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False)
plt.title("Number of Times Each Type of View Permission is Asked (Participant-related)")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotting participant manage permissions count
participant_manage_df = pd.DataFrame(participant_manage_permissions_counter.items(), columns=['Permission', 'Count'])
plt.figure(figsize=(10, 6))
participant_manage_df.sort_values(by='Count', ascending=False).plot(kind='bar', x='Permission', y='Count', legend=False)
plt.title("Number of Times Each Type of Manage Permission is Asked (Participant-related)")
plt.xlabel("Permission")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Collect descriptions
all_descriptions = []

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for app in data:
                description = app.get('description')
                if description:
                    all_descriptions.append(description)

# Combine all descriptions
combined_text = ' '.join(all_descriptions)

# Create word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

# Plot word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of App Descriptions")
plt.show()

# Count apps with valid privacy policy links
valid_privacy_links_count = 0

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for app in data:
                privacy_link = app.get('developerPrivacyPolicy')
                if privacy_link and privacy_link.startswith("http"):
                    valid_privacy_links_count += 1

print(f"Number of Apps with Valid Privacy Policy Links: {valid_privacy_links_count}")

# Count apps aimed at education
keywords = ["teaching", "children", "education", "student", "classroom"]
education_apps_count = 0

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for app in data:
                description = app.get('description', '').lower()
                if any(keyword in description for keyword in keywords):
                    education_apps_count += 1

print(f"Number of Apps Aimed at Education (Particularly for Children): {education_apps_count}")

# Identifying suspicious apps with identical descriptions
descriptions_dict = {}

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json"):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for app in data:
                description = app.get('description')
                if description:
                    desc_hash = md5(description.encode()).hexdigest()
                    if desc_hash in descriptions_dict:
                        descriptions_dict[desc_hash].append(app['appName'])
                    else:
                        descriptions_dict[desc_hash] = [app['appName']]

# Print apps with identical descriptions
for desc_hash, app_names in descriptions_dict.items():
    if len(app_names) > 1:
        print(f"Apps with identical descriptions: {app_names}")

import os
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles

# Folder containing the JSON files
data_folder = "Category_Data"
target_date = "2024-12-15"

# Initialize sets for each category
meetings_apps = set()
education_apps = set()
learning_dev_apps = set()

# Read the data and debug print categories
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json") and target_date in filename:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                print("\nProcessing categories for each app:")
                for app in data:
                    categories = app.get('categories', [])
                    app_name = app.get('appName', 'Unknown App')
                    
                    # Debug print
                    if any(cat in ['Meetings', 'Education', 'Learning & Development'] for cat in categories):
                        print(f"App: {app_name}")
                        print(f"Categories: {categories}")
                    
                    # Add to sets
                    if 'Meetings' in categories:
                        meetings_apps.add(app_name)
                    if 'Education' in categories:
                        education_apps.add(app_name)
                    if 'Learning & Development' in categories:
                        learning_dev_apps.add(app_name)
                        
                print("\nSets after processing:")
                print(f"Meetings apps: {meetings_apps}")
                print(f"Education apps: {education_apps}")
                print(f"Learning & Development apps: {learning_dev_apps}")
                
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Calculate all possible regions of the Venn diagram
# Region (100): Only in Meetings
only_meetings = meetings_apps - (education_apps | learning_dev_apps)

# Region (010): Only in Education
only_education = education_apps - (meetings_apps | learning_dev_apps)

# Region (001): Only in Learning & Development
only_learning = learning_dev_apps - (meetings_apps | education_apps)

# Region (110): In Meetings and Education but not Learning & Development
meet_edu = (meetings_apps & education_apps) - learning_dev_apps

# Region (101): In Meetings and Learning & Development but not Education
meet_learning = (meetings_apps & learning_dev_apps) - education_apps

# Region (011): In Education and Learning & Development but not Meetings
edu_learning = (education_apps & learning_dev_apps) - meetings_apps

# Region (111): In all three
all_three = meetings_apps & education_apps & learning_dev_apps

# Print detailed statistics before creating visualization
print(f"\nDetailed Statistics for {target_date}:")
print(f"Apps only in Meetings: {len(only_meetings)}")
print(f"Apps only in Education: {len(only_education)}")
print(f"Apps only in Learning & Development: {len(only_learning)}")
print(f"Apps in Meetings and Education only: {len(meet_edu)}")
print(f"Apps in Meetings and Learning & Development only: {len(meet_learning)}")
print(f"Apps in Education and Learning & Development only: {len(edu_learning)}")
print(f"Apps in all three categories: {len(all_three)}")

# Print total apps in each category
print(f"\nTotal apps per category:")
print(f"Total in Meetings: {len(meetings_apps)}")
print(f"Total in Education: {len(education_apps)}")
print(f"Total in Learning & Development: {len(learning_dev_apps)}")

# Create the Venn diagram
plt.figure(figsize=(12, 8))
venn = venn3(subsets=(
    len(only_meetings),      # 100
    len(only_education),     # 010
    len(meet_edu),          # 110
    len(only_learning),     # 001
    len(meet_learning),     # 101
    len(edu_learning),      # 011
    len(all_three)          # 111
), set_labels=('Meetings', 'Education', 'Learning & Development'))

# Customize appearance
plt.title(f"App Category Overlaps ({target_date})")

# Add circles for better visibility
venn_circles = venn3_circles(subsets=(
    len(only_meetings),
    len(only_education),
    len(meet_edu),
    len(only_learning),
    len(meet_learning),
    len(edu_learning),
    len(all_three)
))

# Print the actual apps in each category for verification
print("\nApps in each category:")
print("\nMeetings only:")
for app in only_meetings:
    print(f"- {app}")

print("\nEducation only:")
for app in only_education:
    print(f"- {app}")

print("\nLearning & Development only:")
for app in only_learning:
    print(f"- {app}")

print("\nApps in all three categories:")
for app in all_three:
    print(f"- {app}")

plt.show()
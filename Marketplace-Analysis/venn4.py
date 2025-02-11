import os
import json
from venny4py.venny4py import *
import matplotlib.pyplot as plt

# Folder containing the JSON files
data_folder = "Data"
target_date = "2024-12-15"

# Initialize sets for each category
productivity_apps = set()
scheduling_calendar_apps = set()
team_collaborations_apps = set()

# Read the data and process categories
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    if filename.endswith(".json") and target_date in filename:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                for app in data:
                    categories = app.get('categories', [])
                    app_name = app.get('appName', 'Unknown App')
                    
                    # Add to sets using the exact category names from JSON
                    if 'productivity' in categories:
                        productivity_apps.add(app_name)
                    if 'scheduling-calendar' in categories:
                        scheduling_calendar_apps.add(app_name)
                    if 'team-collaborations' in categories:
                        team_collaborations_apps.add(app_name)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {filename}")

# Create dictionary of sets for venny4py
sets = {
    'Productivity': productivity_apps,
    'Scheduling/Calendar': scheduling_calendar_apps,
    'Team Collaborations': team_collaborations_apps
}

# Create the Venn diagram
venny4py(sets=sets)

# Print statistics
print(f"\nTotal apps per category:")
print(f"Total in Productivity: {len(productivity_apps)}")
print(f"Total in Scheduling/Calendar: {len(scheduling_calendar_apps)}")
print(f"Total in Team Collaborations: {len(team_collaborations_apps)}")

# Print the actual apps in each category
print("\nApps in each category:")
print("\nProductivity apps:")
for app in productivity_apps:
    print(f"- {app}")

print("\nScheduling/Calendar apps:")
for app in scheduling_calendar_apps:
    print(f"- {app}")

print("\nTeam Collaborations apps:")
for app in team_collaborations_apps:
    print(f"- {app}")

# Print apps in all three categories
all_three = productivity_apps & scheduling_calendar_apps & team_collaborations_apps
print(f"\nApps in all three categories ({len(all_three)}):")
for app in all_three:
    print(f"- {app}")
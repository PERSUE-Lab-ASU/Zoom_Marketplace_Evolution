import json

# Specify the path to your JSON file
file_path = 'Data/zoom_marketplace_2024-12-15.json'

# Read the JSON data from the file
try:
    with open(file_path, 'r') as file:
        apps = json.load(file)  # Load JSON data directly from the file

    # Find and print apps with zero categories
    apps_with_no_categories = [app for app in apps if not app['categories']]
    for app in apps_with_no_categories:
        print(f"App Name: {app['appName']}, App URL: {app['appUrl']}")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
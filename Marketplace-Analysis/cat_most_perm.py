import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def analyze_categories_permissions(data):
    # Create a mapping of categories to their permission counts
    category_permissions = defaultdict(list)
    
    for app in data:
        categories = app.get('categories', [])
        permissions = app.get('managePermissions', [])
        permission_count = len(permissions)
        
        # Add permission count to each category the app belongs to
        for category in categories:
            category_permissions[category].append(permission_count)
    
    # Calculate statistics for each category
    category_stats = []
    for category, perm_counts in category_permissions.items():
        category_stats.append({
            'category': category,
            'mean_permissions': sum(perm_counts) / len(perm_counts),
            'max_permissions': max(perm_counts),
            'min_permissions': min(perm_counts),
            'app_count': len(perm_counts),
            'total_permissions': sum(perm_counts)
        })
    
    return pd.DataFrame(category_stats)

# Load the most recent data
data = load_data('Data/zoom_marketplace_2024-05-12.json')

# Analyze the data
df = analyze_categories_permissions(data)
df_sorted = df.sort_values('mean_permissions', ascending=False)

# Create a bar plot
plt.figure(figsize=(15, 8))
ax = sns.barplot(data=df_sorted, x='category', y='mean_permissions', color='black')

# Add value labels on top of each bar
for i, v in enumerate(df_sorted['mean_permissions']):
    ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
plt.title('Average Number of Manage Permissions by App Category')
plt.xlabel('Category')
plt.ylabel('Average Number of Manage Permissions')
plt.tight_layout()
plt.show()

# Print detailed statistics
print("\nDetailed Category Statistics:")
print(df_sorted.to_string(index=False))

# Identify categories with highest permission requirements
print("\nTop 5 Categories by Average Manage Permissions:")
print(df_sorted.head().to_string(index=False))

# Calculate correlation between app count and permission count
correlation = df_sorted['app_count'].corr(df_sorted['mean_permissions'])
print(f"\nCorrelation between category size and average manage permissions: {correlation:.3f}")
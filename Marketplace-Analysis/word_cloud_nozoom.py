import os
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Folder containing the JSON files
data_folder = "Data"

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

# Remove words that include "zoom"
filtered_text = ' '.join([word for word in combined_text.split() if "zoom" not in word.lower()])

# Create word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)

# Plot word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of App Descriptions (Without 'zoom')")
plt.show()

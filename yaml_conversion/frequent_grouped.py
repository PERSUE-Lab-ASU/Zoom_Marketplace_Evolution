import os
import pandas as pd
from collections import defaultdict

def count_data_types_in_csv(csv_folder: str) -> pd.DataFrame:
    """
    Process all CSV files in the specified folder and count the most frequently collected data types,
    grouping by unique data types within each file.
    """
    data_type_counts = defaultdict(int)
    
    # Iterate through all CSV files in the folder
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_folder, filename)
            try:
                df = pd.read_csv(file_path)
                
                if 'data_type' in df.columns:
                    # Count unique data types in this file
                    unique_data_types = df['data_type'].drop_duplicates()
                    for data_type in unique_data_types:
                        data_type_counts[data_type] += 1
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    # Convert the counts into a DataFrame for easier viewing and sorting
    data_type_summary = pd.DataFrame(data_type_counts.items(), columns=['data_type', 'count'])
    data_type_summary = data_type_summary.sort_values(by='count', ascending=False).reset_index(drop=True)
    
    return data_type_summary

def main():
    csv_folder = 'leaf_connection'  # Update this path to your folder containing CSV files

    try:
        data_type_summary = count_data_types_in_csv(csv_folder)
        
        if not data_type_summary.empty:
            # Save the summary to a new CSV file with the new name
            data_type_summary.to_csv('data_type_frequency_summary_grouped.csv', index=False)
            print("Successfully created data type frequency summary!")
            print(f"\nMost frequent data types:")
            print(data_type_summary)
        else:
            print("No data types were found.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

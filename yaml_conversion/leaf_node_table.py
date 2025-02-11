import yaml
import pandas as pd
from collections import defaultdict
from typing import Dict, List, Any, Set, Tuple

def extract_purposes(purposes: Dict[str, List[str]]) -> str:
    """Convert purposes dictionary to a string format, keeping only the purpose categories."""
    if not purposes:
        return ""
    return ", ".join(purposes.keys())

def build_adjacency_list(links: List[Dict]) -> Dict[str, List[Tuple[str, Dict]]]:
    """
    Build an adjacency list representation of the graph with purposes.
    """
    adj_list = defaultdict(list)
    for link in links:
        source = link.get('source', '')
        target = link.get('target', '')
        purposes = link.get('purposes', {})
        if source and target:
            adj_list[source].append((target, purposes))
    return adj_list

def find_leaf_nodes(links: List[Dict]) -> Set[str]:
    """
    Identify leaf nodes (nodes that don't have any outgoing edges).
    """
    sources = set(link.get('source', '') for link in links)
    targets = set(link.get('target', '') for link in links)
    return targets - sources

def find_root_nodes(links: List[Dict]) -> Set[str]:
    """
    Identify root nodes (nodes that appear as sources but not as targets).
    """
    sources = set(link.get('source', '') for link in links)
    targets = set(link.get('target', '') for link in links)
    return sources - targets

def get_all_paths_with_purposes(adj_list: Dict[str, List[Tuple[str, Dict]]], 
                                start: str,
                                end: str,
                                path: List[str] = None,
                                purposes_accumulated: Dict[str, List[str]] = None,
                                all_paths: List[Tuple[List[str], Dict[str, List[str]]]] = None) -> List[Tuple[List[str], Dict[str, List[str]]]]:
    """
    Find all paths between start and end nodes while accumulating purposes along the way.
    """
    if path is None:
        path = []
    if purposes_accumulated is None:
        purposes_accumulated = defaultdict(list)
    if all_paths is None:
        all_paths = []
    
    path = path + [start]

    if start == end:
        all_paths.append((path, dict(purposes_accumulated)))
        return
    
    for next_node, purposes in adj_list.get(start, []):
        if next_node not in path:
            for category in purposes.keys():
                purposes_accumulated[category].extend(purposes[category])
            get_all_paths_with_purposes(adj_list, next_node, end, path, purposes_accumulated, all_paths)
    
    return all_paths

def process_yaml_to_organized_data(yaml_content: str) -> pd.DataFrame:
    """
    Convert YAML content to a DataFrame with inherited purposes from root to leaf.
    """
    try:
        data = yaml.safe_load(yaml_content)
        if not isinstance(data, dict) or 'links' not in data:
            print("Invalid YAML structure: missing 'links' key")
            return pd.DataFrame()
            
        links = data['links']
        if not isinstance(links, list):
            print("Invalid YAML structure: 'links' is not a list")
            return pd.DataFrame()
        
        adj_list = build_adjacency_list(links)
        leaf_nodes = find_leaf_nodes(links)
        root_nodes = find_root_nodes(links)

        rows = []
        for root in root_nodes:
            for leaf in leaf_nodes:
                paths_with_purposes = get_all_paths_with_purposes(adj_list, root, leaf)

                for path, inherited_purposes in paths_with_purposes:
                    rows.append({
                        'data_type': leaf,
                        'collector': root,
                        'purpose': extract_purposes(inherited_purposes)
                    })
        
        df = pd.DataFrame(rows)
        
        if not df.empty:
            df = df.sort_values(['data_type', 'collector']).reset_index(drop=True)
            df = df.drop_duplicates()
        
        return df

    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame()

def main():
    try:
        with open('Graph Original.yml', 'r') as file:
            yaml_content = file.read()
        
        df = process_yaml_to_organized_data(yaml_content)
        
        if not df.empty:
            df.to_csv('data_collection_inventory.csv', index=False)
            print("Successfully created data collection inventory!")
            print(f"\nTotal entries: {len(df)}")
            print("\nData types being collected:")
            print('\n'.join(f"- {data_type}" for data_type in sorted(df['data_type'].unique())))
        else:
            print("No data was processed.")
            
    except FileNotFoundError:
        print("Input YAML file not found!")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
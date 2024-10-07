import json
from flatten_zones import flatten_zones
from json_to_csv import json_to_csv

def from_file(file_path = 'zones_data.json'):
    result = False
    # Load JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            json_data = json.load(file)  # Parse JSON data into a Python dictionary
            print(json_data)  # Print the loaded data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Check result before passing it to json.loads
    try:
        # json_data = json.loads(result)
        # Flatten the zones data
        flattened_zones = flatten_zones(json_data)
        # Convert to CSV
        csv_file_path = 'output.csv'
        json_to_csv(flattened_zones, csv_file_path)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return result
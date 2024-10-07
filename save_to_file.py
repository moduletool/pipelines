from list_zones import list_zones

def save_to_file(headers, file_path = 'zones_data.json'):
    result = list_zones(headers)

    print(result)
    # Specify the file path

    # Write JSON data to a file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)  # indent=4 for pretty printing

    print(f"Data successfully written to {file_path}")

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
    if result is None:
        print("Result is None, unable to process JSON.")
    else:
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

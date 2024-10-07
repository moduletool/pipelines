import csv

def json_to_csv(flattened_data, csv_file_path):
    # Check if flattened_data is None
    if flattened_data is None:
        raise ValueError("No data available to convert to CSV")

    # Get the headers from the keys of the first item
    headers = flattened_data[0].keys()

    # Write to CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write the rows
        for row in flattened_data:
            writer.writerow(row)
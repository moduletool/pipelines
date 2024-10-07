
def flatten_zones(json_data):
    flattened_data = []

    for zone in json_data:
        zone_name = zone.get("zone_name")
        original_name_servers = zone.get("original_name_servers", [])

        # If original_name_servers is None, set it to an empty list
        if original_name_servers is None:
            original_name_servers = []

        # Join the original name servers into a single string
        original_name_servers_str = ", ".join(original_name_servers) if original_name_servers else "N/A"

        flattened_data.append({
            "zone_name": zone_name,
            "original_name_servers": original_name_servers_str
        })

    return flattened_data
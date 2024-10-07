from list_zones import list_zones
from get_all_zones import get_all_zones

def list_zones(headers):
    zones = get_all_zones(headers)

    output = []

    for zone in zones:
        zone_info = {
            "zone_name": zone.get("name"),
            "original_name_servers": zone.get("original_name_servers", [])
        }
        output.append(zone_info)

    # Print the output as a JSON string
    return output
    # return json.dumps(output, indent=4)



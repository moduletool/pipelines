from list_zones import list_zones
import requests

def remove_zone(domain, headers, zones):

    for zone in zones:
        if zone.get("name") == domain:
            zone_id = zone.get("id")
            url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}'

            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                print(f"Successfully removed zone for domain '{domain}'.")
                return True
            else:
                print(f"Error removing zone: {response.status_code} - {response.text}")

    return False


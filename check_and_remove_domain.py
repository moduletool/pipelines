import os
import sys
from dotenv import load_dotenv
from cloudflare import Cloudflare  # Replace this with the actual library if it's different

import requests



def get_all_zones(headers, url = 'https://api.cloudflare.com/client/v4/zones'):

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        zones = response.json()["result"]
        for zone in zones:
            print(zone["name"])  # Print each zone name
    else:
        print(f"Error fetching zones: {response.status_code} - {response.text}")


import requests


def get_zone_id(domain, headers, url = 'https://api.cloudflare.com/client/v4/zones'):

    response = requests.get(url, headers=headers)
    # return response.status_code
    if response.status_code == 200:
        zones = response.json()["result"]
        for zone in zones:
            if zone["name"] == domain:
                return zone["id"]
    else:
        print(f"Error fetching zones: {response.status_code} - {response.text}")

    return None


def remove_zone(domain, headers):
    zone_id = get_zone_id(domain, headers)

    if not zone_id:
        print(f"Zone for domain '{domain}' not found.")
        return False

    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}'

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"Successfully removed zone for domain '{domain}'.")
        return True
    else:
        print(f"Error removing zone: {response.status_code} - {response.text}")

    return False





def remove_domain_from_cloudflare(domain, cf):
    # Get all zones
    try:
        # zones = cf.zones.get()  # Fetch all available zones
        # Find the zone with the name that matches the domain
        # matching_zones = [zone for zone in zones if zone['name'] == domain]

        # if not matching_zones:
        #     print(f"Nie znaleziono strefy dla domeny: {domain}")
        #     return False

        # Assuming you're interested in the first match
        # zone_id = matching_zones[0]['id']

        # Delete the DNS zone
        # cf.zones.delete(zone_id=zone_id)
        # print(f"Pomyślnie usunięto domenę {domain} ze stref DNS Cloudflare")
        return True
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python check_and_remove_domain.py <nazwa_domeny>")
        sys.exit(1)

    domain = sys.argv[1]
    load_dotenv()
    client = Cloudflare(
        api_email=os.getenv('CLOUDFLARE_EMAIL'),
        api_key=os.getenv('CLOUDFLARE_API_KEY'),
    )
    # Example usage
    api_token = os.getenv('CLOUDFLARE_API_KEY')
    # print(api_token)
    headers = {
        'Authorization': f'Bearer {api_token}',  # Use Bearer token
        'Content-Type': 'application/json'
    }
    # print(headers)
    # result = get_all_zones(api_token)
    result = remove_zone(domain, headers)
    # result = get_zone_id(domain=domain, headers=headers)
    print(result)
    # result = remove_domain_from_cloudflare(domain, client)
    sys.exit(0 if result else 1)
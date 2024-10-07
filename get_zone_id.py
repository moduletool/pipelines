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

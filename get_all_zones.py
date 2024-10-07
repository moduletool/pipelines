import requests

def get_all_zones(headers, url = 'https://api.cloudflare.com/client/v4/zones'):

    zones = []
    page = 1
    per_page = 50  # Number of results per page

    while True:
        params = {
            'page': page,
            'per_page': per_page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            result = response.json()
            zones.extend(result["result"])  # Add the fetched zones to the list

            # Break if there are no more zones to fetch
            if len(result["result"]) < per_page:
                break

            page += 1  # Move to the next page
        else:
            print(f"Error fetching zones: {response.status_code} - {response.text}")
            break

    return zones



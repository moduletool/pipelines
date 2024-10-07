import os
import sys
from dotenv import load_dotenv
from cloudflare import Cloudflare  # Replace this with the actual library if it's different
from get_all_zones import get_all_zones
from get_zone_id import get_zone_id
from remove_zone import remove_zone



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
    # file_path='zones_data.json'
    # result = save_to_file(headers, file_path)
    # exit()
    #result = from_file(file_path)

    # print(headers)
    # result = get_all_zones(headers)


    # Specify the path to your file containing domain names
    file_path = 'domains.csv'
    # Open the file and read line by line
    with open(file_path, 'r', encoding='utf-8') as file:
        zones = get_all_zones(headers)

        for line in file:
            domain = line.strip()  # Remove any leading/trailing whitespace
            if domain:  # Ensure the line is not empty
                print(f"- {domain}")
                result = remove_zone(domain, headers, zones)
                # Here you can add your logic to process each domain


    # result = get_zone_id(domain=domain, headers=headers)

    # Convert JSON string to Python object
    # json_data = json.loads(result)



    # result = remove_domain_from_cloudflare(domain, client)
    sys.exit(0 if result else 1)
import os
import sys
from dotenv import load_dotenv
# Replace 'cloudflare' with the actual library/package name
from cloudflare import Cloudflare  # Assuming this is the correct import


def remove_domain_from_cloudflare(domain, cf):
    # Load environment variables from .env file
    try:
        # Fetch all zones and find the correct zone for the domain
        zones = cf.zones.get()  # Here we assume it fetches all zones
        # Normally, filtering might be needed according to the library's interface
        matching_zones = [zone for zone in zones if zone['name'] == domain]

        if not matching_zones:
            print(f"Nie znaleziono strefy dla domeny: {domain}")
            return False

        zone_id = matching_zones[0]['id']
        # Delete the DNS zone
        cf.zones.delete(zone_id)
        print(f"Pomyślnie usunięto domenę {domain} ze stref DNS Cloudflare")
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

    result = remove_domain_from_cloudflare(domain, client)
    sys.exit(0 if result else 1)
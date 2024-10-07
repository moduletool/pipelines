import os
import sys
from dotenv import load_dotenv
from cloudflare import Cloudflare



def remove_domain_from_cloudflare(domain, cf):
    # Wczytaj zmienne środowiskowe z pliku .env

    try:
        # Znajdź zone_id dla podanej domeny
        zones = cf.zones.get(domain)

        if len(zones) == 0:
            print(f"Nie znaleziono strefy dla domeny: {domain}")
            return False

        zone_id = zones[0]['id']

        # Usuń strefę DNS
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
    print(domain)
    load_dotenv()
    print(os.getenv('CLOUDFLARE_EMAIL'))
    client = Cloudflare(
        # This is the default and can be omitted
        api_email=os.getenv('CLOUDFLARE_EMAIL'),
        # This is the default and can be omitted
        api_key=os.getenv('CLOUDFLARE_API_KEY'),
    )    
    result = remove_domain_from_cloudflare(domain, client)
    print(str(result).lower())
    sys.exit(0 if result else 1)
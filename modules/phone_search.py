# modules/phone_search.py
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def search_phone():
    number_input = input("\nEntrez le numéro : ").strip()

    try:
        number = phonenumbers.parse(number_input)

        valid = phonenumbers.is_valid_number(number)
        possible = phonenumbers.is_possible_number(number)
        country = geocoder.description_for_number(number, "fr")
        operator = carrier.name_for_number(number, "fr")
        zones = timezone.time_zones_for_number(number)

        print(f"\n{BOLD}{CYAN}=== 📞 Infos sur le numéro ==={RESET}")

        print(f"{YELLOW}• Numéro valide :{RESET} "
              f"{GREEN if valid else RED}{valid}{RESET}")

        print(f"{YELLOW}• Numéro possible :{RESET} "
              f"{GREEN if possible else RED}{possible}{RESET}")

        print(f"{YELLOW}• Pays :{RESET} {country or 'Inconnu'}")
        print(f"{YELLOW}• Opérateur :{RESET} {operator or 'Inconnu'}")

        print(f"{YELLOW}• Fuseau(x) horaire :{RESET} "
              f"{', '.join(zones) if zones else 'Inconnu'}")

    except phonenumbers.NumberParseException as e:
        print(f"{RED}[!] Numéro invalide : {e}{RESET}")

    input("\nAppuyez sur Entrée pour revenir au menu...")
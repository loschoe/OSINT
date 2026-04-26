import os
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type, PhoneNumberType, format_number, PhoneNumberFormat

RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def get_number_type(num):
    t = number_type(num)
    types = {
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE: "Fixe",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe/Mobile",
        PhoneNumberType.TOLL_FREE: "Numéro gratuit",
        PhoneNumberType.PREMIUM_RATE: "Surtaxé",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.UNKNOWN: "Inconnu"
    }
    return types.get(t, "Inconnu")


def save_to_file(data, filename):
    os.makedirs("module/data", exist_ok=True)
    path = os.path.join("modules/data", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

    return path


def search_phone():
    number_input = input("\n📞 Entrez le numéro : ").strip()

    try:
        number_input = number_input.replace(" ", "").replace("-", "")

        if number_input.startswith("+"):
            number = phonenumbers.parse(number_input, None)
        else:
            number = phonenumbers.parse(number_input, "FR")

        valid = phonenumbers.is_valid_number(number)
        possible = phonenumbers.is_possible_number(number)

        region = phonenumbers.region_code_for_number(number)
        country = geocoder.description_for_number(number, "fr")
        operator = carrier.name_for_number(number, "fr")
        zones = timezone.time_zones_for_number(number)
        num_type = get_number_type(number)

        international = format_number(number, PhoneNumberFormat.INTERNATIONAL)
        national = format_number(number, PhoneNumberFormat.NATIONAL)
        e164 = format_number(number, PhoneNumberFormat.E164)

        # 🔥 Affichage console
        print(f"\n{BOLD}{CYAN}=== 📡 PHONE INFO ==={RESET}")
        print(f"{YELLOW}• Validité :{RESET} {valid}")
        print(f"{YELLOW}• Possible :{RESET} {possible}")
        print(f"{YELLOW}• Pays :{RESET} {country or 'Inconnu'}")
        print(f"{YELLOW}• Région :{RESET} {region or 'Inconnu'}")
        print(f"{YELLOW}• Opérateur :{RESET} {operator or 'Inconnu'}")
        print(f"{YELLOW}• Type :{RESET} {num_type}")
        print(f"{YELLOW}• Fuseaux :{RESET} {', '.join(zones) if zones else 'Inconnu'}")

        print(f"\n{BOLD}{CYAN}=== 📌 FORMATS ==={RESET}")
        print(f"{YELLOW}• International :{RESET} {international}")
        print(f"{YELLOW}• National :{RESET} {national}")
        print(f"{YELLOW}• E164 :{RESET} {e164}")

        report = f"""
PHONE OSINT REPORT
===================

Number input: {number_input}

Valid: {valid}
Possible: {possible}

Country: {country}
Region: {region}
Operator: {operator}
Type: {num_type}
Timezones: {', '.join(zones) if zones else 'Inconnu'}

Formats:
- International: {international}
- National: {national}
- E164: {e164}
"""

        filename = f"phone_{e164.replace('+','')}.txt"
        path = save_to_file(report, filename)

        print(f"\n{GREEN}[+] Rapport sauvegardé : {path}{RESET}")

    except phonenumbers.NumberParseException as e:
        print(f"{RED}[!] Numéro invalide : {e}{RESET}")
import os
import sys
from wcwidth import wcswidth

from modules.analyse_exif import extract_exif_data
from modules.remove_exif import remove_metadata
from modules.sherlock import sherlock_scan
from modules.nmap_scan import scan_ip
from modules.nmap_carto_scan import scan_network_auto
from modules.phone_search import search_phone
from modules.compagny_dork import search_company
from modules.person_dork import search_person
from tools.utils import clear_console


# ───────────────────────────────────────────────
#  Gestion clavier
# ───────────────────────────────────────────────

def get_key():
    if os.name == 'nt':
        import msvcrt
        key = msvcrt.getch()
        if key == b'\xe0':
            return msvcrt.getch().decode()
        return key.decode()

    import tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)

        if ch1 == '\n':
            return '\n'

        if ch1 == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            seq = ch1 + ch2 + ch3
            if seq == '\x1b[A': return 'H'
            if seq == '\x1b[B': return 'P'
            return seq

        return ch1

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ───────────────────────────────────────────────
#  Menu UI
# ───────────────────────────────────────────────

def menu(title, options):
    index = 0
    width = max(wcswidth(opt) for opt in options) + 4

    while True:
        clear_console()

        print("╔" + "═" * width + "╗")
        print("║" + title.center(width) + "║")
        print("╠" + "═" * width + "╣")

        for i, opt in enumerate(options):
            prefix = "👉 " if i == index else "   "
            line = prefix + opt
            padding = width - wcswidth(line)
            print(f"║{line}{' ' * padding}║")

        print("╚" + "═" * width + "╝")

        key = get_key()

        match key:
            case 'H':
                index = (index - 1) % len(options)
            case 'P':
                index = (index + 1) % len(options)
            case '\r' | '\n':
                return index


# ───────────────────────────────────────────────
#  Safe runner
# ───────────────────────────────────────────────

def safe_run(func, *args):
    try:
        return func(*args)
    except Exception as e:
        print("\n❌ Une erreur est survenue :")
        print(f"   → {e}")
    finally:
        input("\nAppuyez sur Entrée pour continuer...")


# ───────────────────────────────────────────────
#  IDENTITÉ
# ───────────────────────────────────────────────

def menu_identite():
    choix = menu("IDENTITÉ", [
        "🔎 Sherlock (pseudo)",
        "👤 Profil (nom/prenom)",
        "💼 Entreprise (Pappers / OSINT)",
        "📞 Téléphone",
        "🔙 Retour"
    ])

    match choix:
        case 0:
            username = input("🎯 Pseudo à rechercher : ").strip()

            if not username:
                print("[-] Pseudo invalide")
                return

            safe_run(sherlock_scan, username)

        case 1:
            name = input("👤 Nom / prénom : ").strip()

            if not name:
                print("[-] Nom invalide")
                return

            safe_run(search_person, name)

        case 2:
            name = input("🏢 Nom entreprise : ").strip()

            if not name:
                print("[-] Nom invalide")
                return

            safe_run(search_company, name)

        case 3:
            safe_run(search_phone)

        case 4:
            return

# ───────────────────────────────────────────────
#  MÉTADONNÉES
# ───────────────────────────────────────────────

def menu_metadonnees():
    choix = menu("MÉTADONNÉES", [
        "📸 Extraction EXIF",
        "🧹 Nettoyage EXIF",
        "🔍 Recherche visuelle (à venir)",
        "🔙 Retour"
    ])

    match choix:
        case 0:
            path = input("Chemin image : ").strip()
            safe_run(extract_exif_data, path)

        case 1:
            path = input("Chemin image : ").strip()
            overwrite = input("Écraser ? (o/N) : ").lower() == "o"
            safe_run(remove_metadata, path, overwrite)

        case 2:
            print("🚧 En développement")
            input("Entrée...")

        case 3:
            return


# ───────────────────────────────────────────────
#  RÉSEAU
# ───────────────────────────────────────────────

def menu_reseaux():
    choix = menu("RÉSEAUX", [
        "📡 Scan Nmap",
        "🌍 Cartographie",
        "🔙 Retour"
    ])

    match choix:
        case 0:
            ip = input("IP : ").strip()
            safe_run(scan_ip, ip)

        case 1:
            safe_run(scan_network_auto)

        case 2:
            return


# ───────────────────────────────────────────────
#  MAIN
# ───────────────────────────────────────────────

def main():
    while True:
        choix = menu("OUTILS OSINT", [
            "👤 Identité",
            "📷 Métadonnées",
            "🌐 Réseaux",
            "❌ Quitter"
        ])

        match choix:
            case 0:
                menu_identite()
            case 1:
                menu_metadonnees()
            case 2:
                menu_reseaux()
            case 3:
                print("👋 Au revoir !")
                break


if __name__ == "__main__":
    main()
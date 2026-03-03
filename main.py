import os
import sys

from modules.analyse_exif import extract_exif_data
from modules.remove_exif import remove_metadata
from modules.nmap_scan import scan_ip
from modules.sherlock import run_sherlock
from tools.utils import clear_console
from wcwidth import wcswidth

# ───────────────────────────────────────────────
#  Gestion des touches (Windows + Linux)
# ───────────────────────────────────────────────
def get_key():
    if os.name == 'nt':
        import msvcrt
        key = msvcrt.getch()
        if key == b'\xe0':  # touche spéciale (flèches)
            return msvcrt.getch().decode()
        return key.decode()

    import tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(3)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    if key == '\x1b[A': return 'H'
    if key == '\x1b[B': return 'P'
    return key


# ───────────────────────────────────────────────
#  Menu stylé avec navigation au clavier
# ───────────────────────────────────────────────
def menu(options):
    index = 0
    width = max(wcswidth(opt) for opt in options) + 4

    while True:
        clear_console()

        print("╔" + "═" * width + "╗")
        print("║" + "OUTILS OSINT".center(width) + "║")
        print("╠" + "═" * width + "╣")

        for i, opt in enumerate(options):
            prefix = "👉 " if i == index else "   "
            line = prefix + opt
            padding = width - wcswidth(line)
            print(f"║{line}{' ' * padding}║")

        print("╚" + "═" * width + "╝")

        key = get_key()

        if key == 'H':
            index = (index - 1) % len(options)
        elif key == 'P':
            index = (index + 1) % len(options)
        elif key in ('\r', '\n'):
            return index


# ───────────────────────────────────────────────
#  Programme principal
# ───────────────────────────────────────────────
def main():
    options = [
        "📸 Lire les métadonnées EXIF",
        "🧹 Supprimer les métadonnées d'une image",
        "🌐 Sherlock (username)",
        "📡 Scan de ports",
        "❌ Quitter"
    ]

    while True:
        choix = menu(options)

        if choix == 0:
            path = input("\nChemin de l'image à analyser : ").strip()
            extract_exif_data(path)
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == 1:
            path = input("\nChemin de l'image à nettoyer : ").strip()
            overwrite = input("Écraser le fichier original ? (o/N) : ").strip().lower() == "o"
            remove_metadata(path, overwrite)
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == 2:
            run_sherlock()
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == 3:
            ip = input("\nAdresse IP à scanner : ").strip()
            scan_ip(ip)
            input("\nAppuyez sur Entrée pour revenir au menu...")


        else:
            print("\n👋 Au revoir !")
            break


if __name__ == "__main__":
    main()
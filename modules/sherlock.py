import subprocess
from tools.utils import clear_console

def run_sherlock():
    clear_console()
    print("🔎 Recherche Sherlock\n")

    username = input("Nom d'utilisateur à rechercher : ").strip()

    if not username:
        print("\n❌ Aucun nom fourni.")
        input("\nAppuyez sur Entrée pour revenir au menu...")
        return

    print("\n⏳ Recherche en cours...\n")

    try:
        command = ["python", "-m", "sherlock_project", username, "--print-found"]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )

        print(result.stdout)

    except subprocess.TimeoutExpired:
        print("⏳ Temps dépassé : Sherlock a mis trop longtemps à répondre.")
        print("💡 Astuce : essaye un autre pseudo ou augmente le timeout.")

    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution de Sherlock : {e}")

    input("\n🔁 Appuyez sur Entrée pour revenir au menu...")
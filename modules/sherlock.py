import subprocess
import os
import signal
from datetime import datetime

SITES = [
    "twitter", "instagram", "facebook", "tiktok", "linkedin",
    "github", "gitlab", "reddit", "pinterest", "twitch"
]

OUTPUT_DIR = "modules/data"

# -----------------------------
# RUN SHERLOCK
# -----------------------------
def run_sherlock(username: str, sites: list, timeout_per_site: int = 5, module: str = "sherlock_project"):

    cmd = [
        "python", "-m", module, username,
        "--print-found",
        "--timeout", str(timeout_per_site)
    ]

    for site in sites:
        cmd += ["--site", site]

    print(f"[+] Sites chargés : {len(sites)}")

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        output_lines = []
        global_timeout = len(sites) * timeout_per_site + 5  # marge

        try:
            for line in process.stdout:
                line = line.strip()

                # Filtrage intelligent
                if (
                    line.startswith("[+]") or
                    line.startswith("[!]") or
                    "Search completed" in line or
                    "Error" in line
                ):
                    print(line)

                output_lines.append(line + "\n")

            process.wait(timeout=global_timeout)

        except subprocess.TimeoutExpired:
            print("⏳ Timeout global atteint. Arrêt forcé.")
            process.kill()
            output_lines.append("\n[!] Timeout global atteint.\n")

        return output_lines

    except FileNotFoundError:
        print("❌ Sherlock n'est pas installé ou introuvable.")
        return []

    except Exception as e:
        print(f"❌ Erreur : {e}")
        return []


# -----------------------------
# SAVE RESULTS
# -----------------------------
def save_results(username: str, output_lines: list):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"sherlock_{username}_{timestamp}.txt"
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print(f"[+] Résultats sauvegardés dans : {output_path}")


# -----------------------------
# FUNCTION
# -----------------------------
def sherlock_scan(username: str):
    if not SITES:
        print("❌ Aucun site chargé.")
        return

    output = run_sherlock(username, SITES)

    if not output:
        print("❌ Aucun résultat à sauvegarder.")
        return

    save_results(username, output)

# -----------------------------
# MAIN
# -----------------------------
def main():
    print("\nSherlock OSINT Tool")

    username = input("Pseudo : ").strip()

    if not username:
        print("❌ Username vide.")
        return

    sherlock_scan(username)


if __name__ == "__main__":
    main()

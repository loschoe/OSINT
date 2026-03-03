import subprocess

INTERESTING_SERVICES = [
    "ssh", "http", "https", "ftp",
    "microsoft-ds", "rdp",
    "mysql", "smtp", "domain"
]

def scan_ip(ip):
    try:
        print("\n[+] Scan rapide en cours (30s max)...")
        print("-" * 50)

        result = subprocess.run(
            [
                "nmap",
                "-sT",
                "-F",
                "-sV",                 
                "--open",
                "--host-timeout", "30s",
                ip
            ],
            capture_output=True,
            text=True,
            timeout=35
        )

        output = result.stdout
        found = []

        for line in output.split("\n"):
            if "/tcp" in line and "open" in line:
                parts = line.split()
                service = parts[2] if len(parts) > 2 else ""

                for interesting in INTERESTING_SERVICES:
                    if interesting in service:
                        found.append(parts)

        if found:
            print("[✔] Services exploitables détectés :\n")
            print("{:<10} {:<10} {:<15}".format("PORT", "SERVICE", "VERSION"))
            print("-" * 50)

            for item in found:
                port = item[0]
                service = item[2]
                version = " ".join(item[3:]) if len(item) > 3 else "unknown"

                print("{:<10} {:<15} {:<15}".format(port, service, version))
        else:
            print("\n[-] Aucun service exploitable détecté.")

        print("\n" + "-" * 50)

    except subprocess.TimeoutExpired:
        print("\n[!] Scan interrompu : délai dépassé (30s).")

    except FileNotFoundError:
        print("Erreur : Nmap non installé.")

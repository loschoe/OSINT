import subprocess
import shutil
from tools.utils import save_report

INTERESTING_SERVICES = [
    "ssh", "http", "https", "ftp",
    "microsoft-ds", "rdp",
    "mysql", "smtp", "domain"
]

def scan_ip(ip):
    if not shutil.which("nmap"):
        print("❌ Nmap non installé.")
        return

    try:
        print("\n[+] Scan discret en cours...")
        print("-" * 50)

        result = subprocess.run(
            [
                "nmap",
                "-sS",
                "--top-ports", "50",
                "-sV",
                "--open",
                "-T2",
                ip
            ],
            capture_output=True,
            text=True,
            timeout=60
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

        report = f"SCAN IP REPORT\nIP: {ip}\n\n"

        if found:
            print("[✔] Services détectés :\n")
            print("{:<10} {:<10} {:<20}".format("PORT", "SERVICE", "VERSION"))
            print("-" * 50)

            report += "PORT\tSERVICE\tVERSION\n"

            for item in found:
                port = item[0]
                service = item[2]
                version = " ".join(item[3:]) if len(item) > 3 else "unknown"

                print("{:<10} {:<15} {:<20}".format(port, service, version))
                report += f"{port}\t{service}\t{version}\n"

        else:
            print("\n[-] Aucun service intéressant détecté.")
            report += "Aucun service intéressant détecté.\n"

        path = save_report(f"scan_ip_{ip.replace('.', '_')}", report)
        print(f"\n💾 Rapport sauvegardé : {path}")

        print("\n" + "-" * 50)

    except subprocess.TimeoutExpired:
        print("\n[!] Scan interrompu (timeout).")
import subprocess
import shutil
import socket
from tools.utils import save_report 

def get_local_network():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        base = ".".join(local_ip.split(".")[:3]) + ".0/24"
        return base
    except:
        return None


def scan_network_auto():
    if not shutil.which("nmap"):
        print("❌ Nmap non installé.")
        return

    network = get_local_network()

    if not network:
        print("❌ Impossible de détecter le réseau.")
        return

    print(f"\n📡 Réseau détecté : {network}")
    print("[+] Scan en cours...")
    print("-" * 70)

    try:
        result = subprocess.run(
            ["nmap", "-sn", network],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout

        devices = {}
        current_ip = None

        for line in output.split("\n"):
            if "Nmap scan report for" in line:
                current_ip = line.split()[-1]
                devices[current_ip] = {
                    "mac": "N/A",
                    "vendor": "Unknown"
                }

            elif "MAC Address" in line and current_ip:
                mac_part = line.split("MAC Address:")[1].strip()

                if "(" in mac_part:
                    mac, vendor = mac_part.split("(", 1)
                    vendor = vendor.replace(")", "").strip()
                else:
                    mac = mac_part
                    vendor = "Unknown"

                devices[current_ip]["mac"] = mac.strip()
                devices[current_ip]["vendor"] = vendor

        report = f"NETWORK SCAN REPORT\nNetwork: {network}\n\n"

        if devices:
            print(f"[✔] {len(devices)} appareil(s) détecté(s) :\n")

            print("{:<16} {:<20} {:<30}".format("IP", "MAC", "CONSTRUCTEUR"))
            print("-" * 70)

            report += "IP\tMAC\tVENDOR\n"

            for ip, info in devices.items():
                print("{:<16} {:<20} {:<30}".format(
                    ip,
                    info["mac"],
                    info["vendor"]
                ))

                report += f"{ip}\t{info['mac']}\t{info['vendor']}\n"

        else:
            print("[-] Aucun appareil détecté.")
            report += "Aucun appareil détecté.\n"

        path = save_report("network_scan", report)
        print(f"\n💾 Rapport sauvegardé : {path}")

        print("-" * 70)

    except subprocess.TimeoutExpired:
        print("[!] Scan interrompu (timeout).")
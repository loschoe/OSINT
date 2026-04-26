import exifread
import os
from datetime import datetime

# ---------------------------------------------------------
# Conversion GPS (version complète et précise)
# ---------------------------------------------------------
def convert_to_degrees(value):
    try:
        d = value.values[0].num / value.values[0].den
        m = value.values[1].num / value.values[1].den
        s = value.values[2].num / value.values[2].den
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None


# ---------------------------------------------------------
# Extraction EXIF
# ---------------------------------------------------------
def extract_exif_data(image_path):

    if not os.path.isfile(image_path):
        print(f"[!] Fichier non trouvé : {image_path}")
        return

    try:
        with open(image_path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        if not tags:
            print("[!] Aucune donnée EXIF trouvée.")
            return

        # ---------------------------------------------------------
        # Construction d’un dictionnaire propre
        # ---------------------------------------------------------
        data = {}

        data["Appareil"] = f"{tags.get('Image Make', 'Inconnu')} {tags.get('Image Model', '')}".strip()
        data["Résolution"] = f"{tags.get('EXIF ExifImageWidth', 'N/A')} x {tags.get('EXIF ExifImageLength', 'N/A')}"
        data["Date prise"] = str(tags.get("EXIF DateTimeOriginal", "Inconnue"))

        flash_tag = tags.get("EXIF Flash")
        if flash_tag:
            data["Flash"] = "ON" if "fired" in str(flash_tag).lower() else "OFF"
        else:
            data["Flash"] = "Inconnu"

        # ---------------------------------------------------------
        # GPS
        # ---------------------------------------------------------
        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            lat = convert_to_degrees(tags["GPS GPSLatitude"])
            lon = convert_to_degrees(tags["GPS GPSLongitude"])

            if tags.get("GPS GPSLatitudeRef", "N") == "S":
                lat = -lat
            if tags.get("GPS GPSLongitudeRef", "E") == "W":
                lon = -lon

            if lat is not None and lon is not None:
                data["GPS"] = f"{lat:.6f}, {lon:.6f}"
                data["Google Maps"] = f"https://www.google.com/maps?q={lat},{lon}"
            else:
                data["GPS"] = "Données GPS invalides"
        else:
            data["GPS"] = "Aucune donnée GPS"

        # ---------------------------------------------------------
        # Affichage console propre
        # ---------------------------------------------------------
        print("\n" + "=" * 50)
        print("📸  RÉSUMÉ EXIF".center(50))
        print("=" * 50)

        for key, value in data.items():
            print(f"{key:<15} : {value}")

        print("=" * 50)

        # ---------------------------------------------------------
        # Export vers fichier texte dans /data
        # ---------------------------------------------------------
        script_dir = os.path.dirname(os.path.abspath(__file__))  
        output_dir = os.path.join(script_dir, "data")           
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, "donnees_exif.txt")

        # Date simplifiée
        date_analyse = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("===== RÉSUMÉ EXIF =====\n")
            f.write(f"Fichier analysé : {image_path}\n")
            f.write(f"Date analyse    : {date_analyse}\n\n")

            for key, value in data.items():
                f.write(f"{key:<15} : {value}\n")

        print(f"\n📁 Données enregistrées dans : {output_file}\n")

    except Exception as e:
        print(f"[!] Erreur lors de l'analyse EXIF : {e}")

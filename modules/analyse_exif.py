import os
from PIL import Image
import exifread
from tools.utils import *


def convert_to_degrees(value):
    try:
        d = float(value.values[0])
        m = float(value.values[1])
        s = float(value.values[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None


def extract_exif_data(path):
    if not os.path.isfile(path):
        print("❌ Fichier introuvable.")
        return

    try:
        image = Image.open(path)
        width, height = image.size

        clear_console()
        print("\n🔎 Analyse EXIF")
        print("-" * 50)

        # Informations générales
        print(f"📏 Résolution : {width} x {height}")

        with open(path, "rb") as f:
            tags = exifread.process_file(f)

        # Appareil photo
        print("\n📷 Appareil photo")
        make = tags.get("Image Make")
        model = tags.get("Image Model")
        software = tags.get("Image Software")

        print(f"   • Marque : {make if make else 'Non disponible'}")
        print(f"   • Modèle : {model if model else 'Non disponible'}")
        print(f"   • Logiciel : {software if software else 'Non disponible'}")

        # Date
        print("\n🕒 Date")
        date = tags.get("EXIF DateTimeOriginal")
        print(f"   • Date prise : {date if date else 'Non disponible'}")

        # Flash
        print("\n⚡ Flash")
        flash_tag = tags.get("EXIF Flash")
        if flash_tag:
            flash_str = str(flash_tag).lower()
            print("   • Flash : ON" if "fired" in flash_str else "   • Flash : OFF")
        else:
            print("   • Flash : Non disponible")

        # Paramètres photo
        print("\n📸 Paramètres photo")
        iso = tags.get("EXIF ISOSpeedRatings")
        exposure = tags.get("EXIF ExposureTime")
        aperture = tags.get("EXIF FNumber")
        focal = tags.get("EXIF FocalLength")

        print(f"   • ISO : {iso if iso else 'Non disponible'}")
        print(f"   • Vitesse d'obturation : {exposure if exposure else 'Non disponible'}")
        print(f"   • Ouverture : f/{aperture if aperture else 'Non disponible'}")
        print(f"   • Focale : {focal if focal else 'Non disponible'}")

        # Orientation
        print("\n📐 Orientation")
        orientation = tags.get("Image Orientation")
        print(f"   • Orientation : {orientation if orientation else 'Non disponible'}")

        # GPS
        print("\n🌍 Géolocalisation")
        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            lat = convert_to_degrees(tags["GPS GPSLatitude"])
            lon = convert_to_degrees(tags["GPS GPSLongitude"])

            if lat and lon:
                lat_ref = tags.get("GPS GPSLatitudeRef")
                lon_ref = tags.get("GPS GPSLongitudeRef")

                if lat_ref and str(lat_ref) != "N":
                    lat = -lat
                if lon_ref and str(lon_ref) != "E":
                    lon = -lon

                print(f"   • Coordonnées : {lat:.6f}, {lon:.6f}")
                print(f"   • Google Maps : https://www.google.com/maps?q={lat:.6f},{lon:.6f}")
            else:
                print("   • Données GPS illisibles")
        else:
            print("   • Pas de données GPS disponibles")

        print("\n" + "-" * 50)

    except Exception as e:
        print(f"❌ Erreur : {e}")
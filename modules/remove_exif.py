import os
from PIL import Image


def remove_metadata(path, overwrite=False):
    """
    Supprime toutes les métadonnées d'une image.
    
    :param path: chemin de l'image
    :param overwrite: si True, écrase l'image originale
    """

    if not os.path.isfile(path):
        print("❌ Fichier introuvable.")
        return

    try:
        image = Image.open(path)

        # Copier uniquement les pixels
        data = list(image.getdata())
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(data)

        if overwrite:
            save_path = path
        else:
            base, ext = os.path.splitext(path)
            save_path = f"{base}_clean{ext}"

        # Sauvegarde sans EXIF
        if image.format == "JPEG":
            clean_image.save(save_path, "JPEG", quality=100)
        else:
            clean_image.save(save_path)

        print("🧹 Métadonnées supprimées avec succès.")
        print(f"💾 Fichier sauvegardé : {save_path}")

    except Exception as e:
        print(f"❌ Erreur : {e}")
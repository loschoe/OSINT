import os
import piexif

def remove_metadata(image_path, overwrite=False, output_path=None):
    """
    Supprime toutes les métadonnées EXIF d'une image (JPEG uniquement).
    
    Args:
        image_path (str): Chemin de l'image à traiter.
        overwrite (bool): Si True, écrase le fichier original.
        output_path (str): Chemin de sortie si overwrite=False.
    
    Returns:
        bool: True si suppression réussie, False sinon.
    """

    if not os.path.isfile(image_path):
        print(f"[!] Fichier non trouvé : {image_path}")
        return False

    ext = os.path.splitext(image_path)[1].lower()
    if ext not in [".jpg", ".jpeg"]:
        print(f"[!] Format non supporté ({ext}). Seules les images JPEG peuvent contenir des EXIF.")
        return False

    if overwrite:
        output_path = image_path
    else:
        if output_path is None:
            # On génère un fichier propre dans ./data/
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, "data")
            os.makedirs(data_dir, exist_ok=True)

            filename = os.path.basename(image_path)
            output_path = os.path.join(data_dir, f"clean_{filename}")

        # Création du dossier si nécessaire
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    try:
        piexif.remove(image_path, output_path)

        print("\n" + "=" * 50)
        print("🧹  MÉTADONNÉES SUPPRIMÉES".center(50))
        print("=" * 50)
        print(f"Image traitée : {image_path}")
        print(f"Image sortie  : {output_path}")
        print("=" * 50 + "\n")

        return True

    except Exception as e:
        print(f"[!] Erreur lors de la suppression EXIF : {e}")
        return False

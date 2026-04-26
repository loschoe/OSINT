## 🕵️‍♂️ OSINT Toolkit
OSINT Toolkit est un outil codé en python qui permet de rassembler des outils puissant tels que **sherlock**, **nmap** ou de pouvoir voir et supprimer les méta-données EXIF d'une image. 

## 🎯 Objectifs du projet
- Centraliser plusieurs outils OSINT dans une seule interface.
- Fournir une architecture modulaire facile à étendre.
- Permettre l’analyse d’images (EXIF), la recherche de profils, et le scan réseau.
- Offrir une base solide pour développer de nouveaux modules d’investigation.

## 📦 Fonctionnalités principales
- Analyse EXIF — extraction des métadonnées d’images (GPS, appareil, date…)
- Suppression EXIF — nettoyage complet des métadonnées sensibles
- Scan réseau Nmap — détection de ports ouverts et services
- Scan d'inventaire réseau - détection des appareils connectés à un réseau local 
- Recherche Sherlock — recherche de profils sur des centaines de plateformes
- Recherche d'informations concernant une entreprise  
- Recherche d'informations concernant un numéron de téléphone


## 📁 Arborescence du projet
```
OSINT/
│
├── main.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── __init__.py
│   ├── analyse_exif.py
│   ├── compagny_dork.py
│   ├── nmap_carto_scan.py
│   ├── nmap_scan.py
│   ├── person_dork.py
│   ├── phone_search.py
│   ├── remove_exif.py
│   ├── nmap_scan.py
│   └── sherlock.py
│
├── tools/
    ├── img_demo
    └── utils.py
```
## ⚙️ Installation
1. Cloner le dépôt
```bash
git clone https://github.com/loschoe/OSINT.git
cd OSINT
```
3. Installer les dépendances Python
`pip install -r requirements.txt`

4. Installer Nmap (obligatoire pour le module réseau)
- Windows : https://nmap.org/download.html (nmap.org in Bing)
- Linux : sudo apt install nmap
- macOS : brew install nmap

## 🚀 Utilisation
Lancer le menu principal :
```py
python main.py
```
Le menu permet d’accéder à 3 catégories :
- Identité : `Sherlock` ; `Profil` ; `Entreprise` ; `Téléphone`
- Métadonnées : `Exif`
- Réseaux : `Scan` ; `Cartographie`
- *Modules additionnels (viendrons plus tard)*

## 🧩 Ajouter un module OSINT
- Créer un fichier dans modules/
- Ajouter une fonction principale 
- Importer la fonction dans main.py
- Ajouter une entrée dans le menu
L’architecture est pensée pour être extensible sans casser le reste du projet.

## 🛠️ Technologies utilisées
- Python 3.11+
- Nmap / python-nmap 
- Sherlock (sherlock-project)
- Pillow / ExifRead / piexif 
- wcwidth
- requests
- phonenumbers
- beautifulsoup4
- lxml

📜 Licence
Projet open-source. Libre d’utilisation, de modification et de distribution.

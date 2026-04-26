import urllib.parse

def search_company(name):
    print("\n🏢 OSINT ENTREPRISE\n")

    encoded = urllib.parse.quote(name)

    links = {
        "Pappers": f"https://www.pappers.fr/recherche?q={encoded}",
        "Societe.com": f"https://www.google.com/search?q=site%3Asociete.com+%22{encoded}%22",
        "Infogreffe": f"https://www.google.com/search?q=site%3Ainfogreffe.fr+%22{encoded}%22",
        "Google SIREN": f"https://www.google.com/search?q=%22{encoded}%22+SIREN+France",
        "LinkedIn": f"https://www.google.com/search?q=site%3Alinkedin.com%2Fcompany+%22{encoded}%22"
    }

    for name, url in links.items():
        print(f"🔹 {name}")
        print(f"   👉 {url}")

    print("\n💡 Clique sur les liens")
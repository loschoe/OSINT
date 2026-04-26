import urllib.parse

def search_person(name):
    print("\n🔎 OSINT PERSON SEARCH\n")

    encoded = urllib.parse.quote(name)

    links = {
        "Google": f"https://www.google.com/search?q={encoded}",
        "LinkedIn": f"https://www.google.com/search?q=site%3Alinkedin.com+%22{encoded}%22",
        "Facebook": f"https://www.google.com/search?q=site%3Afacebook.com+%22{encoded}%22",
        "Instagram": f"https://www.google.com/search?q=site%3Ainstagram.com+%22{encoded}%22",
        "Twitter/X": f"https://www.google.com/search?q=site%3Atwitter.com+%22{encoded}%22",
        "TikTok": f"https://www.google.com/search?q=site%3Atiktok.com+%22{encoded}%22",
        "GitHub": f"https://www.google.com/search?q=site%3Agithub.com+%22{encoded}%22",
        "Email leaks": f"https://www.google.com/search?q=%22{encoded}%22+email",
    }

    for label, url in links.items():
        print(f"🔹 {label}")
        print(f"   👉 {url}\n")

    print("💡 Clique sur les résultats")
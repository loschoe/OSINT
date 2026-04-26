import os
import datetime 

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_report(filename, content):
    os.makedirs("modules/data", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"modules/data/{filename}_{timestamp}.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path
import os
import subprocess
import argparse
import requests

# GitHub API URL
GITHUB_API_URL = "https://api.github.com/user/repos"

def create_or_update_github_repo(token, repo_name):
    """
    Erstellt ein privates GitHub-Repository oder erkennt, ob es bereits existiert und aktualisiert es.
    
    Args:
        token (str): Der GitHub-Token für die Authentifizierung.
        repo_name (str): Der Name des Repositories, das erstellt oder aktualisiert werden soll.
    
    Returns:
        str: Die URL des GitHub-Repositories.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Prüfe, ob das Repository bereits existiert
    repo_url = f"https://api.github.com/repos/hellmader/{repo_name}"
    response = requests.get(repo_url, headers=headers)

    if response.status_code == 404:
        # Repository existiert nicht, also erstellen wir es
        data = {
            "name": repo_name,
            "private": True
        }

        response = requests.post(GITHUB_API_URL, json=data, headers=headers)

        if response.status_code == 201:
            print(f"Privates Repository '{repo_name}' erfolgreich erstellt.")
            return f"https://github.com/hellmader/{repo_name}.git"
        else:
            print(f"Fehler beim Erstellen des Repositories: {response.json()}")
            return None
    elif response.status_code == 200:
        print(f"Repository '{repo_name}' existiert bereits, wird aktualisiert.")
        return f"https://github.com/hellmader/{repo_name}.git"
    else:
        print(f"Fehler beim Überprüfen des Repository-Status: {response.json()}")
        return None

def setup_git_config():
    """
    Setzt die Git-Konfiguration für den globalen Benutzername und die E-Mail-Adresse.
    
    Die Werte sind festgelegt auf:
    - Name: Michael Mader
    - E-Mail: m.mader@hellpower.at
    """
    try:
        subprocess.run(["git", "config", "--global", "user.name", "Michael Mader"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "m.mader@hellpower.at"], check=True)
        print("Git-Konfiguration erfolgreich festgelegt.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Setzen der Git-Konfiguration: {e}")

def push_to_github(token, repo_url, directory_path):
    """
    Initialisiert ein Git-Repository, erstellt einen Commit und pusht es in ein GitHub-Repository.

    Args:
        token (str): Der GitHub-Token für die Authentifizierung.
        repo_url (str): Die URL des GitHub-Repositories.
        directory_path (str): Der Pfad zum Verzeichnis, das hochgeladen werden soll.
    """
    try:
        # Wechsle in das Verzeichnis
        os.chdir(directory_path)

        # Initialisiere Git-Repository oder nutze bestehendes Repository
        if not os.path.exists('.git'):
            subprocess.run(["git", "init"], check=True)
        else:
            print("Git-Repository existiert bereits, wird aktualisiert.")

        # Füge alle Dateien hinzu
        subprocess.run(["git", "add", "."], check=True)

        # Erstelle einen Commit
        subprocess.run(["git", "commit", "-m", "Update Repository"], check=True)

        # Setze das Remote-Repository
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=False)

        # Push mit Token
        correct_repo_url = repo_url.replace("https://", f"https://{token}@")
        subprocess.run(["git", "push", correct_repo_url, "--all"], check=True)
        print("Push erfolgreich.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Pushen ins GitHub-Repository: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

def get_last_directory_name(directory_path):
    """
    Extrahiert den letzten Teil des Verzeichnispfads, um ihn als Repository-Namen zu verwenden.

    Args:
        directory_path (str): Der Pfad zum Verzeichnis.

    Returns:
        str: Der letzte Verzeichnisname.
    """
    return os.path.basename(os.path.normpath(directory_path))

def main():
    """
    Hauptfunktion, die den Benutzerinput verarbeitet und die entsprechenden Funktionen aufruft.
    """
    parser = argparse.ArgumentParser(description="Verzeichnis in ein privates GitHub-Repository hochladen.")
    parser.add_argument("token", help="GitHub-Token für die Authentifizierung")
    parser.add_argument("directory_path", help="Pfad zum Verzeichnis")
    
    args = parser.parse_args()

    # Git-Konfiguration festlegen
    setup_git_config()

    # Erhalte den letzten Verzeichnisnamen als Repository-Namen
    repo_name = get_last_directory_name(args.directory_path)

    # Erstelle oder aktualisiere das GitHub-Repository
    repo_url = create_or_update_github_repo(args.token, repo_name)

    if repo_url:
        # Verzeichnis zu GitHub pushen
        push_to_github(args.token, repo_url, args.directory_path)

if __name__ == "__main__":
    main()

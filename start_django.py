import subprocess
import webbrowser
import os
import socket
import time

def is_port_in_use(port=8000):
    """ Vérifie si le port est déjà utilisé """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def start_django_server():
    """ Démarre le serveur Django et ouvre immédiatement le navigateur """
    django_project_path = os.path.dirname(os.path.abspath(__file__))  # Répertoire courant
    manage_py_path = os.path.join(django_project_path, "manage.py")  # Chemin vers manage.py

    if not os.path.exists(manage_py_path):
        print(f"❌ Erreur : Le fichier {manage_py_path} est introuvable.")
        return None

    # Vérifier si le serveur est déjà en cours d'exécution
    if is_port_in_use():
        print("🚀 Le serveur Django est déjà en cours d'exécution.")
    else:
        # Lancer le serveur Django en arrière-plan
        process = subprocess.Popen(
            ["python", manage_py_path, "runserver"],  # Utilisation de manage.py pour démarrer le serveur
            cwd=django_project_path,  # Définit le répertoire de travail pour le processus
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        print("⏳ Démarrage du serveur Django...")
        time.sleep(3)  # Laisser un peu de temps pour démarrer le serveur

    # Ouvrir immédiatement le navigateur
    webbrowser.open("http://127.0.0.1:8000")
    print("✅ Navigateur ouvert sur le serveur Django.")

if __name__ == "__main__":
    start_django_server()

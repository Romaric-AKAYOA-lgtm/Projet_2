import os
import sys
import webbrowser

import threading  # Importer le module threading

def run_django_server():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestion_visite.settings')
    
    # Simuler la commande 'runserver' pour démarrer le serveur Django sans auto-rechargement
    sys.argv = ['manage.py', 'runserver', '--noreload']
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    # Démarrer le serveur Django dans un thread séparé
    server_thread = threading.Thread(target=run_django_server)
    server_thread.start()

    # Ouvrir automatiquement le navigateur après un délai pour être sûr que le serveur est lancé
    import time
    time.sleep(2)  # Attendre 2 secondes pour être sûr que le serveur est bien démarré
    webbrowser.open('http://127.0.0.1:8000/')

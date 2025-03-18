from setuptools import setup, find_packages

# Lire le fichier requirements.txt
with open('requirements.txt') as f:
    required = f.readlines()

# Nettoyer les lignes (enlever les retours à la ligne)
required = [r.strip() for r in required]

setup(
    name='Gestion_visite',  # Le nom de ton application
    version='1.0',  # La version de ton application
    packages=find_packages(),  # Trouve tous les packages dans ton projet
    install_requires=required,  # Utilise les dépendances de requirements.txt
    entry_points={
        'console_scripts': [
            'start-django=Gestion_visite.start_server:main',  # Commande personnalisée
        ],
    },
)

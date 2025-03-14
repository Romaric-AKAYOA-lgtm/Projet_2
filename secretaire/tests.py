# secretaire/tests.py
from django.test import TestCase
from .models import Secretaire

class SecretaireTestCase(TestCase):
    def test_creation_secretaire(self):
        secretaire = Secretaire.objects.create_user(
            username="secretaire1",
            email="secretaire@example.com",
            password="motdepasse123",
            first_name="Marie",   # Utilisation du champ first_name
            last_name="Dupont",     # Utilisation du champ last_name
            num_tel="+1234567890",
            # specialite="Gestion administrative",
            # date_debut="2024-03-01"
        )
        print(f"Secrétaire {secretaire.username} créée avec succès.")
        # Vérification simple
        self.assertEqual(secretaire.first_name, "Marie")
        self.assertEqual(secretaire.last_name, "Dupont")

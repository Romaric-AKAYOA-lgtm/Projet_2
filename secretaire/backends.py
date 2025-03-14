from django.contrib.auth.backends import BaseBackend
from .models import Secretaire
from django.contrib.auth.hashers import check_password

class SecretaireBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Cette méthode tente d'authentifier un utilisateur en fonction de son nom d'utilisateur et de son mot de passe.
        Elle retourne l'instance de Secretaire si l'authentification réussit, sinon elle retourne None.
        """
        try:
            # Recherche un secrétaire dans la base de données par son nom d'utilisateur
            secretaire = Secretaire.objects.get(username=username)
            # Vérifie si le mot de passe fourni correspond au mot de passe haché stocké
            if check_password(password, secretaire.password):
                return secretaire  # Retourne l'utilisateur si l'authentification est réussie
            else:
                return None  # Retourne None si le mot de passe est incorrect
        except Secretaire.DoesNotExist:
            # Si l'utilisateur n'existe pas, retourne None
            return None

    def get_user(self, user_id):
        """
        Cette méthode retourne l'utilisateur correspondant à l'ID passé en paramètre.
        Si l'utilisateur n'existe pas, elle retourne None.
        """
        try:
            # Recherche et retourne le secrétaire en fonction de son ID
            return Secretaire.objects.get(pk=user_id)
        except Secretaire.DoesNotExist:
            # Si aucun secrétaire n'est trouvé avec cet ID, retourne None
            return None

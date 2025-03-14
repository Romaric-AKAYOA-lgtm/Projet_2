from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Secretaire(models.Model):
    username = models.CharField(max_length=150, unique=True)  
    password = models.CharField(max_length=128)  
    email = models.EmailField(max_length=40, unique=True, null=True, blank=True, default='example@example.com')
    num_tel = models.CharField(max_length=15, blank=True, null=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        """Hache le mot de passe avant de l'enregistrer."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Vérifie si le mot de passe saisi correspond au mot de passe haché."""
        return check_password(raw_password, self.password)

    @classmethod
    def authenticate(cls, username, password):
        """Vérifie les identifiants de l'utilisateur."""
        try:
            secretaire = cls.objects.get(username=username)
            if secretaire.check_password(password):
                return secretaire
        except cls.DoesNotExist:
            return None

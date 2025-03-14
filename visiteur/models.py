from django.db import models

class Visiteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=50, choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')])
    type_visiteur = models.CharField(max_length=50)
    contact = models.CharField(max_length=100)
    email = models.EmailField(max_length=40, unique=True, default='example@example.com')

    def __str__(self):
        return f"{self.nom} {self.prenom}"

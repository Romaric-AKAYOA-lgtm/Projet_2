from django.db import models

# Create your models here.

class Directeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=40, unique=True, default='example@example.com')

    num_tel = models.CharField(
        max_length=15, 
        unique=True, 
        error_messages={"unique": "Ce numéro est déjà utilisé."}
    )
    adresse = models.CharField(max_length=60)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M')
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

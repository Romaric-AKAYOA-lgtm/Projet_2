from django.db import models

# Create your models here.

# Modèle pour la gestion des visites
class Visiteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    type_visiteur = models.CharField(max_length=50)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Directeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Secretaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Visite(models.Model):
    date = models.DateField()
    heure = models.TimeField()
    objet = models.TextField()
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    directeur = models.ForeignKey(Directeur, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=[('confirmé', 'Confirmé'), ('annulé', 'Annulé')], default='confirmé')

class ProgrammeVisite(models.Model):
    visite = models.ForeignKey(Visite, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('validé', 'Validé')], default='en attente')
    date_creation = models.DateTimeField(auto_now_add=True)











from django.db import models
from visite.models import Visite
from secretaire.models import Secretaire  # Remplacez 'votre_app' par le nom de votre application

class ProgrammeVisite(models.Model):
    visite = models.ForeignKey(Visite, on_delete=models.CASCADE)
    secretaire = models.ForeignKey(Secretaire, on_delete=models.CASCADE)  # Ajout de la clé étrangère pour la secrétaire
    statut = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('validé', 'Validé')], default='en attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    heure_debut = models.DateTimeField()  # Ajout de l'heure de début
    heure_fin = models.DateTimeField(null=True, blank=True)    # Ajout de l'heure de fin

    def __str__(self):
        return f"Programme pour visite {self.visite.id} - {self.statut}"

from django.db import models
from visiteur.models import Visiteur
from directeur.models import Directeur

class Visite(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)  # Date de création automatique
    date_visite = models.DateField()  
    heure_visite = models.TimeField()  
    objet = models.TextField()
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    directeur = models.ForeignKey(Directeur, on_delete=models.CASCADE)
    
    STATUT_CHOICES = [('confirmé', 'Confirmé'), ('annulé', 'Annulé')]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='confirmé')
    
    # Champ motif_annulation avec des choix spécifiques
    MOTIF_CHOICES = [
        ('indisponible_directeur', 'Indisponibilité du directeur'),
        ('ajourné_visiteur', 'Ajournement du visiteur'),
    ]
    motif_annulation = models.CharField(max_length=50, choices=MOTIF_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Visite de {self.visiteur.nom} {self.visiteur.prenom} avec {self.directeur.nom} {self.directeur.prenom}"

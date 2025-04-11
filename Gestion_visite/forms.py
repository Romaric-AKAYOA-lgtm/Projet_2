from django import forms

from programme_visite.models import ProgrammeVisite
from visite.models import Visite
from visiteur.models import Visiteur
from directeur.models import Directeur
from secretaire.models import Secretaire
from django.forms import RadioSelect

# Formulaire combiné pour Visite et ProgrammeVisite
class VisiteProgrammeForm(forms.Form):
    # ----- Champs pour le modèle Visite -----
    date_creation = forms.DateTimeField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)  # Date de création automatique
    date_visite = forms.DateField(required=True)  # Date de la visite
    heure_visite = forms.TimeField(required=True)  # Heure de la visite
    objet = forms.CharField(max_length=500, required=True)  # Objet de la visite
    visiteur = forms.ModelChoiceField(queryset=Visiteur.objects.all(), required=True)  # Visiteur associé à la visite
    directeur = forms.ModelChoiceField(queryset=Directeur.objects.all(), required=True)  # Directeur associé à la visite
    statut = forms.ChoiceField(choices=Visite.STATUT_CHOICES, required=True)  # Statut de la visite
    motif_annulation = forms.ChoiceField(choices=Visite.MOTIF_CHOICES, required=False)  # Motif d'annulation
    
    # ----- Champs pour le modèle ProgrammeVisite -----
    secretaire = forms.ModelChoiceField(queryset=Secretaire.objects.all(), required=True)  # Secrétaire associé au programme
    statut_programme = forms.ChoiceField(choices=[('en attente', 'En attente'), ('validé', 'Validé')], required=True)  # Statut du programme
    date_creation_programme = forms.DateTimeField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)  # Date de création du programme
    heure_debut = forms.DateTimeField(required=True)  # Heure de début du programme
    heure_fin = forms.DateTimeField(required=False)  # Heure de fin du programme
    motif_annulation_programme = forms.ChoiceField(choices=ProgrammeVisite.MOTIF_CHOICES, required=False)  # Motif d'annulation du programme

    def save(self):
        # Sauvegarde du modèle Visite
        visite = Visite(
            date_visite=self.cleaned_data['date_visite'],
            heure_visite=self.cleaned_data['heure_visite'],
            objet=self.cleaned_data['objet'],
            visiteur=self.cleaned_data['visiteur'],
            directeur=self.cleaned_data['directeur'],
            statut=self.cleaned_data['statut'],
            motif_annulation=self.cleaned_data.get('motif_annulation', None)
        )
        visite.save()

        # Sauvegarde du modèle ProgrammeVisite
        programme_visite = ProgrammeVisite(
            visite=visite,
            secretaire=self.cleaned_data['secretaire'],
            statut=self.cleaned_data['statut_programme'],
            date_creation=self.cleaned_data['date_creation_programme'],
            heure_debut=self.cleaned_data['heure_debut'],
            heure_fin=self.cleaned_data.get('heure_fin', None),
            motif_annulation=self.cleaned_data.get('motif_annulation_programme', None)
        )
        programme_visite.save()

        return visite, programme_visite

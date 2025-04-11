from django import forms
from django.core.exceptions import ValidationError
from datetime import time
from .models import Visite, Visiteur, Directeur

class VisiteForm(forms.ModelForm):
    class Meta:
        model = Visite
        fields = ['date_visite', 'heure_visite', 'objet', 'visiteur', 'directeur', 'statut', 'motif_annulation']  # Ajouter motif_annulation ici

    visiteur = forms.ModelChoiceField(queryset=Visiteur.objects.all(), required=True)
    directeur = forms.ModelChoiceField(queryset=Directeur.objects.all(), required=True)
    motif_annulation = forms.ChoiceField(choices=Visite.MOTIF_CHOICES, required=False)

    def clean(self):
        cleaned_data = super().clean()
        date_visite = cleaned_data.get('date_visite')
        heure_visite = cleaned_data.get('heure_visite')
        visiteur = cleaned_data.get('visiteur')
        statut = cleaned_data.get('statut')
        motif_annulation = cleaned_data.get('motif_annulation')

        # Vérifications de base
        if not date_visite:
            raise ValidationError("La date de la visite est obligatoire.")
        if not heure_visite:
            raise ValidationError("L'heure de la visite est obligatoire.")
        if not visiteur:
            raise ValidationError("Le visiteur doit être spécifié.")
        if statut not in ['confirmé', 'annulé']:
            raise ValidationError("Le statut de la visite doit être 'confirmé' ou 'annulé'.")

        # Vérification que l'heure de la visite est entre 8h et 14h
        if heure_visite:
            if heure_visite < time(8, 0) or heure_visite > time(14, 0):
                raise ValidationError("L'heure de la visite doit être comprise entre 8h et 14h.")

        # Vérification d'une visite existante à la même date et heure
        if Visite.objects.filter(date_visite=date_visite, heure_visite=heure_visite).exists():
            raise ValidationError(f"Une visite est déjà prévue à {heure_visite} le {date_visite}.")

        # Vérification du motif d'annulation si le statut est 'annulé'
        if statut == 'annulé' and not motif_annulation:
            raise ValidationError("Le motif d'annulation doit être spécifié si la visite est annulée.")

        return cleaned_data

from django import forms
from .models import ProgrammeVisite
from django.utils import timezone
from datetime import time, timedelta

class ProgrammeVisiteForm(forms.ModelForm):
    class Meta:
        model = ProgrammeVisite
        fields = ['visite', 'secretaire', 'statut', 'heure_debut', 'heure_fin']

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')

        # Validation pour vérifier que l'heure de fin est après l'heure de début
        if heure_debut and heure_fin and heure_debut >= heure_fin:
            raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")

        # Vérification que les heures sont comprises entre 8h et 16h
        if heure_debut:
            if heure_debut.time() < time(8, 0) or heure_debut.time() > time(16, 0):
                raise forms.ValidationError("L'heure de début doit être comprise entre 08:00 et 16:00.")
        
        if heure_fin:
            if heure_fin.time() < time(8, 0) or heure_fin.time() > time(16, 0):
                raise forms.ValidationError("L'heure de fin doit être comprise entre 08:00 et 16:00.")
        
        # Vérification que si l'heure de début est après 16h, on reporte au jour suivant
        if heure_debut and heure_debut.time() > time(16, 0):
            cleaned_data['heure_debut'] = heure_debut + timedelta(days=1)
        
        if heure_fin and heure_fin.time() > time(16, 0):
            cleaned_data['heure_fin'] = heure_fin + timedelta(days=1)

        return cleaned_data

from django import forms
from .models import ProgrammeVisite
from datetime import datetime, time

class ProgrammeVisiteForm(forms.ModelForm):
    class Meta:
        model = ProgrammeVisite
        fields = ['visite', 'secretaire', 'statut', 'heure_debut', 'heure_fin']

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')

        # Vérifier que l'heure de début et l'heure de fin sont valides
        if heure_debut and heure_fin:
            # 1️⃣ Vérification que l'heure de fin est après l'heure de début
            if heure_debut >= heure_fin:
                raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")

            # 2️⃣ Vérification que l'heure de début est comprise entre 08:00 et 16:00
            if not (time(8, 0) <= heure_debut.time() <= time(16, 0)):
                raise forms.ValidationError("L'heure de début doit être entre 08:00 et 16:00.")
            
            # 3️⃣ Vérification que l'heure de fin est comprise entre 08:00 et 16:00
            if not (time(8, 0) <= heure_fin.time() <= time(16, 0)):
                raise forms.ValidationError("L'heure de fin doit être entre 08:00 et 16:00.")

        return cleaned_data

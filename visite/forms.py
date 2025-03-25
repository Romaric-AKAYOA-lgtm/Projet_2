from django import forms
from django.core.exceptions import ValidationError
from .models import Visite, Visiteur, Directeur  # Assurez-vous que ces modèles existent

class VisiteForm(forms.ModelForm):
    class Meta:
        model = Visite
        fields = ['date_visite', 'heure_visite', 'objet', 'visiteur', 'directeur', 'statut']

    visiteur = forms.ModelChoiceField(queryset=Visiteur.objects.all(), required=True)
    directeur = forms.ModelChoiceField(queryset=Directeur.objects.all(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        date_visite = cleaned_data.get('date_visite')
        heure_visite = cleaned_data.get('heure_visite')
        visiteur = cleaned_data.get('visiteur')
        statut = cleaned_data.get('statut')

        if not date_visite:
            raise ValidationError("La date de la visite est obligatoire.")
        if not heure_visite:
            raise ValidationError("L'heure de la visite est obligatoire.")
        if not visiteur:
            raise ValidationError("Le visiteur doit être spécifié.")
        if statut not in ['confirmé', 'annulé']:
            raise ValidationError("Le statut de la visite doit être 'confirmé' ou 'annulé'.")

        # Vérification d'une visite existante à la même date et heure
        if Visite.objects.filter(date_visite=date_visite, heure_visite=heure_visite, visiteur=visiteur).exists():
            raise ValidationError(f"Une visite est déjà prévue pour {visiteur.nom} {visiteur.prenom} à cette date et heure.")

        return cleaned_data

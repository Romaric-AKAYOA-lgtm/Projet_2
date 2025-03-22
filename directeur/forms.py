from datetime import date
from django import forms
from .models import Directeur
import re
from django.core.exceptions import ValidationError
from datetime import date
from django.utils.timezone import now

class DirecteurForm(forms.ModelForm):
    class Meta:
        model = Directeur
        fields = ['nom', 'prenom', 'email','date_naissance', 'lieu_naissance', 'num_tel', 'adresse', 'sexe', 'date_debut', 'date_fin']

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        
        # Vérification que le nom ne contient pas de chiffres ni de caractères spéciaux
        if any(char.isdigit() for char in nom) :
            raise ValidationError("Le nom ne doit contenir que des lettres, sans chiffres ni caractères spéciaux.")
        
        # Vérification que le nom n'est pas vide
        if not nom:
            raise ValidationError("Le nom est obligatoire.")
        
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data['prenom']
        
        # Vérification que le prénom ne contient pas de chiffres ni de caractères spéciaux
        if any(char.isdigit() for char in prenom):
            raise ValidationError("Le prénom ne doit contenir que des lettres, sans chiffres ni caractères spéciaux.")
        
        return prenom

    def clean_date_fin(self):
        date_debut = self.cleaned_data.get('date_debut')
        date_fin = self.cleaned_data.get('date_fin')

        if date_fin and date_debut and date_fin < date_debut:
            raise forms.ValidationError("La date de fin ne peut pas être antérieure à la date de début.")

        return date_fin

    def clean_date_naissance(self):
        date_naissance = self.cleaned_data.get('date_naissance')
        if date_naissance:
            # Calcul de l'âge minimum requis (18 ans)
            today = date.today()
            age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))

            if age < 18:
                raise ValidationError("La secrétaire doit avoir au moins 18 ans.")
        
        return date_naissance
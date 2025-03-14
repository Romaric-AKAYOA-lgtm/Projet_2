from django import  forms
from django.core.exceptions import ValidationError
from .models import Visiteur
import re

class VisiteurForm(forms.ModelForm):
    class Meta:
        model = Visiteur
        fields = ['nom', 'prenom', 'sexe', 'type_visiteur', 'contact', 'email']  # Ajout du champ email
        widgets = {
            'sexe': forms.Select(choices=[
                ('Masculin', 'Masculin'),
                ('Féminin', 'Féminin')
            ])
        }

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

    def clean_email(self):
        email = self.cleaned_data['email']

        # Vérification que l'email est au format valide
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Veuillez entrer une adresse e-mail valide.")
        
        return email

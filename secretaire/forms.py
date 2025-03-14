from django import forms
from .models import Secretaire
import re
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

# Formulaire pour la gestion des secrétaires
class SecretaireForm(forms.ModelForm):
    class Meta:
        model = Secretaire
        fields = ['username', 'last_name', 'first_name', 'email', 'num_tel', 'date_debut', 'date_fin']  # Ajout des champs nécessaires
    def clean_nom(self):
        nom = self.cleaned_data['last_name']
        
        # Vérification que le nom ne contient pas de chiffres ni de caractères spéciaux
        if any(char.isdigit() for char in nom) :
            raise ValidationError("Le nom ne doit contenir que des lettres, sans chiffres ni caractères spéciaux.")
        
        # Vérification que le nom n'est pas vide
        if not nom:
            raise ValidationError("Le nom est obligatoire.")
        
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data['first_name']
        
        # Vérification que le prénom ne contient pas de chiffres ni de caractères spéciaux
        if any(char.isdigit() for char in prenom):
            raise ValidationError("Le prénom ne doit contenir que des lettres, sans chiffres ni caractères spéciaux.")
        
        return prenom

    def clean_num_tel(self):
        num_tel = self.cleaned_data['num_tel']
        if num_tel:
            # Vérifier que le numéro de téléphone ne contient que des chiffres et éventuellement des caractères spéciaux
            if not re.match(r'^[0-9\s\+()\-]*$', num_tel):
                raise forms.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres, des espaces et les caractères +, (, ), -. ")
        return num_tel

    def clean_date_debut(self):
        date_debut = self.cleaned_data.get('date_debut')
        if date_debut:
            # Vous pouvez ajouter ici des validations supplémentaires pour la date de début
            return date_debut
        return date_debut

    def clean_date_fin(self):
        date_fin = self.cleaned_data.get('date_fin')
        date_debut = self.cleaned_data.get('date_debut')
        if date_fin and date_debut and date_fin < date_debut:
            raise forms.ValidationError("La date de fin ne peut pas être antérieure à la date de début.")
        return date_fin


class LoginForm(forms.Form):  # Remplace AuthenticationForm par forms.Form
    username = forms.CharField(
        label="Nom d'utilisateur", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
    )
    password = forms.CharField(
        label="Mot de passe", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

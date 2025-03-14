from django import forms
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm
from .models import Directeur, Secretaire, Visite, ProgrammeVisite, Visiteur

# Formulaire d'authentification de la secrétaire
class SecretaireLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Formulaire pour créer une visite
class VisiteForm(forms.ModelForm):
    class Meta:
        model = Visite
        fields = ['date', 'heure', 'objet', 'visiteur', 'directeur', 'statut']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'objet': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'visiteur': forms.Select(attrs={'class': 'form-select'}),
            'directeur': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        # Création de la visite
        visite = super().save(commit=False)

        if commit:
            visite.save()

            # Si la visite est confirmée, on crée automatiquement un ProgrammeVisite
            if visite.statut == 'confirmé':
                ProgrammeVisite.objects.create(visite=visite, statut='en attente')

        return visite

# Formulaire pour modifier le statut du programme de visite
class ProgrammeVisiteForm(forms.ModelForm):
    class Meta:
        model = ProgrammeVisite
        fields = ['statut']
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        visite = self.instance.visite

        # Vérification de l'heure actuelle pour mettre à jour le statut
        if visite.date < now().date() or (visite.date == now().date() and visite.heure < now().time()):
            self.instance.statut = 'validé'

        return cleaned_data



# Formulaire pour Visiteur
class VisiteurForm(forms.ModelForm):
    class Meta:
        model = Visiteur
        fields = '__all__'  # Vous pouvez spécifier des champs spécifiques si nécessaire

# Formulaire pour Directeur
class DirecteurForm(forms.ModelForm):
    class Meta:
        model = Directeur
        fields = '__all__'

# Formulaire pour Secretaire
class SecretaireForm(forms.ModelForm):
    class Meta:
        model = Secretaire
        fields = '__all__'

# Formulaire pour Visite
class VisiteForm(forms.ModelForm):
    class Meta:
        model = Visite
        fields = '__all__'

# Formulaire pour ProgrammeVisite
class ProgrammeVisiteForm(forms.ModelForm):
    class Meta:
        model = ProgrammeVisite
        fields = '__all__'

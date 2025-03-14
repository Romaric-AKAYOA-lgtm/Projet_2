from django import forms
from django.core.exceptions import ValidationError
from .models import Visite, Visiteur, Directeur  # Assurez-vous que ces modèles existent
from programme_visite.models import ProgrammeVisite
from secretaire.models import Secretaire
from datetime import timedelta, datetime

class VisiteForm(forms.ModelForm):
    class Meta:
        model = Visite
        fields = ['date_visite', 'heure_visite', 'objet', 'visiteur', 'directeur', 'statut']

    # Ajoutez un queryset pour les champs ForeignKey pour l'autocomplétion
    visiteur = forms.ModelChoiceField(queryset=Visiteur.objects.all(), required=True)
    directeur = forms.ModelChoiceField(queryset=Directeur.objects.all(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        date_visite = cleaned_data.get('date_visite')
        heure_visite = cleaned_data.get('heure_visite')
        visiteur = cleaned_data.get('visiteur')
        statut = cleaned_data.get('statut')

        # Vérifier que la date et l'heure sont renseignées
        if not date_visite:
            raise ValidationError("La date de la visite est obligatoire.")
        if not heure_visite:
            raise ValidationError("L'heure de la visite est obligatoire.")

        # Vérifie si le visiteur est renseigné
        if not visiteur:
            raise ValidationError("Le visiteur doit être spécifié.")

        # Vérification du statut
        if statut not in ['confirmé', 'annulé']:
            raise ValidationError("Le statut de la visite doit être 'confirmé' ou 'annulé'.")

        if date_visite and heure_visite and visiteur and statut != 'annulé':
            # Vérifie si une visite existe déjà à cette date et heure pour le visiteur
            if Visite.objects.filter(date_visite=date_visite, heure_visite=heure_visite, visiteur=visiteur).exists():
                raise ValidationError(f"Une visite est déjà prévue pour {visiteur.nom} {visiteur.prenom} à cette date et heure.")

        return cleaned_data

    def save(self, commit=True):
        # Valider d'abord la création de la visite
        visite = super().save(commit=False)

        # Sauvegarder la visite sans l'engager tout de suite (évite les doublons avant la validation complète)
        if commit:
            visite.save()

        # Instancier la classe Visite et enregistrer le ProgrammeVisite si la validation est réussie
        secretaire = Secretaire.objects.order_by('-date_debut').first()  # Assurez-vous que `date_debut` est un champ de votre modèle Secretaire

        # Vérifiez si un secrétaire a été trouvé
        if not secretaire:
            raise ValidationError("Aucun secrétaire disponible.")

        # Vérifie s'il existe déjà un programme de visite pour cette visite et ce secrétaire
        if ProgrammeVisite.objects.filter(visite=visite, secretaire=secretaire).exists():
            raise ValidationError(f"Un programme de visite existe déjà pour cette visite et ce secrétaire.")

        # Plage horaire pour les visites
        heure_debut = timedelta(hours=8)  # 8h
        heure_fin = timedelta(hours=14)   # 14h

        # Convertir l'heure de la visite en datetime pour comparer avec la plage horaire
        heure_visite = datetime.combine(visite.date_visite, visite.heure_visite)
        heure_debut_comparaison = datetime.combine(visite.date_visite, datetime.min.time()) + heure_debut
        heure_fin_comparaison = datetime.combine(visite.date_visite, datetime.min.time()) + heure_fin

        # Si l'heure de la visite dépasse la plage horaire, la déplacer au jour suivant
        if heure_visite < heure_debut_comparaison or heure_visite > heure_fin_comparaison:
            visite.date_visite = visite.date_visite + timedelta(days=1)  # Déplacer au jour suivant
            visite.heure_visite = datetime.min.time()  # Heure de début de la visite à 8h

        # Vérification des conflits d'horaires
        conflit = ProgrammeVisite.objects.filter(date_creation=visite.date_create,  # Utilisation de `date_create`
                                                 heure_debut__lt=heure_fin_comparaison, 
                                                 heure_fin__gt=heure_debut_comparaison).exists()
        if conflit:
            raise ValidationError("Il y a un conflit avec un programme de visite existant.")

        # Création du programme de visite si aucune erreur n'est levée
        programme_visite = ProgrammeVisite.objects.create(
            visite=visite,
            secretaire=secretaire,  # Utilisez le champ 'secretaire' ici
            statut='en attente',
            heure_debut=visite.heure_visite,  # Ajustez selon votre logique
            heure_fin=visite.heure_visite + timedelta(hours=1),  # Ajoute une durée à la visite (par exemple 1h)
        )

        return visite

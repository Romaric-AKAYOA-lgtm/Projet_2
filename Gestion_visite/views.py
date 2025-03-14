from django.shortcuts import render, redirect
from datetime import date, timedelta
from directeur.models import Directeur
from secretaire.models import Secretaire
from secretaire.views import get_username_from_session
from visiteur.models import Visiteur
from visite.models import Visite
from programme_visite.models import ProgrammeVisite
from Activation.models import Activation

def home_view(request):
    """Page d'accueil avec les listes des directeurs, secrétaires, visiteurs et visites"""
    
    # Vérification de la validité de la clé d'activation via activation_view
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    # Récupérer le nom d'utilisateur depuis la session
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Lundi de la semaine
    month_start = today.replace(day=1)  # Début du mois

    # Log de la transaction effectuée par l'utilisateur
    context = {
        "username": username,  # Passer le nom d'utilisateur dans le contexte
       "directeurs": Directeur.objects.all().order_by('-date_debut')[:10],
        "secretaires": Secretaire.objects.filter(date_debut__isnull=False).order_by('-date_debut')[:10],
        "visiteurs": Visiteur.objects.all().order_by('nom')[:10],
         "visites_en_cours": Visite.objects.filter(statut="en cours")[:10],
        "programmes_reportes": ProgrammeVisite.objects.filter(statut="reporté")[:10],
        "visites_du_jour": Visite.objects.filter(date_visite=today),
        "visites_de_la_semaine": Visite.objects.filter(date_visite__gte=week_start, date_visite__lte=today + timedelta(days=6)),
        "visites_du_mois": Visite.objects.filter(date_visite__gte=month_start, date_visite__lte=today),
    }

    return render(request, "home.html", context)

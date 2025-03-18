from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date  # Pour convertir la date correctement
from Activation.models import Activation
from secretaire.views import get_username_from_session
from visiteur.models import Visiteur
from directeur.models import Directeur
from .forms import VisiteForm
from .models import Visite

# Vue pour afficher la liste des visites
def visite_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    visites = Visite.objects.all()
    return render(request, 'visite/list.html', {'visites': visites,  "username": username,  # Passer le nom d'utilisateur dans le contexte
                                                })

# Vue pour créer une nouvelle visite
def visite_create(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    form = VisiteForm()
    visiteurs = Visiteur.objects.all().order_by('nom')
    directeurs = Directeur.objects.all().order_by('nom')

    if request.method == "POST":
        date_visite = request.POST.get("date_visite", "")
        heure_visite = request.POST.get("heure_visite", "")

        # Vérification et conversion
        date_visite = parse_date(date_visite) if date_visite else None
        heure_visite = str(heure_visite) if heure_visite else None

        form = VisiteForm(request.POST)
        if form.is_valid():
            visite = form.save(commit=False)
            visite.date_visite = date_visite
            visite.heure_visite = heure_visite
            visite.save()
            return redirect('visite:Visite')  # Redirection vers la liste des visites
        else:
            print(f"Erreur : {form.errors}")  # Debugging pour voir les erreurs

    return render(request, 'visite/create.html', {
        'username':username,
        'form': form,
        'visiteurs': visiteurs,
        'directeurs': directeurs
    })

# Vue pour afficher les détails d'une visite spécifique
def visite_detail(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    visite = get_object_or_404(Visite, id=id)
    return render(request, 'visite/detail.html', {'visite': visite, 'username':username})

# Vue pour modifier une visite
def modifier_visite(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    visite = get_object_or_404(Visite, id=id)
    visiteurs = Visiteur.objects.all()
    directeurs = Directeur.objects.all()

    if request.method == "POST":
        form = VisiteForm(request.POST, instance=visite)
        
        if form.is_valid():
            date_visite = form.cleaned_data.get("date_visite")
            heure_visite = form.cleaned_data.get("heure_visite")

            # Vérification des formats avant de sauvegarder
            date_visite = parse_date(date_visite) if isinstance(date_visite, str) else date_visite
            heure_visite = str(heure_visite) if isinstance(heure_visite, str) else heure_visite

            visite.date_visite = date_visite
            visite.heure_visite = heure_visite
            visite.save()
            return redirect('visite:Visite')  # Redirection vers la liste des visites

    else:
        form = VisiteForm(instance=visite)

    return render(request, 'visite/edit.html', {
        'username':username,
        'form': form,
        'visiteurs': visiteurs,
        'directeurs': directeurs,
        'visite': visite
    })

# Vue pour supprimer une visite
def supprimer_visite(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    visite = get_object_or_404(Visite, id=id)
    if request.method == "POST":
        visite.delete()
        return redirect('visite:Visite')  # Redirection vers la liste des visites
    return render(request, 'visite/delete.html', {'visite': visite, 'username':username})

from django.shortcuts import render
from .models import Visite
from visiteur.models import Visiteur
from directeur.models import Directeur
from datetime import datetime

def visite_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (date, visiteur, directeur, statut)
    
    # Récupérer les dates de début et de fin si présentes
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')

    # Initialisation de la queryset avec toutes les visites
    visites = Visite.objects.all()

    # Filtrer selon les critères de recherche
    if critere and query:
        if critere == 'date_visite':
            visites = visites.filter(date_visite__icontains=query)
        elif critere == 'visiteur':
            visites = visites.filter(visiteur__nom__icontains=query)
        elif critere == 'directeur':
            visites = visites.filter(directeur__nom__icontains=query)
        elif critere == 'statut':
            visites = visites.filter(statut__icontains=query)
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale
        visites = visites.filter(visiteur__nom__icontains=query) | visites.filter(directeur__nom__icontains=query)

    # Filtrer selon les dates si spécifiées
    if date_debut:
        try:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()  # Convertir en date
            visites = visites.filter(date_visite__gte=date_debut)
        except ValueError:
            pass  # Si la conversion échoue, on ignore le filtre
    if date_fin:
        try:
            date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()  # Convertir en date
            visites = visites.filter(date_visite__lte=date_fin)
        except ValueError:
            pass  # Si la conversion échoue, on ignore le filtre

    # Ajouter un filtre pour le statut
    statut = request.GET.get('statut', '')
    if statut:
        visites = visites.filter(statut=statut)

    # Si aucune condition n'est remplie, on retourne un message disant qu'il n'y a pas de résultats
    if not visites:
        visites = None  # Pas de visites trouvées

    return render(request, 'visite/search.html', {
        'username':username,
        'visites': visites,
        'query': query,
        'criteres': critere,
        'statut': statut,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })

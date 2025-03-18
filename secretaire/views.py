from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.timezone import now
from .models import Secretaire
from .forms import SecretaireForm, LoginForm
from Activation.models import Activation
from django.contrib.auth import get_user_model
def get_username_from_session(request):
    """Récupère le nom d'utilisateur depuis la session et redirige vers la page de connexion si aucun utilisateur n'est trouvé."""
    username = request.session.get('username', None)
    
    if not username:
        return None  # Aucun nom d'utilisateur trouvé dans la session
    return username
# Vues pour la gestion des secrétaires

def secretaire_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Liste des secrétaires, filtrée par date_debut non nulle et triée par date_debut
    secretaires = Secretaire.objects.filter(date_debut__isnull=False).order_by('-date_debut')
    return render(request, 'secretaire/list.html', {      "username": username,  # Passer le nom d'utilisateur dans le contexte
      'secretaires': secretaires, "username": username})

def secretaire_create(request):
    username = get_username_from_session(request)
    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    if request.method == "POST":
        form = SecretaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('secretaire:Secretaire')  # Redirection après création
    else:
        form = SecretaireForm()
    return render(request, 'secretaire/form.html', {'form': form , 'username':username})

# views.py


def secretaire_detail(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer l'objet Secretaire en fonction de l'ID
    secretaire = get_object_or_404(Secretaire, id=id)
    return render(request, 'secretaire/detail.html', {'secretaire': secretaire , 'username':username})

def modifier_secretaire(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Modification du secrétaire
    secretaire = get_object_or_404(Secretaire, id=id)
    if request.method == "POST":
        form = SecretaireForm(request.POST, instance=secretaire)
        if form.is_valid():
            form.save()
            return redirect('secretaire:Secretaire')  # Redirection après création
    else:
        form = SecretaireForm(instance=secretaire)
    return render(request, 'secretaire/form.html', {'form': form, 'username':username})

def supprimer_secretaire(request, id):
    # Suppression du secrétaire
    secretaire = get_object_or_404(Secretaire, id=id)
    secretaire.delete()
    return redirect('secretaire:Secretaire')  # Redirection après création


from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Secretaire
from .forms import LoginForm
from Activation.models import Activation

def secretaire_detail2(request, username, password):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    """
    Vérifie si un secrétaire avec username et password existe,
    puis affiche ses détails.
    """
    secretaire = Secretaire.objects.filter(username=username).first()
    
    if not secretaire or not secretaire.check_password(password):
        return render(request, "secretaire/login.html", {"error": "Nom d'utilisateur ou mot de passe incorrect."})

    if secretaire.date_fin and secretaire.date_fin < now().date():
        return render(request, "secretaire/login.html", {"error": "Votre accès est expiré."})

    return render(request, "secretaire/detail.html", {"secretaire": secretaire, 'username':username})
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.models import User  # Import du modèle User de Django
from .models import Secretaire
from .forms import LoginForm
from Activation.models import Activation
def login_view(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""

    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    """
    Gère l'authentification du secrétaire et du superutilisateur en utilisant une session.
    """
    try:
        activation = Activation.objects.latest("activated_on")
        if not activation.is_valid():
            return redirect("Activation:activation_page")
    except Activation.DoesNotExist:
        return redirect("Activation:activation_page")

    error_message = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Vérifier d'abord si l'utilisateur est un superuser
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password) and user.is_superuser:
                request.session['superuser_id'] = user.id  # Stocker l'ID du superutilisateur
                return redirect("admin:index")  # Rediriger vers l'interface d'administration

            # Vérifier si le secrétaire existe avec ce username
            secretaire = Secretaire.objects.filter(username=username).first()

            if not secretaire:
                error_message = "Nom d'utilisateur incorrect."
            elif not secretaire.password:
                error_message = "Mot de passe incorrect."
            elif secretaire.date_fin and secretaire.date_fin < now().date():
                error_message = "Votre accès est expiré."
            else:
                  # Si toutes les vérifications sont réussies, on enregistre l'utilisateur dans la session
                request.session['secretaire_id'] = secretaire.id  # Stocker l'ID dans la session
                # Enregistrer également le username pour l'utiliser sur la page d'accueil
                request.session['username'] = username  # Ajouter le username à la session
                print("Redirection vers la page d'accueil.")
                return redirect("home")  # Rediriger vers l'accueil
        else:
            print("Le formulaire n'est pas valide.")
    else:
       form = LoginForm()

    return render(request, "secretaire/login.html", {"form": form, "error": error_message})

def logout_view(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    """
    Déconnecte le secrétaire ou le superuser en supprimant la session.
    """
    request.session.flush()  # Supprime toutes les données de session
    return redirect("secretairem:login")  # Rediriger vers la page de connexion

def secretaire_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (username, first_name, email, etc.)
    
    # Initialisation de la queryset avec tous les secrétaires
    secretaires = Secretaire.objects.all()

    # Si un critère et un terme de recherche sont saisis, filtrer en fonction du critère
    if critere and query:
        if critere == 'username':
            secretaires = secretaires.filter(username__icontains=query)
        elif critere == 'first_name':
            secretaires = secretaires.filter(first_name__icontains=query)
        elif critere == 'last_name':
            secretaires = secretaires.filter(last_name__icontains=query)
        elif critere == 'email':
            secretaires = secretaires.filter(email__icontains=query)
        elif critere == 'num_tel':
            secretaires = secretaires.filter(num_tel__icontains=query)
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale
        secretaires = secretaires.filter(username__icontains=query) | secretaires.filter(first_name__icontains=query) | secretaires.filter(last_name__icontains=query)

    # Ajouter d'autres filtres si nécessaire, par exemple date_debut, date_fin, etc.
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    # Appliquer les filtres supplémentaires uniquement si les champs sont remplis
    if date_debut:
        secretaires = secretaires.filter(date_debut__gte=date_debut)
    if date_fin:
        secretaires = secretaires.filter(date_fin__lte=date_fin)

    # Si aucune condition n'est remplie, on retourne un message disant qu'il n'y a pas de résultats
    if not secretaires:
        secretaires = None  # Pas de secrétaires trouvés

    return render(request, 'secretaire/search.html', {
        'secretaires': secretaires,
        'username':username,
        'query': query,
        'criteres': critere,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })

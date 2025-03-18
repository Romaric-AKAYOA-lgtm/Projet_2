from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from Activation.models import Activation
from secretaire.views import get_username_from_session
from .models import Directeur
from .forms import DirecteurForm

def directeur_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    directeurs = Directeur.objects.all().order_by('-date_debut')
    return render(request, 'directeur/directeur_list.html', {'directeurs': directeurs,
                                                                   "username": username,  # Passer le nom d'utilisateur dans le contexte
     })

def directeur_create(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    if request.method == "POST":
        form = DirecteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directeur:Directeur')
    else:
        form = DirecteurForm()
    return render(request, 'directeur/directeur_form.html', {'form': form, 'username':username})

def directeur_detail(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    directeur = get_object_or_404(Directeur, id=id)
    return render(request, 'directeur/directeur_detail.html', {'directeur': directeur , 'username':username})

def modifier_directeur(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    directeur = get_object_or_404(Directeur, id=id)

    if request.method == "POST":
        form = DirecteurForm(request.POST, instance=directeur)
        if form.is_valid():
            form.save()
            return redirect('directeur:Directeur')  # Redirigez vers la liste des directeurs après la sauvegarde
    else:
        form = DirecteurForm(instance=directeur)  # Remplir le formulaire avec les données existantes

    return render(request, 'directeur/directeur_form_edit.html', {'form': form, 'directeur': directeur, 'username':username})

def supprimer_directeur(request, id):
    directeur = get_object_or_404(Directeur, id=id)
    directeur.delete()
    return redirect('directeur:Directeur')
from django.shortcuts import render
from django.db.models import Q
from .models import Directeur  # Assurez-vous que vous importez correctement le modèle Directeur

def directeur_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (nom, prenom, email, etc.)

    # Initialisation de la queryset avec tous les directeurs
    directeurs = Directeur.objects.all()

    # Si un critère et un terme de recherche sont saisis, filtrer en fonction du critère
    if critere and query:
        if critere == 'nom':
            directeurs = directeurs.filter(nom__icontains=query)
        elif critere == 'prenom':
            directeurs = directeurs.filter(prenom__icontains=query)
        elif critere == 'email':
            directeurs = directeurs.filter(email__icontains=query)
        elif critere == 'num_tel':
            directeurs = directeurs.filter(num_tel__icontains=query)
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale
        directeurs = directeurs.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query) |
            Q(num_tel__icontains=query)
        )

    # Ajouter d'autres filtres si nécessaire, par exemple date_debut, date_fin, etc.
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')

    # Appliquer les filtres supplémentaires uniquement si les champs sont remplis
    if date_debut:
        directeurs = directeurs.filter(date_debut__gte=date_debut)
    if date_fin:
        directeurs = directeurs.filter(date_fin__lte=date_fin)

    # Si aucun résultat n'est trouvé, retourner un message ou laisser la queryset vide
    if not directeurs:
        directeurs = None  # Pas de directeurs trouvés

    # Retourner la réponse au template avec les données filtrées
    return render(request, 'directeur/search.html', {
        'username':username, 
        'directeurs': directeurs,
        'query': query,
        'criteres': critere,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })

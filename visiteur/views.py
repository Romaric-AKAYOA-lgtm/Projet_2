from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

from Activation.models import Activation
from secretaire.views import get_username_from_session
from .models import Visiteur
from .forms import VisiteurForm

from django.shortcuts import render
from .models import Visiteur  # Assurez-vous que le modèle Visiteur est importé

def visiteur_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer tous les visiteurs et les trier par nom
    visiteurs = Visiteur.objects.all().order_by('nom')
    
    # Rendre le template avec la liste des visiteurs
    return render(request, 'Visiteur/visiteur_list.html', {'visiteurs': visiteurs ,  "username": username,  # Passer le nom d'utilisateur dans le contexte 
                                                           })

def visiteur_create(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    if request.method == "POST":
        form = VisiteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Visiteur:Visiteur')
    else:
        form = VisiteurForm()
    return render(request, 'Visiteur/visiteur_create.html', { 'username':username,'form': form})

"""
def visiteur_detail(request, id):
    visiteur = get_object_or_404(Visiteur, id=id)
    return render(request, 'Visiteur/visiteur_detail.html', {'visiteur': visiteur})
"""
def modifier_visiteur(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer le visiteur par son ID
    visiteur = get_object_or_404(Visiteur, id=id)
    
    # Si la méthode est POST, on enregistre les modifications
    if request.method == "POST":
        form = VisiteurForm(request.POST, instance=visiteur)
        if form.is_valid():
            form.save()
            return redirect('Visiteur:Visiteur')  # Rediriger vers la liste des visiteurs après modification
    else:
        form = VisiteurForm(instance=visiteur)  # Charger l'instance du visiteur dans le formulaire
    
    # Passer à la fois le formulaire et le visiteur dans le contexte
    return render(request, 'Visiteur/modifier_visiteur.html', { 'username':username,'form': form, 'visiteur': visiteur})

def supprimer_visiteur(request, id):
    visiteur = get_object_or_404(Visiteur, id=id)
    visiteur.delete()
    return redirect('Visiteur:Visiteur')

def visiteur_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (nom, prénom, email, etc.)
    
    # Initialisation de la queryset avec tous les visiteurs
    visiteurs = Visiteur.objects.all()

    # Si un critère et un terme de recherche sont saisis, filtrer en fonction du critère
    if critere and query:
        if critere == 'nom':
            visiteurs = visiteurs.filter(nom__icontains=query)
        elif critere == 'prenom':
            visiteurs = visiteurs.filter(prenom__icontains=query)
        elif critere == 'email':
            visiteurs = visiteurs.filter(email__icontains=query)
        elif critere == 'contact':
            visiteurs = visiteurs.filter(contact__icontains=query)
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale par nom ou prénom
        visiteurs = visiteurs.filter(nom__icontains=query) | visiteurs.filter(prenom__icontains=query)

    # Ajouter d'autres filtres si nécessaire, par exemple sexe, type_visiteur, etc.
    sexe = request.GET.get('sexe', '')
    type_visiteur = request.GET.get('type_visiteur', '')
    contact = request.GET.get('contact', '')
    email = request.GET.get('email', '')
    
    # Appliquer les filtres supplémentaires uniquement si les champs sont remplis
    if sexe:
        visiteurs = visiteurs.filter(sexe=sexe)
    if type_visiteur:
        visiteurs = visiteurs.filter(type_visiteur__icontains=type_visiteur)
    if contact:
        visiteurs = visiteurs.filter(contact__icontains=contact)
    if email:
        visiteurs = visiteurs.filter(email__icontains=email)

    # Si aucune condition n'est remplie, on retourne un message disant qu'il n'y a pas de résultats
    if not visiteurs:
        visiteurs = None  # Pas de visiteurs trouvés

    return render(request, 'visiteur/search.html', {
        'username':username,
        'visiteurs': visiteurs,
        'query': query,
        'criteres': critere,
        'sexe': sexe,
        'type_visiteur': type_visiteur,
        'contact': contact,
        'email': email
    })

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
    if request.method == "POST":
        form = VisiteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Visiteur:Visiteur')
    else:
        form = VisiteurForm()
    return render(request, 'Visiteur/visiteur_create.html', {'form': form})

"""
def visiteur_detail(request, id):
    visiteur = get_object_or_404(Visiteur, id=id)
    return render(request, 'Visiteur/visiteur_detail.html', {'visiteur': visiteur})
"""
def modifier_visiteur(request, id):
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
    return render(request, 'Visiteur/modifier_visiteur.html', {'form': form, 'visiteur': visiteur})

def supprimer_visiteur(request, id):
    visiteur = get_object_or_404(Visiteur, id=id)
    visiteur.delete()
    return redirect('Visiteur:Visiteur')

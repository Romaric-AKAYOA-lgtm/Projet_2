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
    if request.method == "POST":
        form = DirecteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directeur:Directeur')
    else:
        form = DirecteurForm()
    return render(request, 'directeur/directeur_form.html', {'form': form})

def directeur_detail(request, id):
    directeur = get_object_or_404(Directeur, id=id)
    return render(request, 'directeur/directeur_detail.html', {'directeur': directeur})

def modifier_directeur(request, id):
    directeur = get_object_or_404(Directeur, id=id)

    if request.method == "POST":
        form = DirecteurForm(request.POST, instance=directeur)
        if form.is_valid():
            form.save()
            return redirect('directeur:Directeur')  # Redirigez vers la liste des directeurs après la sauvegarde
    else:
        form = DirecteurForm(instance=directeur)  # Remplir le formulaire avec les données existantes

    return render(request, 'directeur/directeur_form_edit.html', {'form': form, 'directeur': directeur})

def supprimer_directeur(request, id):
    directeur = get_object_or_404(Directeur, id=id)
    directeur.delete()
    return redirect('directeur:Directeur')

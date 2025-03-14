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
    form = VisiteForm()
    visiteurs = Visiteur.objects.all()
    directeurs = Directeur.objects.all()

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
        'form': form,
        'visiteurs': visiteurs,
        'directeurs': directeurs
    })

# Vue pour afficher les détails d'une visite spécifique
def visite_detail(request, id):
    visite = get_object_or_404(Visite, id=id)
    return render(request, 'visite/detail.html', {'visite': visite})

# Vue pour modifier une visite
def modifier_visite(request, id):
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
        'form': form,
        'visiteurs': visiteurs,
        'directeurs': directeurs,
        'visite': visite
    })

# Vue pour supprimer une visite
def supprimer_visite(request, id):
    visite = get_object_or_404(Visite, id=id)
    if request.method == "POST":
        visite.delete()
        return redirect('visite:Visite')  # Redirection vers la liste des visites
    return render(request, 'visite/delete.html', {'visite': visite})

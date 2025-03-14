from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Visiteur, Directeur, Secretaire, Visite, ProgrammeVisite
from .forms import DirecteurForm, SecretaireForm, VisiteForm, ProgrammeVisiteForm, VisiteurForm

# -------------------------- Visiteur -------------------------- #

@login_required
def liste_Visiteur(request):
    visiteurs = Visiteur.objects.all()
    return render(request, 'visiteur/liste_Visiteurs.html', {'visiteurs': visiteurs})

@login_required
def ajouter_Visiteur(request):
    if request.method == 'POST':
        form = VisiteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_Visiteurs')
    else:
        form = VisiteurForm()
    return render(request, 'visiteur/ajouter_Visiteur.html', {'form': form})

@login_required
def modifier_Visiteur(request, Visiteur_id):
    visiteur = get_object_or_404(Visiteur, id=Visiteur_id)
    if request.method == 'POST':
        form = VisiteurForm(request.POST, instance=visiteur)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_Visiteurs')
    else:
        form = VisiteurForm(instance=visiteur)
    return render(request, 'visiteur/modifier_Visiteur.html', {'form': form})

@login_required
def supprimer_Visiteur(request, Visiteur_id):
    visiteur = get_object_or_404(Visiteur, id=Visiteur_id)
    visiteur.delete()
    return redirect('visiteur:liste_Visiteurs')

# -------------------------- Directeur -------------------------- #

@login_required
def liste_Directeur(request):
    directeurs = Directeur.objects.all()
    return render(request, 'directeur/liste_Directeurs.html', {'directeurs': directeurs})

@login_required
def ajouter_Directeur(request):
    if request.method == 'POST':
        form = DirecteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_Directeurs')
    else:
        form = DirecteurForm()
    return render(request, 'directeur/ajouter_Directeur.html', {'form': form})

@login_required
def modifier_Directeur(request, Directeur_id):
    directeur = get_object_or_404(Directeur, id=Directeur_id)
    if request.method == 'POST':
        form = DirecteurForm(request.POST, instance=directeur)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_Directeurs')
    else:
        form = DirecteurForm(instance=directeur)
    return render(request, 'directeur/modifier_Directeur.html', {'form': form})

@login_required
def supprimer_Directeur(request, Directeur_id):
    directeur = get_object_or_404(Directeur, id=Directeur_id)
    directeur.delete()
    return redirect('visiteur:liste_Directeurs')

# -------------------------- Secretaire -------------------------- #

@login_required
def liste_Secretaire(request):
    secretaires = Secretaire.objects.all()
    return render(request, 'secretaire/liste_Secretaires.html', {'secretaires': secretaires})

@login_required
def ajouter_Secretaire(request):
    if request.method == 'POST':
        form = SecretaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_Secretaires')
    else:
        form = SecretaireForm()
    return render(request, 'secretaire/ajouter_Secretaire.html', {'form': form})

@login_required
def modifier_Secretaire(request, Secretaire_id):
    secretaire = get_object_or_404(Secretaire, id=Secretaire_id)
    if request.method == 'POST':
        form = SecretaireForm(request.POST, instance=secretaire)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_Secretaires')
    else:
        form = SecretaireForm(instance=secretaire)
    return render(request, 'secretaire/modifier_Secretaire.html', {'form': form})

@login_required
def supprimer_Secretaire(request, Secretaire_id):
    secretaire = get_object_or_404(Secretaire, id=Secretaire_id)
    secretaire.delete()
    return redirect('visiteur:liste_Secretaires')

# -------------------------- Visite -------------------------- #

@login_required
def liste_Visite(request):
    visites = Visite.objects.all()
    return render(request, 'visite/liste_Visites.html', {'visites': visites})

@login_required
def ajouter_Visite(request):
    if request.method == 'POST':
        form = VisiteForm(request.POST)
        if form.is_valid():
            visite = form.save()
            return redirect('visiteur:liste_Visites')
    else:
        form = VisiteForm()
    return render(request, 'visite/ajouter_Visite.html', {'form': form})

@login_required
def modifier_Visite(request, Visite_id):
    visite = get_object_or_404(Visite, id=Visite_id)
    if request.method == 'POST':
        form = VisiteForm(request.POST, instance=visite)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_Visites')
    else:
        form = VisiteForm(instance=visite)
    return render(request, 'visite/modifier_Visite.html', {'form': form})

@login_required
def supprimer_Visite(request, Visite_id):
    visite = get_object_or_404(Visite, id=Visite_id)
    visite.delete()
    return redirect('visiteur:liste_Visites')

# -------------------------- ProgrammeVisite -------------------------- #

@login_required
def liste_ProgrammeVisite(request):
    programmes = ProgrammeVisite.objects.all()

    # Mise à jour automatique du statut des programmes
    for programme in programmes:
        visite = programme.visite
        if visite.date < now().date() or (visite.date == now().date() and visite.heure < now().time()):
            programme.statut = 'validé'
            programme.save()

    return render(request, 'programme_visite/liste_ProgrammeVisites.html', {'programmes': programmes})

@login_required
def ajouter_ProgrammeVisite(request):
    if request.method == 'POST':
        form = ProgrammeVisiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_ProgrammeVisites')
    else:
        form = ProgrammeVisiteForm()
    return render(request, 'programme_visite/ajouter_ProgrammeVisite.html', {'form': form})

@login_required
def modifier_ProgrammeVisite(request, ProgrammeVisite_id):
    programme = get_object_or_404(ProgrammeVisite, id=ProgrammeVisite_id)
    if request.method == 'POST':
        form = ProgrammeVisiteForm(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            return redirect('visiteur:liste_ProgrammeVisites')
    else:
        form = ProgrammeVisiteForm(instance=programme)
    return render(request, 'programme_visite/modifier_ProgrammeVisite.html', {'form': form})

@login_required
def supprimer_ProgrammeVisite(request, ProgrammeVisite_id):
    programme = get_object_or_404(ProgrammeVisite, id=ProgrammeVisite_id)
    programme.delete()
    return redirect('visiteur:liste_ProgrammeVisites')

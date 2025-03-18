from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from Activation.models import Activation
from secretaire.views import get_username_from_session
from .models import ProgrammeVisite
from .forms import ProgrammeVisiteForm
from visite.models import Visite
from secretaire.models import Secretaire
from datetime import date
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from django.http import HttpResponse
from reportlab.lib import colors
import io
from io import BytesIO
from django.db.models import Q


def programme_visite_list(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Filtrer les programmes de visite pour afficher seulement ceux qui ont un statut confirmé
    programmes = ProgrammeVisite.objects.filter(visite__statut='confirmé').order_by('-date_creation')
    return render(request, 'programme_visite/list.html', {'programmes': programmes , 'username':username # Passer le nom d'utilisateur dans le contexte
 })


def programme_visite_create(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Obtenir la date système (aujourd'hui)
    today = now().date()
    
    # Filtrer les visites confirmées ayant une date de visite <= aujourd'hui 
    # et qui ne sont pas encore enregistrées dans ProgrammeVisite
    visites = Visite.objects.filter(
        statut='confirmé',
        date_visite__lte=today  # Sélectionner les visites dont la date est <= aujourd'hui
    ).exclude(id__in=ProgrammeVisite.objects.values_list('visite_id', flat=True)).order_by('-date_visite')

    # Récupérer les secrétaires avec une date de début non nulle, triées par date de début décroissante
    secretaires = Secretaire.objects.filter(date_debut__isnull=False).order_by('-date_debut')

    form = ProgrammeVisiteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("programme_visite:ProgrammeVisite")

    return render(request, "programme_visite/form.html", {
        "form": form,
        "visites": visites,
        "secretaires": secretaires,  # Passez les secrétaires au contexte
    })
    
def programme_visite_detail(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    programme = get_object_or_404(ProgrammeVisite, id=id)
    return render(request, 'programme_visite/detail.html', {'programme': programme, 'username':username})

def modifier_programme_visite(request, id):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    programme = get_object_or_404(ProgrammeVisite, id=id)
    visites = Visite.objects.filter(statut='confirmé').order_by('-date_visite')  # Récupère toutes les visites confirmées
    #secretaires = Secretaire.objects.all().order_by('-date_debut').first()  # Récupère la secrétaire la plus récente
    secretaires = Secretaire.objects.filter(date_debut__isnull=False).order_by('-date_debut')
    
    if request.method == "POST":
        form = ProgrammeVisiteForm(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            return redirect('programme_visite:ProgrammeVisite')
    else:
        form = ProgrammeVisiteForm(instance=programme)

    return render(request, 'programme_visite/ajouter_programme_visite.html', {
        'username':username,
        'form': form,
        'programme_visite': programme,
        'visites': visites,
        'secretaires': secretaires,  # Ajout de la secrétaire récente
    })

def supprimer_programme_visite(request, id):
    programme = get_object_or_404(ProgrammeVisite, id=id)
    programme.delete()
    return redirect('programme_visite:ProgrammeVisite')

def programme_visite_search(request):
    username = get_username_from_session(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer les paramètres de recherche
    query = request.GET.get('query', '')  # Recherche globale
    critere = request.GET.get('criteres', '')  # Critère de recherche sélectionné (visite, secretaire, statut, etc.)
    
    # Initialisation de la queryset avec tous les programmes de visite
    programmes = ProgrammeVisite.objects.all()

    # Si un critère et un terme de recherche sont saisis, filtrer en fonction du critère
    if critere and query:
        if critere == 'visite':
            programmes = programmes.filter(visite__visiteur__nom__icontains=query)  # Filtrer par nom du visiteur
        elif critere == 'secretaire':
            programmes = programmes.filter(secretaire__last_name__icontains=query)  # Assurez-vous que 'last_name' est un champ de Secretaire
        elif critere == 'statut':
            programmes = programmes.filter(statut__icontains=query)
        elif critere == 'date_creation':
            programmes = programmes.filter(date_creation__icontains=query)  # Recherche par date
    elif query:
        # Si un terme de recherche est saisi sans critère, effectuer une recherche globale sur plusieurs champs
        programmes = programmes.filter(
            Q(visite__visiteur__nom__icontains=query) |  # Recherche sur le nom du visiteur
            Q(secretaire__last_name__icontains=query) |
            Q(statut__icontains=query) |
            Q(date_creation__icontains=query)
        )

    # Ajouter des filtres supplémentaires pour les dates (date_debut et date_fin)
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    # Appliquer les filtres supplémentaires si les champs sont remplis
    if date_debut:
        programmes = programmes.filter(date_creation__gte=date_debut)  # Filtrer après la date_debut
    if date_fin:
        programmes = programmes.filter(date_creation__lte=date_fin)  # Filtrer avant la date_fin

    # Si aucun résultat n'est trouvé, on peut afficher un message ou laisser la queryset vide
    if not programmes:
        programmes = None  # Pas de programmes trouvés

    # Retourner la réponse au template avec les données filtrées
    return render(request, 'programme_visite/search.html', {
        'username':username,
        'programmes': programmes,
        'query': query,
        'criteres': critere,
        'date_debut': date_debut,
        'date_fin': date_fin,
    })

import io
from datetime import date, timedelta
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import ProgrammeVisite
from secretaire.models import Secretaire

def obtenir_secretaire_recente():
    """Récupère la secrétaire la plus récente."""
    return Secretaire.objects.order_by('-date_debut').first()

def imprimer_tous_les_programmes(request):
    """Génère un PDF des programmes du jour, de la semaine et du mois."""
    # Obtenir la date d'aujourd'hui (date système)
    date_aujourdhui = date.today()
    date_debut_semaine = date_aujourdhui - timedelta(days=6)
    date_debut_mois = date_aujourdhui.replace(day=1)
    # Remplacer le jour pour obtenir le 1er jour du mois
    programmes_jour = ProgrammeVisite.objects.filter(date_creation=date_aujourdhui)
    programmes_semaine = ProgrammeVisite.objects.filter(date_creation__range=[date_debut_semaine, date_aujourdhui])
    programmes_mois = ProgrammeVisite.objects.filter(date_creation__range=[date_debut_mois, date_aujourdhui])

    secretaire_recente = obtenir_secretaire_recente()

    return generer_pdf(request, programmes_jour, programmes_semaine, programmes_mois, "PROGRAMMES DE VISITE", secretaire_recente)

from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from io import BytesIO
from datetime import date
from Activation.models import Activation
def generer_pdf(request, programmes_jour, programmes_semaine, programmes_mois, titre, secretaire_recente):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    """Crée un PDF avec mise en page et styles améliorés."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    # Style des en-têtes
    header_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ])

    # Style spécifique pour la devise
    devise_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.green),  # Couleur verte pour la devise
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
    ])

    # En-têtes officiels
    entetes = [
        ["Institut National De Recherche et d'Actions Pédagogiques", "République du Congo"],
        ["(INRAP)", "Unité Travail Progrès"]
    ]

    # Première ligne (INRAP et République du Congo)
    for ligne in entetes[:1]:
        table = Table([ligne], colWidths=[375, 375])
        table.setStyle(header_style)
        elements.append(table)

    # Espacement avant la devise
    elements.append(Spacer(1, 20))

    # Deuxième ligne (Devise)
    for ligne in entetes[1:]:
        table = Table([ligne], colWidths=[375, 375])
        table.setStyle(devise_style)
        elements.append(table)

    # Espacement supplémentaire pour séparer les sections
    elements.append(Spacer(1, 40))

    # --- Titre principal ---
    elements.append(Table([[titre]], colWidths=[750], style=[
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))

    def ajouter_section(nom_section, programmes):
        """Ajoute une section avec un tableau contenant les programmes."""
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(nom_section, styles['Heading3']))

        if not programmes:
            elements.append(Paragraph("Aucun programme disponible.", styles['Normal']))
            return

        data = [["ID", "Visite", "Secrétaire", "Statut", "Heure Début", "Heure Fin"]]

        for programme in programmes:
            secretaire_complete = (f"{programme.secretaire.last_name} {programme.secretaire.first_name}"
                                   if programme.secretaire else "N/A")
            ligne = [
                programme.id,
                Paragraph(str(programme.visite), styles['Normal']),
                secretaire_complete,
                programme.statut,
                programme.heure_debut.strftime("%H:%M") if programme.heure_debut else "N/A",
                programme.heure_fin.strftime("%H:%M") if programme.heure_fin else "N/A",
            ]
            data.append(ligne)

        base_style = [
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]
        alternating_background = [
            ('BACKGROUND', (0, row), (-1, row), colors.lightblue if row % 2 == 0 else colors.white)
            for row in range(1, len(data))
        ]

        table = Table(data, colWidths=[50, 300, 150, 100, 80, 80])
        table.setStyle(TableStyle(base_style + alternating_background))
        elements.append(table)

    ajouter_section("Programmes du Jour", programmes_jour)
    ajouter_section("Programmes de la Semaine", programmes_semaine)
    ajouter_section("Programmes du Mois", programmes_mois)

    # --- Signature ---
    elements.append(Spacer(1, 30))
    if secretaire_recente:
        lieu_date = f"Brazzaville, Fait le : {date.today().strftime('%d/%m/%Y')}"
        signataire = f" {getattr(secretaire_recente, 'fonction', 'Secrétaire')}, {secretaire_recente.last_name} {secretaire_recente.first_name}"
        
        elements.append(Table([[lieu_date]], colWidths=[750], style=[
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))
        
        elements.append(Spacer(1, 60))  # Augmenter la marge pour la signature
        
        elements.append(Spacer(1, 20))
        
        elements.append(Table([[signataire]], colWidths=[750], style=[
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))
    
    # --- Génération du PDF ---
    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="programmes_visite.pdf"'
    return response

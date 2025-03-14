from django.urls import path
from . import views

app_name='visiteur'

urlpatterns = [
    # Gestion des Visiteurs
    path('Visiteur/', views.liste_Visiteur, name='liste_Visiteurs'),
    path('Visiteur/ajouter/', views.ajouter_Visiteur, name='ajouter_Visiteur'),
    path('Visiteur/modifier/<int:Visiteur_id>/', views.modifier_Visiteur, name='modifier_Visiteur'),
    path('Visiteur/supprimer/<int:Visiteur_id>/', views.supprimer_Visiteur, name='supprimer_Visiteur'),


     # Gestion des Directeurs
    path('Directeur/', views.liste_Directeur, name='liste_Directeurs'),
    path('Directeur/ajouter/', views.ajouter_Directeur, name='ajouter_Directeur'),
    path('Directeur/modifier/<int:Directeur_id>/', views.modifier_Directeur, name='modifier_Directeur'),
    path('Directeur/supprimer/<int:Directeur_id>/', views.supprimer_Directeur, name='supprimer_Directeur'),


   # Gestion des Secretaire
    path('Secretaire/', views.liste_Secretaire, name='liste_Secretaires'),
    path('Secretaire/ajouter/', views.ajouter_Secretaire, name='ajouter_Secretaire'),
    path('Secretaire/modifier/<int:Secretaire_id>/', views.modifier_Secretaire, name='modifier_Secretaire'),
    path('Secretaire/supprimer/<int:Secretaire_id>/', views.supprimer_Secretaire, name='supprimer_Secretaire'),


   # Gestion des Visite
    path('Visite/', views.liste_Visite, name='liste_Visites'),
    path('Visite/ajouter/', views.ajouter_Visite, name='ajouter_Visite'),
    path('Visite/modifier/<int:Visite_id>/', views.modifier_Visite, name='modifier_Visite'),
    path('Visite/supprimer/<int:Visite_id>/', views.supprimer_Visite, name='supprimer_Visite'),


   # Gestion des Visite
    path('ProgrammeVisite', views.liste_ProgrammeVisite, name='liste_ProgrammeVisites'),
    path('ProgrammeVisite/', views.ajouter_ProgrammeVisite, name='ajouter_ProgrammeVisite'),
    path('ProgrammeVisite/modifier/<int:ProgrammeVisite_id>/', views.modifier_ProgrammeVisite, name='modifier_ProgrammeVisite'),
    path('ProgrammeVisite/supprimer/<int:ProgrammeVisite_id>/', views.supprimer_ProgrammeVisite, name='supprimer_ProgrammeVisite'),

]

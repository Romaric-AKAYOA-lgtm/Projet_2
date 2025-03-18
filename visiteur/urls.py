from django.urls import path
from . import views

app_name = 'Visiteur'

urlpatterns = [
    path('', views.visiteur_list, name='Visiteur'),
    path('creer/', views.visiteur_create, name='creer'),
    path('<int:id>/modifier/', views.modifier_visiteur, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_visiteur, name='supprimer'),
    path('recherche/', views.visiteur_search, name='recherche'),  # Ajout de la route de recherche
]

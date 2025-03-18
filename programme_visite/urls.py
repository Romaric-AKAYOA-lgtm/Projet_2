from django.urls import path
from . import views

app_name = 'programme_visite'

urlpatterns = [
    path('', views.programme_visite_list, name='ProgrammeVisite'),
    path('creer/', views.programme_visite_create, name='creer'),
    path('<int:id>/', views.programme_visite_detail, name='information'),
    path('<int:id>/modifier/', views.modifier_programme_visite, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_programme_visite, name='supprimer'),
    path('imprimer/', views.imprimer_tous_les_programmes, name='imprimer'),  # Ajout de l'URL d'impression
     path('recherche/', views.programme_visite_search, name='recherche'),  # Ajout de la route de recherche
]

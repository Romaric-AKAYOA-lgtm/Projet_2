from django.urls import path
from . import views

app_name = 'directeur'

urlpatterns = [
    path('', views.directeur_list, name='Directeur'),
    path('creer/', views.directeur_create, name='creer'),
    path('<int:id>/', views.directeur_detail, name='information'),
   path('<int:id>/modifier/', views.modifier_directeur, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_directeur, name='supprimer'),
]

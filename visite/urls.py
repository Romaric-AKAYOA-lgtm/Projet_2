from django.urls import path
from . import views

app_name = 'visite'

urlpatterns = [
    path('', views.visite_list, name='Visite'),
    path('creer/', views.visite_create, name='creer'),
    path('<int:id>/', views.visite_detail, name='infomation'),
    path('<int:id>/modifier/', views.modifier_visite, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_visite, name='supprimer'),
]

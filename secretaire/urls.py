# urls.py
from django.urls import path
from . import views

app_name = 'secretaire'

urlpatterns = [
    path('Secretaire/', views.secretaire_list, name='Secretaire'),
    path('creer/', views.secretaire_create, name='creer'),
    path('<int:id>/', views.secretaire_detail, name='information'),    path('<int:id>/modifier/', views.modifier_secretaire, name='modifier'),
    path('<int:id>/supprimer/', views.supprimer_secretaire, name='supprimer'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

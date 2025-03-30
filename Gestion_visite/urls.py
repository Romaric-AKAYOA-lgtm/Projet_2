from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from secretaire.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path("home", views.home_view, name='home'), 
    path('visiteur/', include('visiteur.urls')),  # Inclure les URLs de l'application visiteur
    path('visite/', include('visite.urls')),  # Inclure les URLs de l'application visite
    path('secretaire/', include('secretaire.urls')),  # Inclure les URLs de l'application secretaire
    path('directeur/', include('directeur.urls')),  # Inclure les URLs de l'application directeur
    # Ajoutez d'autres applications ici, si nécessaire
    path('', login_view, name='login'),  # Page de connexion
    path('programme_visite/', include('programme_visite.urls')),  # Inclure les URLs de l'application programme_visite
    path('activation/', include('Activation.urls')),
    path('Notifications/', include('Notifications.urls')),
    path('administration/', include('administration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

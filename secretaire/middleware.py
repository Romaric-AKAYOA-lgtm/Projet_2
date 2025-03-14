from django.shortcuts import redirect
from django.utils.timezone import now
from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si l'utilisateur est authentifié
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                # Utiliser timezone.now() pour obtenir l'heure actuelle
                now_timestamp = now().timestamp()
                # Si plus de 5 minutes d'inactivité
                if now_timestamp - last_activity > 300:
                    logout(request)  # Déconnecter l'utilisateur
                    return redirect('login')  # Rediriger vers la page de connexion (assurez-vous que 'login' est bien défini dans vos urls)
                
            # Mettre à jour la session avec l'heure de la dernière activité
            request.session['last_activity'] = now().timestamp()

        response = self.get_response(request)
        return response

import socket
import logging
from django.shortcuts import redirect
from django.utils.timezone import now
from django.contrib.auth import logout

# Configuration du logger
logger = logging.getLogger('django')

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Récupération de l'adresse IP et du nom d'hôte
        client_ip = self.get_client_ip(request)
        client_hostname = self.get_hostname(client_ip)

        # Log de l'accès utilisateur
        if request.user.is_authenticated:
            logger.info(
                f"Utilisateur {request.user.username} connecté depuis {client_ip} ({client_hostname})"
            )

            last_activity = request.session.get('last_activity')
            if last_activity:
                now_timestamp = now().timestamp()
                if now_timestamp - last_activity > 300:  # 5 minutes d'inactivité
                    logger.info(
                        f"Déconnexion automatique de {request.user.username} depuis {client_ip} ({client_hostname}) pour inactivité."
                    )
                    logout(request)
                    return redirect('login')  # Redirige vers la page de connexion

            # Mise à jour du timestamp de la dernière activité
            request.session['last_activity'] = now().timestamp()

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """ Récupérer l'adresse IP du client """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_hostname(self, ip):
        """ Récupérer le nom du PC client à partir de l'IP """
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return "Unknown"

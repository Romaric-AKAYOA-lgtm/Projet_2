from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json

# Importation des modèles
from Activation.models import Activation
from visiteur.models import Visiteur
from directeur.models import Directeur
from secretaire.models import Secretaire

def send_sms(phone_number, message):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    """
    Fonction fictive d'envoi de SMS (à remplacer par une vraie API).
    """
    print(f"Envoi du SMS à {phone_number}: {message}")
    # Simulation d'envoi de SMS : retourner un dictionnaire de succès
    return {"success": True, "message": "SMS envoyé avec succès !"}

@csrf_exempt
def send_sms_api(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    if request.method == "GET":
        # Récupérer les numéros des visiteurs, directeurs et secrétaires
        visiteurs = Visiteur.objects.all()
        directeurs = Directeur.objects.all()
        secretaires = Secretaire.objects.all()

        contacts = (
            [{"nom": v.nom, "prenom": v.prenom, "numero": v.contact, "role": "Visiteur"} for v in visiteurs] +
            [{"nom": d.nom, "prenom": d.prenom, "numero": d.num_tel, "role": "Directeur"} for d in directeurs] +
            [{"nom": s.last_name, "prenom": s.first_name, "numero": s.num_tel, "role": "Secrétaire"} for s in secretaires]
        )

        # Assurez-vous que le fichier "Notifications/send_sms.html" existe dans Notifications/templates/Notifications/
        return render(request, "Notifications/send_sms.html", {"contacts": contacts})

    elif request.method == "POST":
        try:
            # Récupérer les données du formulaire
            data = request.POST
            phone_number = data.get("manual_phone") or data.get("phone_number")
            message = data.get("message")

            if not phone_number or not message:
                return JsonResponse({"error": "Numéro et message requis"}, status=400)

            result = send_sms(phone_number, message)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Format JSON invalide"}, status=400)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

def my_view(request):
    """Affiche la page d'accueil avec la gestion du personnel et la vérification d'activation."""
    
    # 🔹 Vérifier l'activation
    activation = Activation.objects.first()
    if not activation or not activation.is_valid():
        return redirect("Activation:activation_page")  # Redirige vers une page d'activation si expiré

    return HttpResponseRedirect(reverse('Notifications:send_sms_api'))

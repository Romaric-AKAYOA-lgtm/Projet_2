import serial
import time

# Configuration du port série
SERIAL_PORT = "COM3"  # Remplace par ton port correct
BAUD_RATE = 115200

def send_sms(phone_number, message):
    try:
        # Ouvrir la connexion série avec le module GSM
        gsm = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Attendre l'initialisation du module

        # Vérifier la connexion
        gsm.write(b'AT\r')
        time.sleep(1)
        response = gsm.read(gsm.inWaiting()).decode()
        if "OK" not in response:
            return {"error": "Module GSM non détecté"}

        # Configurer le mode texte
        gsm.write(b'AT+CMGF=1\r')
        time.sleep(1)

        # Définir le numéro de téléphone du destinataire
        gsm.write(f'AT+CMGS="{phone_number}"\r'.encode())
        time.sleep(1)

        # Envoyer le message
        gsm.write(message.encode() + b'\r')
        time.sleep(1)

        # Envoyer la commande de fin (CTRL+Z = 26 en ASCII)
        gsm.write(bytes([26]))
        time.sleep(3)

        gsm.close()
        return {"status": "success", "message": "SMS envoyé avec succès"}
    
    except Exception as e:
        return {"error": str(e)}

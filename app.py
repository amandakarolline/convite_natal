from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")
SENDGRID_TO_EMAIL = os.getenv("SENDGRID_TO_EMAIL")

def enviar_email(mensagem):
    url = "https://api.sendgrid.com/v3/mail/send"

    data = {
        "personalizations": [{
            "to": [{"email": SENDGRID_TO_EMAIL}],
            "subject": "Resposta ao convite"
        }],
        "from": {"email": SENDGRID_FROM_EMAIL},
        "content": [{
            "type": "text/plain",
            "value": mensagem
        }]
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code >= 400:
        raise Exception(f"Erro ao enviar email: {response.text}")

@app.route("/notificar", methods=["POST"])
def notificar():
    data = request.get_json()
    mensagem = data.get("mensagem")

    if not mensagem:
        return jsonify({"error": "Mensagem vazia"}), 400

    try:
        enviar_email(mensagem)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "API de Notificação com SendGrid funcionando!"

if __name__ == "__main__":
    app.run()

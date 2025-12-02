from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

app = Flask(__name__)

# CONFIGURAÇÃO DO EMAIL
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def enviar_email(mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = "Resposta ao convite"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

@app.route("/notificar", methods=["POST"])
def notificar():
    data = request.get_json()
    mensagem = data.get("mensagem")

    if not mensagem:
        return jsonify({"error": "Mensagem vazia"}), 400

    enviar_email(mensagem)

    return jsonify({"status": "ok"}), 200


@app.route("/")
def home():
    return "API de Notificação funcionando!"


if __name__ == "__main__":
    app.run()


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO")


def send_alert_email(service_name: str, message: str, level: str):
    subject = f"[ALERTA {level.upper()}] Problema detectado em {service_name}"
    body = f"""
Atenção,

Um alerta de nível {level.upper()} foi gerado para o serviço: {service_name}

Detalhes:
{message}

Monitoramento Automático — Trabalho de Redes / DevOps
"""

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Conexão SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        print(f"[EMAIL] Alerta enviado para {ALERT_EMAIL_TO}")

    except Exception as e:
        print(f"[ERRO EMAIL] Falha ao enviar alerta: {e}")

from app.email_sender import send_alert_email

print("Teste de Envio de e-mail")

service = "TESTE_SMTP"
message = "Este é um e-mail de teste enviado pelo sistema de monitoramento."
level = "red"

try:
    send_alert_email(service, message, level)
    print(" Teste concluído. Se tudo deu certo, o e-mail deve ter chegado!")
except Exception as e:
    print(" Erro no teste:")
    print(e)

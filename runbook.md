# RUNBOOK — Guia de Operação do Sistema de Monitoramento DevOps
## 1. Visão Geral

Este runbook descreve como instalar, configurar, iniciar e operar a Plataforma de Monitoramento DevOps, composta por:

- Backend FastAPI (API + alerta automático por e-mail)

- Coletor de Métricas (simulador de métricas contínuas)

- Banco SQLite (monitor.db)

- Frontend React (dashboard do monitoramento)

O runbook cobre os procedimentos do dia a dia e não aborda incidentes — estes estão no Playbook.

##  2. Estrutura do Projeto
```text 
monitor-back-end/
│── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── email_sender.py
│   └── routers/
│       ├── metrics.py
│       ├── services.py
│       ├── status.py
│       └── alerts.py
│── collector/
│   └── collector.py
│── monitor.db
│── .env
│── requirements.txt
│── RUNBOOK.md
│── PLAYBOOK.md
```

## 3. Requisitos
Backend

- Python 3.10+

- FastAPI

- Uvicorn

- SQLite3

- Requests

Frontend

- Node.js 18+

- React + Tailwind

##  4. Configuração do Ambiente
### 4.1 Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

### 4.2 Instalar dependências
pip install -r requirements.txt

##  5. Arquivo .env

Crie na raiz:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=SEU_EMAIL@gmail.com
SMTP_PASS=SUA_SENHA_DE_APLICATIVO
ALERT_EMAIL_TO=SEU_EMAIL@gmail.com
```

##  6. Executando o Backend

Na pasta monitor-back-end:

```text 
uvicorn app.main:app --reload
```

A API estará disponível em:

     http://127.0.0.1:8000

Documentação Swagger:

     http://127.0.0.1:8000/docs

##  7. Executando o Coletor

Em outro terminal:

```text
python collector/collector.py
```

Ele envia métricas automaticamente a cada 30s.

##  8. Testando o sistema
Testar serviço Web:
http://127.0.0.1:8000/status/web

Testar alerta (DB crítico):

Se o coletor gerar valores vermelhos → você recebe e-mail.

Testar dashboard consolidado:
http://127.0.0.1:8000/status/dashboard/all

##  9. Testar envio de e-mail manual
```text
python test_email.py
```

##  10. Reset do Banco de Dados 
```text
rm monitor.db
python app/database.py
```

##  11. Parar processos
### Backend:
Ctrl + C

### Coletor:
Ctrl + C

##  12. Logs úteis
### Backend:
```text
uvicorn app.main:app --reload --log-level debug
``` 

### Coletor:

Exibe métricas enviadas no terminal.
# README — Guia de Instalação e Execução

# Plataforma de Monitoramento DevOps

## 1. Visão Geral

Este repositório contém a implementação completa de uma Plataforma de Monitoramento DevOps, composta por:

- Backend FastAPI — ingestão, armazenamento e cálculo de status dos serviços

- Coletor de Métricas — simula métricas contínuas de Web, Banco, DNS e SMTP

- Banco SQLite — (monitor.db)

- Frontend React + Tailwind — dashboard do monitoramento

- Alertas Automáticos por E-mail — nível VERMELHO

O objetivo é monitorar:

- Web Server

- Banco de Dados

- DNS

- SMTP

- Segurança

- Visão Consolidada

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
│       ├── consolidado.py
│       └── alerts.py
│── collector/
│   ├── collector.py
│   └── collector.txt
│── monitor.db
│── requirements.txt
│── .env
│── test_email.py
│
monitor-front-end/
│── src/
│   ├── App.tsx
│   ├── index.css
│   ├── components/
│   │     ├── Services.tsx
│   │     ├── Consolidated.tsx
│   │     └── charts/
│   │           └── LineChartCard.tsx
│── package.json
│── vite.config.ts
│── README.md
```

## 3. Pré-requisitos
Backend

- Python 3.10+

- SQLite3

- Pip / venv

- Pacotes do requirements.txt

Frontend

- Node.js 18+

- NPM ou Yarn

## 4. Instalação do Backend

No diretório monitor-back-end:

### 4.1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

### 4.2 Instalar dependências
pip install -r requirements.txt

## 5. Configuração do Arquivo .env

Crie um arquivo .env dentro de monitor-back-end/:

```ini
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=SEU_EMAIL@gmail.com
SMTP_PASS=SENHA_DE_APLICATIVO
ALERT_EMAIL_TO=EMAIL_QUE_RECEBERÁ_ALERTAS
```

Importante: Para Gmail, crie uma Senha de Aplicativo (não funciona senha normal).

##  6. Executando o Backend

Dentro de monitor-back-end execute:

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```bash
http://127.0.0.1:8000
```

Documentação Swagger:
```bash
http://127.0.0.1:8000/docs
```

## 7. Executando o Coletor de Métricas

Em outro terminal:
```bash
python collector/collector.py
```

Ele envia novas métricas a cada 30 segundos.

## 8. Executando o Frontend

No diretório monitor-front-end:

### 8.1 Instalar dependências
```bash
npm install
```
### 8.2 Rodar o servidor
```bash
npm run dev
```

Acesse no navegador:
```bash
http://localhost:5173
```

O dashboard deve exibir:

- Cartões dos serviços

- Alertas

- Métricas e gráficos (via Recharts)

- Visão consolidada

## 9. Testando Envio de E-mail

No backend:

- python test_email.py


Se tudo estiver correto, aparecerá:

```bash
[EMAIL] Alerta enviado para ....
```

E você deve receber o e-mail.

## 10. Reset do Banco de Dados (opcional)

Se quiser limpar tudo:
```bash
rm monitor.db
python app/database.py   # recria tabelas
```
## 11. Testes Manuais Úteis
Testar status do Web Server:
```bash
curl http://127.0.0.1:8000/status/service/web
```
Testar consolidado:
```bash
curl http://127.0.0.1:8000/status/consolidado
```

Ver todos os serviços:
```bash
curl http://127.0.0.1:8000/status/dashboard/all
```

## 12. Parar o Sistema
Backend
Ctrl + C

Coletor
Ctrl + C

Frontend
Ctrl + C

## 13. Licença

Uso acadêmico — Disciplina de Redes e Internet — IDP.

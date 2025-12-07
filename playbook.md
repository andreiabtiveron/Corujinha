#  PLAYBOOK — Procedimentos de Resposta a Incidentes

Este documento orienta o que fazer quando algum serviço entra em estado amarelo (atenção) ou vermelho (crítico).

##  1. Severidade dos Alertas
    Cor     -  Nível  -   Significado
🟩 Green	-    1	  -  Operação normal
🟨 Yellow	-    2	  -  Degradação moderada — observar
🟥 Red	    -    3	  -  Incidente crítico — ação imediata

##  2. Web Server — Playbook
### Alerta Amarelo

Motivos possíveis:

- Latência > 1000 ms

- Taxa de erro > 2%

Ações:

- Checar conectividade externa:
```text
ping google.com
```

- Verificar carga no coletor (pico de simulação).

- Revisar logs do frontend/backend.

### Alerta Vermelho

Motivos:

- Latência > 2000 ms

- Error rate > 10%

- Serviço indisponível

T- ráfego anômalo

Ações imediatas:

- Verificar se o backend está rodando:

```text
ps aux | grep uvicorn
```

- Reiniciar serviço:

```text
uvicorn app.main:app --reload
```

- Validar conexão com a internet.

- Procurar anomalias de tráfego, possível ataque.

##  3. Database — Playbook
### Alerta Amarelo

Motivos:

- CPU 70–90%

- Memória 2500–3500 MB

- Lentidão moderada

- Rollbacks até 3%

Ações:

- Verificar queries lentas.

- Checar crescimento do banco (db_size_gb).

- Analisar uso de CPU/Memória.

### Alerta Vermelho

Motivos:

- CPU > 90%

- Memória > 3500 MB

- Slow queries > 10

- Conexões > 250

- Vulnerabilidade detectada

- Falhas de autenticação altas

Ações imediatas:

- Reiniciar banco simulado:

```text
restart collector simulation
```

- Checar integridade do ambiente .env.

- Validar se o coletor não gerou valores extremos repetidos.

- Acompanhar logs com:

```text
tail -f collector.log
```

##  4. DNS — Playbook
### Amarelo

- Latência > 80 ms

- Falhas > 1%

Ações:

- Testar DNS manual:

```text
nslookup google.com
```

### Vermelho

- Latência > 150 ms

- Falhas > 5%

- Vulnerabilidade ou anomalia

Ações:

- Verificar conexão com DNS.

- Reiniciar coletor.

- Identificar possível ataque DNS.

##  5. SMTP — Playbook
### Amarelo

- Fila 10–30

- Erros moderados

Ações:

- Verificar fila simulada.

- Garantir que Gmail SMTP não bloqueou conexões.

### Vermelho

- Fila > 30

- Throughput < 1

- Vulnerabilidade detectada

Ações:

- Checar .env - senha SMTP.

- Testar envio:

```python
python test_email.py
```

- Reiniciar serviço SMTP simulado.

##  6. Quando escalar

Escalar para o responsável quando:

- 3 alertas vermelhos consecutivos

- Latência de DB > 20 ms por mais de 5 ciclos

- Fila SMTP > 40

- Falhas DNS constantes

- Envio de e-mail falhar continuamente

##  7. Finalizar incidente

Marcar como resolvido quando:

- Alertas voltarem para 🟩 green

- Logs confirmarem estabilidade

- Últimas 5 medições estiverem dentro do normal
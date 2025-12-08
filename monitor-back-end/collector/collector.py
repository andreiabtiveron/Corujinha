import time
import requests
import random

API_BASE = "http://127.0.0.1:8000"

# valores-base mais realistas
def jitter(base, spread):
    return base + random.uniform(-spread, spread)

def send(service, metric, value, unit):
    try:
        r = requests.post(
            f"{API_BASE}/metrics/ingest",
            json={
                "service_key": service,
                "metric_name": metric,
                "value": value,
                "unit": unit,
            },
            timeout=3
        )
        print(f"[OK] {service} → {metric} = {value} {unit}")
    except Exception as e:
        print("[ERRO]", e)


# ==========================================================
# WEB SERVER — agora com latências mais moderadas
# ==========================================================
def web_metrics():
    return {
        "latency_ms": jitter(400, 250),             # antes 2000+ → agora ~200–650ms
        "availability": 1,
        "rps": jitter(80, 20),
        "error_rate": max(0, jitter(0.01, 0.015)),  # 0% – 3%
        "traffic_anomaly": random.choice([0, 0, 0, 1]),
        "auth_failures": random.randint(0, 4),      # antes 15 → agora 0–4
        "config_change": random.choice([0, 0, 0, 1]),
        "known_vulnerability": random.choice([0, 0, 0, 1]),
    }


# ==========================================================
# DATABASE — menos agressivo para não ficar sempre RED
# ==========================================================
def db_metrics():
    return {
        "availability": 1,
        "qps": jitter(120, 60),
        "slow_queries": random.randint(0, 8),            # antes 14 → agora 0–8
        "cpu_usage": jitter(40, 20),                     # 20–60%
        "memory_mb": jitter(2200, 500),                  # 1700–2700
        "open_connections": jitter(120, 80),             # 40–200
        "rollback_rate": max(0, jitter(0.02, 0.015)),     # ~0.01–0.035
        "disk_latency_ms": jitter(8, 4),                 # ~4–12ms
        "db_size_gb": jitter(10.5, 0.3),
        "auth_failures": random.randint(0, 3),
        "config_change": random.choice([0, 0, 0, 1]),
        "known_vulnerability": random.choice([0, 0, 0, 1]),
        "slow_query_spike": random.randint(0, 1),
    }


# ==========================================================
# DNS — latências mais baixas para evitar RED constante
# ==========================================================
def dns_metrics():
    return {
        "latency_ms": jitter(60, 25),                 # antes 155 → agora 35–85ms
        "failures": random.choice([0, 0, 0, 1]),
        "qps": jitter(300, 100),
        "traffic_anomaly": random.choice([0, 0, 0, 1]),
        "config_change": random.choice([0, 0, 0, 1]),
        "known_vulnerability": random.choice([0, 0, 0, 1]),
    }


# ==========================================================
# SMTP — fila muito mais leve
# ==========================================================
def smtp_metrics():
    return {
        "queue_length": random.randint(0, 18),       # antes 36 → agora 0–18
        "throughput": jitter(60, 20),
        "errors": random.choice([0, 0, 1, 1, 2]),    # raramente passa de 2
        "auth_failures": random.randint(0, 3),
        "queue_spike": random.randint(0, 1),
        "known_vulnerability": random.choice([0, 0, 0, 1]),
        "config_change": random.choice([0, 0, 0, 1]),
    }


SERVICES = {
    "web": web_metrics,
    "db": db_metrics,
    "dns": dns_metrics,
    "smtp": smtp_metrics,
}


# ==========================================================
# LOOP PRINCIPAL
# ==========================================================
def loop():
    while True:
        for service, generator in SERVICES.items():
            metrics = generator()
            for name, value in metrics.items():
                send(service, name, float(value), "")
        print("---- ciclo completo ----\n")
        time.sleep(4)  # ciclo mais rápido sem sobrecarregar o servidor


if __name__ == "__main__":
    loop()

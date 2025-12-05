import time
import requests
import random

API_BASE = "http://127.0.0.1:8000"

def send_metric(service_key: str, metric_name: str, value: float, unit: str):
    payload = {
        "service_key": service_key,
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
    }

    try:
        r = requests.post(f"{API_BASE}/metrics/ingest", json=payload, timeout=5)
        print(f"[OK] {service_key} → {metric_name} = {value} {unit}")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar métrica: {e}")

#Web server
def collect_web():
    start = time.time()
    try:
        req = requests.get("https://google.com", timeout=3)
        latency = (time.time() - start) * 1000  # ms
        availability = 1 if req.status_code == 200 else 0
    except Exception:
        latency = 1500  # ms
        availability = 0

    send_metric("web", "latency_ms", latency, "ms")
    send_metric("web", "availability", availability, "bool")

    # simulações
    rps = random.uniform(10, 80)
    error_rate = random.choice([0.0, 0.002, 0.01, 0.05, 0.1])

    send_metric("web", "rps", rps, "req/s")
    send_metric("web", "error_rate", error_rate, "ratio")

#database
def collect_db():
    # 0–1 significa ativo/parado 
    availability = random.choice([1, 1, 1, 0])  #mais chances de estar UP
    qps = random.uniform(5, 200)
    slow_queries = random.randint(0, 10)
    cpu = random.uniform(5, 95)
    mem = random.uniform(200, 2000)  # MB

    send_metric("db", "availability", availability, "bool")
    send_metric("db", "qps", qps, "queries/s")
    send_metric("db", "slow_queries", slow_queries, "count")
    send_metric("db", "cpu_usage", cpu, "%")
    send_metric("db", "memory_mb", mem, "MB")

#aqui dns pipipipopopo
def collect_dns():
    dns_latency = random.uniform(10, 200)
    failures = random.choice([0, 0, 0, 1])
    qps = random.uniform(100, 800)

    send_metric("dns", "latency_ms", dns_latency, "ms")
    send_metric("dns", "failures", failures, "count")
    send_metric("dns", "qps", qps, "queries/s")

#smtp
def collect_smtp():
    queue = random.randint(0, 50)
    throughput = random.uniform(5, 200)
    errors = random.choice([0, 0, 0, 1, 2])

    send_metric("smtp", "queue_length", queue, "emails")
    send_metric("smtp", "throughput", throughput, "emails/min")
    send_metric("smtp", "errors", errors, "count")

# aqui faz o loop principal
def main():
    print("Iniciando coletor…")
    while True:
        collect_web()
        collect_db()
        collect_dns()
        collect_smtp()
        print("---- ciclo completo ----\n")
        time.sleep(30)

if __name__ == "__main__":
    main()

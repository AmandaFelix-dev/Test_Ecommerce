import pytest
import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor
from tests.stress.metricas import registrar_gateway_delay, registrar_diario

BASE_URL = "http://localhost:8000"
CSV_PATH = "tests/stress/relatorios/stress_resultados.csv"


usuarios_teste = [
    1000,
    2500,
    5000,
    7500,
    10000,
    15000,
    20000,
    30000,
]


resultados = []


@pytest.mark.stress

def test_stress():
    registrar_gateway_delay()

    for usuarios in usuarios_teste:
        inicio = time.time()

        falhas = 0
        sucessos = 0

        def bater_endpoint(_):
            try:
                r = requests.get(f"{BASE_URL}/")
                return r.status_code == 200
            except Exception:
                return False

        with ThreadPoolExecutor(max_workers=usuarios) as executor:
            respostas = list(executor.map(bater_endpoint, range(usuarios)))

        for r in respostas:
            if r:
                sucessos += 1
            else:
                falhas += 1

        tempo_total = round(time.time() - inicio, 2)

        taxa_falha = (falhas / usuarios) * 100

        resultados.append({
            "usuarios": usuarios,
            "sucessos": sucessos,
            "falhas": falhas,
            "taxa_falha": taxa_falha,
            "tempo_total": tempo_total,
        })

        registrar_diario(
            f"Usuarios={usuarios} | Falhas={falhas} | Tempo={tempo_total}s"
        )

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as csvfile:
        campos = [
            "usuarios",
            "sucessos",
            "falhas",
            "taxa_falha",
            "tempo_total",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()

        for linha in resultados:
            writer.writerow(linha)
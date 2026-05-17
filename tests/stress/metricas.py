from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

DIARIO = "tests/stress/relatorios/diario_stress.md"


def registrar_diario(msg):
    with open(DIARIO, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def registrar_gateway_delay():
    valor = os.getenv("GATEWAY_DELAY_SECONDS")
    registrar_diario(f"GATEWAY_DELAY_SECONDS={valor}")
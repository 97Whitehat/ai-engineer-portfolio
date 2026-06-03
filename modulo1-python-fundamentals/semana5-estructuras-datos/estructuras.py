from collections import Counter, defaultdict
import heapq

# Datos de prueba — alertas simuladas
ALERTAS = [
    {"cliente": "Restaurante El Patio", "obligacion": "IVA", "dias": 5},
    {"cliente": "Fontanería Martínez", "obligacion": "IRPF", "dias": 5},
    {"cliente": "Academia de Inglés Torres", "obligacion": "IVA", "dias": 15},
    {"cliente": "Transporte López e Hijos", "obligacion": "IRPF", "dias": 15},
    {"cliente": "Fontanería Martínez", "obligacion": "IS", "dias": 15},
    {"cliente": "Restaurante El Patio", "obligacion": "IRPF", "dias": 28},
    {"cliente": "Clínica Dental Ruiz", "obligacion": "IS", "dias": 30},
    {"cliente": "Academia de Inglés Torres", "obligacion": "IVA", "dias": 3},
    {"cliente": "Transporte López e Hijos", "obligacion": "IVA", "dias": 22},
    {"cliente": "Clínica Dental Ruiz", "obligacion": "IRPF", "dias": 8},
]

# punto 1
contador = Counter(alerta["obligacion"] for alerta in ALERTAS)

# punto 2
grupos = defaultdict(list)

for alerta in ALERTAS:
    if alerta["dias"] <= 5:
        nivel = "urgente"
    elif alerta["dias"] <= 15:
        nivel = "próxima"
    else:
        nivel = "en plazo"

    grupos[nivel].append(alerta["cliente"])

# punto 3
heap = [(a["dias"], a["cliente"], a["obligacion"]) for a in ALERTAS]
heapq.heapify(heap)

top3 = [heapq.heappop(heap) for _ in range(3)]

# punto 4
ordenadas = sorted(ALERTAS, key=lambda a: a["dias"])


# --------------------------------PRINTS----------------------
print("── Punto 1 — Por obligación ──")
print(contador)

print("\n── Punto 2 — Por urgencia ──")
for nivel, clientes in grupos.items():
    print(f"{nivel}: {clientes}")

print("\n── Punto 3 — Top 3 urgentes ──")
print(top3)

print("\n── Punto 4 — Ordenadas por días ──")
for a in ordenadas:
    print(f"{a['dias']} días — {a['cliente']} — {a['obligacion']}")

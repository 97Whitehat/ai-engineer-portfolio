from datetime import date, timedelta

# --------CLIENTES GESTORÍA ---------
# Cada cliente es un diccionario independiente con su nombre asociado y sus oblicaciones fiscales dado que no todos tienen las mismas responsabilidades de pagos.

CLIENTES = [
    {"nombre": "Restaurante El Patio",       "obligaciones": ["IVA", "IRPF"]},
    {"nombre": "Fontanería Martínez",        "obligaciones": ["IVA", "IRPF", "IS"]},
    {"nombre": "Academia de Inglés Torres",  "obligaciones": ["IVA"]},
    {"nombre": "Clínica Dental Ruiz",        "obligaciones": ["IRPF", "IS"]},
    {"nombre": "Transporte López e Hijos",   "obligaciones": ["IVA", "IRPF"]},
]

EMAILS_CLIENTES = {
    "Restaurante El Patio":      'gabimori97@gmail.com',
    "Fontanería Martínez":       'gabimori97@gmail.com',
    "Academia de Inglés Torres": 'gabimori97@gmail.com',
    "Clínica Dental Ruiz":       'gabimori97@gmail.com',
    "Transporte López e Hijos":  'gabimori97@gmail.com'
}

# -------CALENDARIO FISCAL ---------
# Lista de fechas fiscales reales del calendario español.
# Cada entrada propia tendrá:
#   - nombre: el impuesto o declaración
#   - fecha: cuándo vence (usamos date de datetime, no strings)
#   - obligacion: clave que conecta con las obligaciones de cada cliente
#                 así sabemos a qué clientes afecta cada fecha

FECHAS_FISCALES = [
    {
        "nombre": "IVA 2T 2026",
        "fecha": date(2026, 7, 20),
        "obligacion": "IVA"
    },
    {
        "nombre": "IRPF 2T 2026",
        "fecha": date(2026, 7, 20),
        "obligacion": "IRPF"
    },
    {
        "nombre": "Pago fraccionado IS 2T 2026",
        "fecha": date(2026, 10, 20),
        "obligacion": "IS"
    },
    {
        "nombre": "IVA 3T 2026",
        "fecha": date(2026, 10, 20),
        "obligacion": "IVA"
    },
    {
        "nombre": "IRPF 3T 2026",
        "fecha": date(2026, 10, 20),
        "obligacion": "IRPF"
    },
    {
        "nombre": "Declaración Anual IS 2026",
        "fecha": date(2027, 1, 25),
        "obligacion": "IS"
    },

    # Fechas de prueba para la demo — se eliminan en producción
    {
        "nombre": "IVA 2T 2026",
        "fecha": date.today() + timedelta(days=5),
        "obligacion": "IVA"
    },
    {
        "nombre": "IRPF 2T 2026",
        "fecha": date.today() + timedelta(days=15),
        "obligacion": "IRPF"
    },
    {
        "nombre": "Pago fraccionado IS",
        "fecha": date.today() + timedelta(days=30),
        "obligacion": "IS"
    },
]
# Sistema de Alertas Fiscales — Gestoría López & Asociados

## El problema

Gestoría López & Asociados gestiona 80 clientes entre autónomos y pequeñas empresas.
Cada semana, uno de sus 5 empleados revisaba manualmente un Excel con fechas fiscales
y llamaba o escribía a cada cliente que tenía algo que vencer próximamente.

**Tiempo perdido: ~1.5h/día. Riesgo de error: alto. Escalabilidad: ninguna.**

## La solución

Sistema automatizado en Python que monitoriza el calendario fiscal español,
detecta vencimientos próximos y genera alertas automáticas para cada cliente afectado.
Incluye un dashboard web para visualizar las alertas en tiempo real.

## Funcionalidades

- Alertas automáticas para vencimientos en los próximos 30 días
- Tres niveles de urgencia: crítico (5 días), próximo (15 días), en plazo (30 días)
- Calendario fiscal real: IVA trimestral, IRPF, pagos fraccionados, Impuesto de Sociedades
- Dashboard web con KPIs, tabla de alertas por urgencia y estado de clientes
- Logging completo con rotación — historial de todas las alertas en gestor.log
- Manejo de errores robusto con excepciones personalizadas
- Tests con pytest — 96% de cobertura

## Stack

Python 3.8+ · dataclasses · logging · pytest · pytest-cov · HTML/CSS/JS

## Estructura

```
p1-alertas-automaticas/
├── alertas.py       # Lógica principal — SistemaAlertas, Alerta, excepciones
├── datos.py         # Clientes y calendario fiscal
├── test_alertas.py  # Tests — 11 tests, 96% cobertura
├── reporte.json     # Generado automáticamente por alertas.py
└── gestor.log       # Log con historial de alertas
```

## Cómo ejecutarlo

```bash
# Instalar dependencias
pip install pytest pytest-cov

# Generar el reporte de alertas
cd gestoria-lopez/p1-alertas-automaticas
python alertas.py

# Ver el dashboard — desde la raíz del repo
cd ../../
python -m http.server 8000
# Abrir http://localhost:8000/core/dashboard/

# Ejecutar los tests
cd gestoria-lopez/p1-alertas-automaticas
pytest test_alertas.py -v

# Ver cobertura
pytest --cov=alertas --cov-report=term-missing test_alertas.py
```

## Resultado

```
🏢 Gestoría López & Asociados — Sistema de Alertas Fiscales
============================================================
📅 Fecha actual: 29/05/2026

🚨 ALERTA —  5 días  | IVA 2T 2026          | Restaurante El Patio
🚨 ALERTA —  5 días  | IVA 2T 2026          | Fontanería Martínez
⚠️  ALERTA — 15 días  | IRPF 2T 2026         | Restaurante El Patio
📅 ALERTA — 30 días  | Pago fraccionado IS  | Fontanería Martínez

📊 Resumen: 10 alerta(s) generada(s) · Log guardado en gestor.log
```

## Tests

```
$ pytest test_alertas.py -v
collected 11 items

test_alertas.py::test_calcular_dias_restantes[5-5]       PASSED
test_alertas.py::test_calcular_dias_restantes[15-15]     PASSED
test_alertas.py::test_calcular_dias_restantes[30-30]     PASSED
test_alertas.py::test_fecha_pasada_lanza_error           PASSED
test_alertas.py::test_generar_alertas_devuelve_lista     PASSED
test_alertas.py::test_generar_alertas_son_alertas        PASSED
test_alertas.py::test_generar_alertas_campos_completos   PASSED
test_alertas.py::test_alerta_dias_dentro_de_rango        PASSED
test_alertas.py::test_alerta_str                         PASSED
test_alertas.py::test_handle_errors_captura_excepcion    PASSED
test_alertas.py::test_handle_errors_devuelve_default     PASSED

11 passed — coverage: 96%
```

## Contexto

Proyecto 1 del curriculum AI Engineer — Módulo 1 Python Fundamentals.
Caso de uso real basado en Gestoría López & Asociados, empresa ficticia
utilizada como hilo conductor de todos los proyectos del roadmap.
El dashboard forma parte del core compartido — se irá ampliando con cada proyecto.
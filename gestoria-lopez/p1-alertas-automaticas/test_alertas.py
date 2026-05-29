import pytest
from datetime import date, timedelta
from alertas import SistemaAlertas, Alerta, FechaInvalidaError, handle_errors


# ── FIXTURES ──────────────────────────────────────────────
@pytest.fixture
def sistema():
    return SistemaAlertas()


# ── handle_errors ────────────────────────────────
def test_handle_errors_captura_excepcion(sistema):
    # generar_alertas está decorada con @handle_errors
    # Si le metemos datos que fallen, el decorador devuelve []
    # Esto cubre el bloque except del decorador
    from unittest.mock import patch
    with patch('alertas.FECHAS_FISCALES', [{"nombre": "test", "fecha": "fecha_invalida", "obligacion": "IVA"}]):
        resultado = sistema.generar_alertas()
        assert resultado == []

def test_generar_alertas_ignora_fechas_vencidas(sistema):
    from unittest.mock import patch
    from datetime import date, timedelta
    fechas_con_vencida = [
        {"nombre": "Vencida", "fecha": date.today() - timedelta(days=10), "obligacion": "IVA"}
    ]
    with patch('alertas.FECHAS_FISCALES', fechas_con_vencida):
        resultado = sistema.generar_alertas()
        assert resultado == []

def test_handle_errors_devuelve_default():
    @handle_errors(default_return="error")
    def funcion_que_falla():
        raise ValueError("fallo deliberado")
    
    resultado = funcion_que_falla()
    assert resultado == "error"

# ── calcular_dias_restantes ────────────────────────────────

@pytest.mark.parametrize('dias_offset, esperado', [
    (5,  5),
    (15, 15),
    (30, 30),
])
def test_calcular_dias_restantes(sistema, dias_offset, esperado):
    fecha = date.today() + timedelta(days=dias_offset)
    assert sistema.calcular_dias_restantes(fecha) == esperado


def test_fecha_pasada_lanza_error(sistema):
    fecha_pasada = date.today() - timedelta(days=1)
    with pytest.raises(FechaInvalidaError):
        sistema.calcular_dias_restantes(fecha_pasada)


# ── generar_alertas ────────────────────────────────────────

def test_generar_alertas_devuelve_lista(sistema):
    resultado = sistema.generar_alertas()
    assert isinstance(resultado, list)


def test_generar_alertas_son_alertas(sistema):
    resultado = sistema.generar_alertas()
    # Si hay alertas, todas deben ser instancias de Alerta
    for alerta in resultado:
        assert isinstance(alerta, Alerta)


def test_generar_alertas_campos_completos(sistema):
    resultado = sistema.generar_alertas()
    for alerta in resultado:
        assert alerta.cliente
        assert alerta.obligacion
        assert alerta.dias_restantes >= 0
        assert isinstance(alerta.fecha_vencimiento, date)


def test_alerta_dias_dentro_de_rango(sistema):
    resultado = sistema.generar_alertas()
    # Ninguna alerta debe tener más de 30 días — el sistema las filtra
    for alerta in resultado:
        assert alerta.dias_restantes <= 30



def test_alerta_str(sistema):
    # Comprueba que el __str__ de Alerta funciona correctamente
    alerta = Alerta(
        cliente="Restaurante El Patio",
        obligacion="IVA 2T 2026",
        dias_restantes=5,
        fecha_vencimiento=date.today() + timedelta(days=5)
    )
    resultado = str(alerta)
    assert "Restaurante El Patio" in resultado
    assert "5" in resultado
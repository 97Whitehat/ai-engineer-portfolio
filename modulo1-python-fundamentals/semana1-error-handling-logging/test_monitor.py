import pytest
from monitor import obtener_precio, TickerInvalidoError
from unittest.mock import patch


# Fixture
@pytest.fixture
def tickets_validos():
    return ["AAPL", "GOOG", "MSFT"]


@pytest.mark.parametrize(
    "ticker, esperado", [("AAPL", 20), ("GOOG", 20), ("", 0), ("ERROR", 0)]
)
def test_obtener_precio(ticker, esperado):
    assert obtener_precio(ticker) == esperado


def test_precio_simulado():
    with patch("monitor.obtener_precio", return_value=150.0) as mock_precio:
        mock_precio.return_value = 150.0
        resultado = mock_precio("AAPL")
        assert resultado == 150.0


def test_ticker_vacio_lanza_error():
    with pytest.raises(TickerInvalidoError):
        obtener_precio.__wrapped__("")

import logging
import functools
from logging.handlers import RotatingFileHandler


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = RotatingFileHandler('monitor.log', maxBytes=1_000_000, backupCount=5)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

logger = setup_logger(__name__)

class TickerInvalidoError (Exception):
    pass


def handle_errors(default_return= None):
    def decorator (func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f'Error en {func.__name__}: {e}',
                    exc_info= True
                )
                return default_return
        return wrapper
    return decorator


@handle_errors(default_return=0)
def obtener_precio(ticker):

    if ticker == '':
        raise TickerInvalidoError(f'El campo ticker está vacío')
    
    if ticker == "ERROR":
        raise Exception(f'Se ha generado un fallo en la conexión con la API')
    
    return 20

print(obtener_precio(""))
print(obtener_precio("ERROR"))
print(obtener_precio("AAPL"))
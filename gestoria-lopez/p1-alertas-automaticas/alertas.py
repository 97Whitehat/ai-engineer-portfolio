import logging
import functools
import json
from datetime import date
from dataclasses import dataclass, field
from logging.handlers import RotatingFileHandler
from typing import List
from datos import CLIENTES, FECHAS_FISCALES

# ----- LOGGER -------------------
# Fichero rotacional de logs

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #Handler fichero rotación
    fh = RotatingFileHandler('gestor.log', maxBytes=1_000_000, backupCount= 5)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    #Formating
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

logger = setup_logger(__name__)

#------- EXCEPTIONS PERSONALIZADAS -------
# Por el momento, se incluyen 2 tipos de error especificos de nuestro dominio:
# FechaInvalidaError - cuando una fecha está mal formada o es del pasado
# ClienteNoEncontradoError - cuando buscamos un cliente que no existe
class FechaInvalidaError(Exception):
    pass

class ClienteNoEncontradoError(Exception):
    pass

# ------ DECORATORS --------
# Handle errors para capturar las excepciones
# Lo utilizamos para que, en caso de tener que modificar el cómo se muestran los errores, 
# no tener que ir caso a caso, sino que con esto es suficiente de cambio

def handle_errors(default_return = None):
    def decorator(func):
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

# ------ DATACLASS ALERTA -------
# Alerta es un contenedor de datos
# __str__ lo definimos nosotros para que el print sea bonito
# en la demo — el resto (__init__, __repr__, __eq__) los
# genera dataclass automáticamente.

@dataclass
class Alerta:
    cliente: str
    obligacion: str
    dias_restantes: int
    fecha_vencimiento: date

    def __str__(self):
        if self.dias_restantes <=5:
            icono = "🚨"

        elif self.dias_restantes <= 15:
            icono = "⚠️"

        else:
            icono = "📅"
        
        return (
            f"{icono} ALERTA — {self.dias_restantes} días  "
            f"| {self.obligacion:<30} "
            f"| {self.cliente}"
        )
    
# ------ SISTEMA DE ALERTAS ---------
# Clase ppal, 2 responsabilidades : 
# 1. calcular_dias_restantes - cuantos días faltan para una fecha 
# 2. generar_alertas - recorre el calendario, detecta que hay vencimientos próxiomos 
# y crea alerta para los clientes que se vean afectados

# Los umbrales puestos son de 30, 15 y 5 días - igual que haría un gestor humano:
# aviso con un mes, 15 dias y ya con una mayor urgencia.

class SistemaAlertas:

    

    def calcular_dias_restantes(self, fecha: date) -> int:
        dias = (fecha - date.today()).days
        if dias < 0:
            raise FechaInvalidaError(
                f'La fecha {fecha} ya ha vencido - hace {abs(dias)} días'
            )
        return dias
    
    @handle_errors(default_return=[])
    def generar_alertas(self) -> List[Alerta]:
        alertas = []

        for fecha_fiscal in FECHAS_FISCALES:
            try:
                dias = self.calcular_dias_restantes(fecha_fiscal["fecha"])
            except FechaInvalidaError as e:
                
                # Aquí es el momento de loggear en caso de error con la fecha por ser vencida
                # Si no loggeamos y continuamos, el vencimiento puede provocar el bloqueo del sistema y no
                # queremos eso.
                logger.warning(f'Fecha vencida ignorada: {e}')
                continue

            #Tras solventar este problema, generamos alerta si estamos dentro de umbral

            #  27-05-2026 Alertamos solo si tienemos los dias exactos metidos en el umbral, fácil de editar si metemos mas dias en los umbrales
            #  29-05-2026 Ahora te aparecen los comunicados independientemente de la fecha mientras estén en los 30 dias de fecha.
            if dias > 30:
                continue

            # Busqueda de clientes con necesidad de hacer notificación de alertas
            for cliente in CLIENTES:
                if fecha_fiscal['obligacion'] in cliente['obligaciones']:
                    alerta = Alerta(
                        cliente= cliente["nombre"],
                        obligacion= fecha_fiscal["nombre"],
                        dias_restantes= dias,
                        fecha_vencimiento= fecha_fiscal["fecha"]
                    )
                    alertas.append(alerta)
                    logger.info(
                        f'Alerta generada - {dias} días - {fecha_fiscal["nombre"]} - {cliente["nombre"]}'
                    )
        
        return alertas
    
# ------ MAIN ------
# 3 partes: 
#   1. Cabecera 
#   2. Generación y muestra de alertas 
#   3. Resumen final 

def main():
    sistema = SistemaAlertas()

    # Cabecera
    print("\n🏢 Gestoría López & Asociados — Sistema de Alertas Fiscales")
    print("=" * 60)
    print(f"📅 Fecha actual: {date.today().strftime('%d/%m/%Y')}\n")
    
    # ── Generación de alertas ──
    alertas = sistema.generar_alertas()

    if not alertas:
        print("✅ No hay alertas pendientes en este momento.")
    else:
        for alerta in alertas:
            print(alerta)  # usa el __str__ que definimos en la dataclass

    
    # ── Resumen ──
    print("\n" + "=" * 60)
    print(f"📊 Resumen: {len(alertas)} alerta(s) generada(s)")
    print(f"📁 Log guardado en: gestor.log")
    print("=" * 60)

    # ---- Exportación de JSON ---- inicial unicamente para la P1 para poder plasmar la información en el dashboard

    reporte = {
        'fecha': date.today().strftime("%d/%m/%Y"),
        'total': len(alertas),
        'alertas': [
            {
                'cliente': a.cliente,
                'obligacion': a.obligacion,
                'dias_restantes': a.dias_restantes,
                'fecha_vencimiento': a.fecha_vencimiento.strftime('%d/%m/%Y')
            }
            for a in alertas
        ]
    }

    with open('reporte.json', 'w', encoding='utf-8') as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    logger.info(f'Reporte exportado a reporte.json')

    
if __name__ == "__main__":
    main()
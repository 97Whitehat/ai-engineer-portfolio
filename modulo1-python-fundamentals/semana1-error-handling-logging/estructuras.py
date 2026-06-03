# list_palabras = [x for x in lista_nombres if len(x.split()) > 5 ]


def contar_tokens(texto: str, conteo_palabras: int = 10):
    texto_split = texto.split()
    for i in range(0, len(texto_split), conteo_palabras):
        yield texto_split[i : i + conteo_palabras]


texto = "a " * 25
acumulado = 0
for conteo in contar_tokens(texto):
    acumulado += len(conteo)
    print(f"imprime cada {acumulado}")


def log_llamada(func):
    def wrapper(*arg, **kargs):
        print(f"llamada a funcion {func.__name__}")
        print(f"con argumentos {arg, kargs}")
        res = func(*arg, **kargs)
        return res

    return wrapper


@log_llamada
def sumar(a, b):
    return a + b


sumar(3, 5)

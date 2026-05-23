class Conversacion:

    def __init__(self, modelo: str, max_mensajes: int):
        self.modelo = modelo
        self.max_mensajes =  max_mensajes
        self.historial = []

    def añadir_mensaje(self, rol, contenido):
        if len(self) >= self.max_mensajes:
            self.historial.pop(0)
        self.historial.append({'rol': rol, 'contenido': contenido})

    def __len__(self):
        return len(self.historial)
    def __str__(self):
        return f'Conversacion(model={self.modelo}, mensajes= {len(self)})'

conv = Conversacion("claude-sonnet", 3)
conv.añadir_mensaje("user", "hola")
conv.añadir_mensaje("assistant", "¿cómo estás?")
conv.añadir_mensaje("user", "bien")
print(conv)
print(len(conv))

conv.añadir_mensaje("assistant", "me alegro")  # este debería eliminar el primero
print(conv.historial)  # el primer mensaje "hola" ya no debería estar
class Transaccion:
    def __init__(self, id, servicio, cliente, estado):
        self.id = id
        self.servicio = servicio
        self.cliente = cliente
        self.estado = estado  # 'pendiente', 'completado', 'cancelado'
class Transaction:
    def __init__(self, id, service, client, status):
        self.id = id
        self.service = service
        self.client = client
        self.status = status  # 'pendiente', 'completado', 'cancelado'
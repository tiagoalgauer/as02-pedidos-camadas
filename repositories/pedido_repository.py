class PedidoRepository:
    def __init__(self):
        self._pedidos = []
        self._proximo_id = 1

    def salvar(self, clienteId, itens, total):
        pedido = {
            "id": self._proximo_id,
            "clienteId": clienteId,
            "itens": itens,
            "total": total,
            "status": "confirmado",
        }
        self._proximo_id += 1
        self._pedidos.append(pedido)
        return pedido

    def buscar_por_id(self, pedido_id):
        return next((p for p in self._pedidos if p["id"] == pedido_id), None)

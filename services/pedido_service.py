from repositories.estoque_repository import EstoqueRepository
from repositories.pedido_repository import PedidoRepository

class ErroValidacao(Exception):
    pass

class EstoqueInsuficiente(Exception):
    pass

class PagamentoRecusado(Exception):
    pass

class PedidoService:
    def __init__(self):
        self._pedidos = PedidoRepository()
        self._estoque = EstoqueRepository()

    def criar_pedido(self, clienteId, itens):
        if not clienteId or not isinstance(itens, list) or len(itens) == 0:
            raise ErroValidacao("clienteId e itens são obrigatórios.")

        for item in itens:
            if self._estoque.disponivel(item["sku"]) < item["quantidade"]:
                raise EstoqueInsuficiente(f"Estoque insuficiente para {item['sku']}.")

        total = sum(item["precoUnitario"] * item["quantidade"] for item in itens)

        if not total > 0:
            raise PagamentoRecusado("Pagamento recusado.")

        for item in itens:
            self._estoque.baixar(item["sku"], item["quantidade"])

        return self._pedidos.salvar(clienteId, itens, total)

    def buscar_pedido(self, pedido_id):
        return self._pedidos.buscar_por_id(pedido_id)

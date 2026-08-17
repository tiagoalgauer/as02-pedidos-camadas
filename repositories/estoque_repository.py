class EstoqueRepository:
    def __init__(self):
        self._estoque = {"teclado-mecanico": 42, "mouse-gamer": 15, "monitor-4k": 3}

    def disponivel(self, sku):
        return self._estoque.get(sku, 0)

    def baixar(self, sku, quantidade):
        self._estoque[sku] = self.disponivel(sku) - quantidade

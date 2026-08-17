from flask import jsonify, request

from services.pedido_service import (
    ErroValidacao,
    EstoqueInsuficiente,
    PagamentoRecusado,
    PedidoService,
)


class PedidosRoutes:
    """Controller do recurso /pedidos.

    Não contém regra de negócio: recebe a requisição, chama o
    PedidoService e converte o resultado (ou a exceção) no status
    HTTP correspondente — exatamente o papel da camada de
    apresentação no estilo em camadas.

    COMPARAÇÃO ATAM (tabela da Figura 5, monolítico -> camadas):
    O QUE MELHOROU: a manutenibilidade — no monólito validação,
    estoque, total, cobrança e persistência viviam misturados em uma
    única rota, e agora cada responsabilidade tem um lugar óbvio
    (routes/ services/ repositories/), então "fácil localizar onde
    mudar" deixou de ser opinião e virou estrutura; a testabilidade
    também melhorou, porque a regra de negócio (PedidoService) é
    testável sem subir HTTP; e a curva de aprendizado do time segue
    baixa, pois continua um único processo, sem rede nem orquestração.
    O QUE PASSOU A CUSTAR MAIS CARO: a leitura de um fluxo simples —
    o que era 1 arquivo virou 6, e seguir um pedido agora atravessa
    três camadas (indireção); e os atributos de execução NÃO
    melhoraram: continua deploy único (deploy independente: não) e
    escalabilidade baixa-média, porque escalar qualquer camada ainda
    escala o processo inteiro — camadas compram organização, não
    escala.
    """

    def __init__(self, app):
        self._service = PedidoService()
        app.add_url_rule("/pedidos", view_func=self.criar, methods=["POST"])
        app.add_url_rule("/pedidos/<int:pedido_id>", view_func=self.buscar, methods=["GET"])

    def criar(self):
        dados = request.get_json(silent=True) or {}
        try:
            pedido = self._service.criar_pedido(dados.get("clienteId"), dados.get("itens"))
        except ErroValidacao as e:
            return jsonify({"erro": str(e)}), 400
        except EstoqueInsuficiente as e:
            return jsonify({"erro": str(e)}), 409
        except PagamentoRecusado as e:
            return jsonify({"erro": str(e)}), 402
        return jsonify(pedido), 201

    def buscar(self, pedido_id):
        pedido = self._service.buscar_pedido(pedido_id)
        if pedido is None:
            return jsonify({"erro": "Pedido não encontrado."}), 404
        return jsonify(pedido)

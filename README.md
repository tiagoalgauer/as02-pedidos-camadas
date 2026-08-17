# Exercício 2 — Aula 02: Refatoração Monolito → Camadas

Serviço de Pedidos refatorado do estilo **monolítico** (`monolito-original/pedidos-monolito.js`, single-file em Node/Express) para o estilo **em camadas (n-tier)** em **Python/Flask**.

## Estrutura

```
app.py                              # ponto de entrada (cria o Flask e registra as rotas)
routes/pedidos_routes.py            # APRESENTAÇÃO: controller, traduz HTTP <-> serviço
services/pedido_service.py          # NEGÓCIO: validação, estoque, total, cobrança
repositories/pedido_repository.py   # DADOS: pedidos em memória
repositories/estoque_repository.py  # DADOS: estoque em memória
test_pedidos.py                     # cobre 201, 400, 409 e 404 (mesmo comportamento do monólito)
monolito-original/                  # código de partida fornecido em aula
```

## Como executar

```bash
pip install flask
python app.py            # sobe na porta 3001, mesmas rotas do monólito
python test_pedidos.py   # ou: pytest
```

`POST /pedidos` (body: `{clienteId, itens: [{sku, quantidade, precoUnitario}]}`) e `GET /pedidos/<id>`.

## Comparação ATAM (tabela da Figura 5 da aula)

**O que melhorou:** a **manutenibilidade** — no monólito validação, estoque, total, cobrança e persistência viviam misturados em uma única rota; agora cada responsabilidade tem um lugar óbvio (routes/ services/ repositories/), então "fácil localizar onde mudar" deixou de ser opinião e virou estrutura. A **testabilidade** também melhorou, porque a regra de negócio (`PedidoService`) é testável sem subir HTTP. E a **curva de aprendizado do time segue baixa**: continua um único processo, sem rede nem orquestração.

**O que passou a custar mais caro:** a leitura de um fluxo simples — o que era 1 arquivo virou 6, e seguir um pedido agora atravessa três camadas (indireção). E os atributos de execução **não** melhoraram: continua **deploy único** (deploy independente: não) e **escalabilidade baixa-média**, porque escalar qualquer camada ainda escala o processo inteiro — camadas compram organização, não escala.

*(O mesmo parágrafo está nos comentários da classe `PedidosRoutes`, conforme pedido no enunciado.)*

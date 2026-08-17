/**
 * pedidos-monolito.js
 * -------------------------------------------------------------
 * Ponto de partida do Exercício 2 da Aula 02 (Estilos Arquiteturais).
 *
 * Serviço de Pedidos no estilo MONOLÍTICO: uma única rota Express
 * mistura validação, verificação de estoque, cálculo de total e
 * cobrança. É o MESMO sistema usado nos quatro diagramas C4 vistos
 * em aula (monolítico, camadas, microsserviços, event-driven).
 *
 * Tarefa do aluno: refatorar este arquivo para o ESTILO EM CAMADAS
 * (n-tier), separando em módulos routes/ services/ repositories/,
 * conforme o Exercício 2 do roteiro.
 *
 * Como executar:
 *   npm init -y && npm install express
 *   node pedidos-monolito.js
 * -------------------------------------------------------------
 */

const express = require('express');
const app = express();
app.use(express.json());

const pedidos = [];
const estoque = { 'teclado-mecanico': 42, 'mouse-gamer': 15, 'monitor-4k': 3 };
let proximoId = 1;

app.post('/pedidos', (req, res) => {
  const { clienteId, itens } = req.body;

  // validação misturada com a rota
  if (!clienteId || !Array.isArray(itens) || itens.length === 0) {
    return res.status(400).json({ erro: 'clienteId e itens são obrigatórios.' });
  }

  // verificação de estoque misturada com a rota
  for (const item of itens) {
    const disponivel = estoque[item.sku] ?? 0;
    if (disponivel < item.quantidade) {
      return res.status(409).json({ erro: `Estoque insuficiente para ${item.sku}.` });
    }
  }

  // cálculo de total misturado com a rota
  const total = itens.reduce((soma, item) => soma + item.precoUnitario * item.quantidade, 0);

  // baixa de estoque misturada com a rota
  for (const item of itens) {
    estoque[item.sku] -= item.quantidade;
  }

  // "cobrança" simulada, direto na rota
  const pagamentoAprovado = total > 0;
  if (!pagamentoAprovado) {
    return res.status(402).json({ erro: 'Pagamento recusado.' });
  }

  const pedido = { id: proximoId++, clienteId, itens, total, status: 'confirmado' };
  pedidos.push(pedido);
  return res.status(201).json(pedido);
});

app.get('/pedidos/:id', (req, res) => {
  const pedido = pedidos.find(p => p.id === Number(req.params.id));
  if (!pedido) return res.status(404).json({ erro: 'Pedido não encontrado.' });
  return res.json(pedido);
});

const PORTA = 3001;
app.listen(PORTA, () => console.log(`pedidos-monolito rodando na porta ${PORTA}`));

module.exports = app;

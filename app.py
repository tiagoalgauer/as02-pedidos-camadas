from flask import Flask

from routes.pedidos_routes import PedidosRoutes

app = Flask(__name__)
PedidosRoutes(app)

if __name__ == "__main__":
    PORTA = 3001
    print(f"pedidos-camadas rodando na porta {PORTA}")
    app.run(port=PORTA)

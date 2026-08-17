from app import app

def cliente():
    return app.test_client()

def test_fluxo_completo():
    c = cliente()

    r = c.post("/pedidos", json={
        "clienteId": "ana",
        "itens": [{"sku": "monitor-4k", "quantidade": 2, "precoUnitario": 1500}],
    })
    assert r.status_code == 201
    assert r.get_json()["total"] == 3000
    assert r.get_json()["status"] == "confirmado"

    r2 = c.get(f"/pedidos/{r.get_json()['id']}")
    assert r2.status_code == 200

    assert c.post("/pedidos", json={"itens": []}).status_code == 400

    r3 = c.post("/pedidos", json={
        "clienteId": "bia",
        "itens": [{"sku": "monitor-4k", "quantidade": 2, "precoUnitario": 1500}],
    })
    assert r3.status_code == 409

    assert c.get("/pedidos/999").status_code == 404

if __name__ == "__main__":
    test_fluxo_completo()
    print("ok — todos os cenários passaram")

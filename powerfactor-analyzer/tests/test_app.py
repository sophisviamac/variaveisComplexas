from app import app


def test_dashboard_oferece_cenarios_e_grafico_de_fasores():
    response = app.test_client().get("/")
    pagina = response.get_data(as_text=True)
    assert response.status_code == 200
    assert all(nome in pagina for nome in ("Motor de esteira", "Conjunto de bombas", "Ventiladores industriais"))
    assert 'id="corrente-antes-vetor"' in pagina


def test_endpoint_aceita_entrada_manual_e_retorna_fasores():
    cliente = app.test_client()
    response = cliente.post("/api/analisar", json={"p_kw": "10", "q_kvar": "7.5", "fp_desejado": "0.95"})
    assert response.status_code == 200
    assert response.json["fp_atual"] == 0.8
    assert response.json["fp_novo"] == 0.95
    assert response.json["fasores"]["antes"]["angulo_graus"] < 0

    invalida = cliente.post("/api/analisar", json={"p_kw": 10, "q_kvar": -1, "fp_desejado": 0.95})
    assert invalida.status_code == 400
    assert "error" in invalida.json

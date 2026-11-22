import pytest

from calculos import calcular_analise, ErroEntrada


def test_caso_academico_padrao():
    resultado = calcular_analise(10, 7.5, 0.95)

    assert resultado["potencia_complexa"]["retangular"].startswith("10.0000")
    assert resultado["potencia_aparente_kva"] == pytest.approx(12.5, abs=0.01)
    assert resultado["angulo_graus"] == pytest.approx(36.87, abs=0.01)
    assert resultado["fp_atual"] == pytest.approx(0.80, abs=0.01)
    assert resultado["qc_kvar"] == pytest.approx(4.21, abs=0.01)
    assert resultado["potencia_aparente_nova_kva"] == pytest.approx(10.53, abs=0.01)
    assert resultado["fp_novo"] == pytest.approx(0.95, abs=0.01)


def test_instalacao_ja_atende_meta():
    resultado = calcular_analise(10, 2, 0.95)

    assert resultado["atende_meta"] is True
    assert resultado["qc_kvar"] == 0
    assert resultado["q_novo_kvar"] == 2
    assert resultado["fasores"]["antes"] == resultado["fasores"]["depois"]


@pytest.mark.parametrize(("p", "q", "meta"), [(10, 7.5, 0.95), (45, 33, 0.95), (24, 6, 0.95), (10, 7.5, 1), (10, 0, 1)])
def test_fasores_recompoem_potencia_antes_e_depois(p, q, meta):
    resultado = calcular_analise(p, q, meta)
    fasores = resultado["fasores"]
    tensao_kv = fasores["tensao_rms_v"] / 1000

    for nome, triangulo in zip(("antes", "depois"), resultado["triangulos"]):
        estado = fasores[nome]
        corrente = complex(estado["corrente_real_a"], estado["corrente_imaginaria_a"])
        potencia = tensao_kv * corrente.conjugate()
        assert potencia == pytest.approx(complex(p, triangulo[2]["y"]))
        assert potencia.real == pytest.approx(estado["potencia_recomposta_kw"])
        assert potencia.imag == pytest.approx(estado["potencia_recomposta_kvar"])
        assert abs(corrente) == pytest.approx(estado["corrente_rms_a"])
        assert estado["angulo_graus"] <= 0
        assert estado["vetor"]["y"] >= 0

    assert fasores["antes"]["corrente_rms_a"] >= fasores["depois"]["corrente_rms_a"]
    assert resultado["fp_novo"] >= meta
    assert resultado["qc_kvar"] == pytest.approx(q - resultado["triangulos"][1][2]["y"], abs=0.0001)


def test_meta_unitaria_com_carga_fortemente_indutiva():
    resultado = calcular_analise(1, 1e20, 1)
    assert resultado["qc_kvar"] == 1e20
    assert resultado["q_novo_kvar"] == 0
    assert resultado["fasores"]["depois"]["corrente_imaginaria_a"] == 0


@pytest.mark.parametrize(
    ("p", "q", "meta"),
    [
        (0, 5, 0.95),
        (-10, 5, 0.95),
        (10, -1, 0.95),
        (10, 5, 0),
        (10, 5, 1.1),
    ],
)
def test_entradas_invalidas(p, q, meta):
    with pytest.raises(ErroEntrada):
        calcular_analise(p, q, meta)

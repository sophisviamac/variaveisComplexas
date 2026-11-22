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

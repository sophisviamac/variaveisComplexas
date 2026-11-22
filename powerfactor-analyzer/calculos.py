import cmath
import math

TENSAO_RMS_V = 230


class ErroEntrada(ValueError):
    pass


def _numero(valor, nome):
    if isinstance(valor, bool):
        raise ErroEntrada(f"{nome} deve ser um número válido.")
    try:
        numero = float(valor)
    except (TypeError, ValueError, OverflowError):
        raise ErroEntrada(f"{nome} deve ser um número válido.")
    if not math.isfinite(numero):
        raise ErroEntrada(f"{nome} deve ser um número finito.")
    return numero


def _fasores(s_atual, s_novo):
    # Modelo equivalente: kVA / kV fornece A. V é a referência real.
    tensao_kv = TENSAO_RMS_V / 1000
    modulo_atual = abs(s_atual)
    if not math.isfinite(modulo_atual / tensao_kv):
        raise ErroEntrada("As potências excedem o intervalo numérico da simulação.")

    def estado(s):
        corrente = (s / tensao_kv).conjugate()
        # Mesma base de corrente antes e depois. A tensão tem base própria.
        vetor = (s / modulo_atual).conjugate()
        recomposicao = tensao_kv * corrente.conjugate()
        theta = cmath.phase(s)
        raio = 0.29
        return {
            "corrente_rms_a": abs(corrente),
            "corrente_real_a": corrente.real,
            "corrente_imaginaria_a": corrente.imag,
            "angulo_graus": -math.degrees(theta) if theta else 0.0,
            "vetor": {"x": vetor.real, "y": -vetor.imag},
            "arco": {"x": raio * math.cos(theta), "y": raio * math.sin(theta)},
            "potencia_recomposta_kw": recomposicao.real,
            "potencia_recomposta_kvar": recomposicao.imag,
        }

    return {"tensao_rms_v": TENSAO_RMS_V, "antes": estado(s_atual), "depois": estado(s_novo)}


def calcular_analise(p_kw, q_kvar, fp_desejado):
    p = _numero(p_kw, "A potência ativa")
    q = _numero(q_kvar, "A potência reativa")
    meta = _numero(fp_desejado, "O fator de potência desejado")

    if p <= 0:
        raise ErroEntrada("A potência ativa deve ser maior que zero.")
    if q < 0:
        raise ErroEntrada("A potência reativa indutiva não pode ser negativa.")
    if not 0 < meta <= 1:
        raise ErroEntrada("O fator de potência desejado deve ser maior que zero e menor ou igual a 1.")

    # S = P + jQ: a parte real representa kW e a imaginaria representa kVAr.
    s_atual = complex(p, q)
    aparente_atual = abs(s_atual)
    if not math.isfinite(aparente_atual):
        raise ErroEntrada("As potências excedem o intervalo numérico da simulação.")
    theta_atual = cmath.phase(s_atual)
    fp_atual = p / aparente_atual if aparente_atual else 0.0

    # Quando a carga ja atende a meta, nao ha necessidade de compensacao.
    if fp_atual >= meta:
        qc = 0.0
        q_novo = q
        atende_meta = True
    else:
        theta_desejado = math.acos(meta)
        q_novo = min(q, p * math.tan(theta_desejado))
        qc = q - q_novo
        atende_meta = False

    s_novo = complex(p, q_novo)
    aparente_novo = abs(s_novo)
    theta_novo = cmath.phase(s_novo)
    fp_novo = p / aparente_novo if aparente_novo else 0.0

    def polar(s):
        modulo = abs(s)
        argumento = cmath.phase(s)
        return {
            "retangular": f"{s.real:.4f} {s.imag:+.4f}j kVA",
            "modulo_kva": round(modulo, 4),
            "argumento_rad": round(argumento, 6),
            "argumento_graus": round(math.degrees(argumento), 4),
        }

    return {
        "entrada": {
            "p_kw": round(p, 6),
            "q_kvar": round(q, 6),
            "fp_desejado": round(meta, 6),
        },
        "potencia_complexa": polar(s_atual),
        "potencia_aparente_kva": round(aparente_atual, 4),
        "angulo_graus": round(math.degrees(theta_atual), 4),
        "angulo_rad": round(theta_atual, 6),
        "fp_atual": round(fp_atual, 6),
        "fp_novo": round(min(1.0, fp_novo), 6),
        "qc_kvar": round(qc, 4),
        "q_novo_kvar": round(q_novo, 4),
        "potencia_complexa_nova": polar(s_novo),
        "potencia_aparente_nova_kva": round(aparente_novo, 4),
        "angulo_novo_graus": round(math.degrees(theta_novo), 4),
        "atende_meta": atende_meta,
        "fasores": _fasores(s_atual, s_novo),
        "triangulos": [
            [{"x": 0, "y": 0}, {"x": p, "y": 0}, {"x": p, "y": reativa}, {"x": 0, "y": 0}]
            for reativa in (q, q_novo)
        ],
        "diagnostico": (
            "A carga simulada já atende à meta de fator de potência. A compensação estimada é zero."
            if atende_meta
            else "O fator de potência da carga simulada está abaixo da meta. O painel mostra a compensação capacitiva estimada."
        ),
    }

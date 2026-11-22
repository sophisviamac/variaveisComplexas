import cmath
import math


class ErroEntrada(ValueError):
    pass


def _numero(valor, nome):
    if isinstance(valor, bool):
        raise ErroEntrada(f"{nome} deve ser um numero valido.")
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise ErroEntrada(f"{nome} deve ser um numero valido.")
    if not math.isfinite(numero):
        raise ErroEntrada(f"{nome} deve ser um numero finito.")
    return numero


def calcular_analise(p_kw, q_kvar, fp_desejado):
    p = _numero(p_kw, "A potencia ativa")
    q = _numero(q_kvar, "A potencia reativa")
    meta = _numero(fp_desejado, "O fator de potencia desejado")

    if p <= 0:
        raise ErroEntrada("A potencia ativa deve ser maior que zero.")
    if q < 0:
        raise ErroEntrada("A potencia reativa indutiva nao pode ser negativa.")
    if not 0 < meta <= 1:
        raise ErroEntrada("O fator de potencia desejado deve estar entre 0 e 1.")

    # S = P + jQ: a parte real representa kW e a imaginaria representa kVAr.
    s_atual = complex(p, q)
    aparente_atual = abs(s_atual)
    theta_atual = cmath.phase(s_atual)
    fp_atual = p / aparente_atual if aparente_atual else 0.0

    # Quando a carga ja atende a meta, nao ha necessidade de compensacao.
    if fp_atual >= meta:
        qc = 0.0
        atende_meta = True
    else:
        theta_desejado = math.acos(meta)
        qc = p * (math.tan(theta_atual) - math.tan(theta_desejado))
        qc = max(0.0, qc)
        atende_meta = False

    q_novo = max(0.0, q - qc)
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
        "diagnostico": (
            "O fator de potencia atual ja atende a meta definida."
            if atende_meta
            else "O fator de potencia atual esta abaixo da meta definida."
        ),
    }

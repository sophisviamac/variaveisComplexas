from flask import Flask, render_template, request, jsonify

from calculos import calcular_analise, ErroEntrada, TENSAO_RMS_V


app = Flask(__name__)

cenarios = (
    {"nome": "Motor de esteira", "p_kw": 10, "q_kvar": 7.5, "fp_desejado": 0.95},
    {"nome": "Conjunto de bombas", "p_kw": 45, "q_kvar": 33, "fp_desejado": 0.95},
    {"nome": "Ventiladores industriais", "p_kw": 24, "q_kvar": 6, "fp_desejado": 0.95},
)


@app.route("/")
def index():
    return render_template("index.html", cenarios=cenarios, inicial=cenarios[0], tensao_rms_v=TENSAO_RMS_V)


@app.route("/api/analisar", methods=["POST"])
def analisar():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"error": "Envie os dados em formato JSON."}), 400

    try:
        resultado = calcular_analise(
            dados.get("p_kw"),
            dados.get("q_kvar"),
            dados.get("fp_desejado"),
        )
        return jsonify(resultado)
    except ErroEntrada as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True)

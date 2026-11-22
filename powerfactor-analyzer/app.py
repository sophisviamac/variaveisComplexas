from flask import Flask, render_template, request, jsonify

from calculos import calcular_analise, ErroEntrada


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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

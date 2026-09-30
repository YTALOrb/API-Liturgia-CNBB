from flask import Flask, request, jsonify
from scraping import getReturnLiturgia
import os
import traceback

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, Origin"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "api": "API Liturgia CNBB",
        "endpoints": {"liturgia": "/api/liturgia"}
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/liturgia", methods=["GET", "POST", "OPTIONS"])
def get_liturgia():

    if request.method == "OPTIONS":
        return ("", 204)

    if request.method == "POST":
        if not request.is_json:
            return jsonify({"erro": "O Content-Type precisa ser application/json."}), 400
        try:
            content = request.get_json()
            ano = int(content["ano"])
            mes = int(content["mes"])
            dia = int(content["dia"])
        except (TypeError, ValueError, KeyError):
            return jsonify({
                "erro": "Envie ano, mes e dia corretamente.",
                "exemplo": {"ano": 2026, "mes": 9, "dia": 30}
            }), 400
        try:
            print(f"[LITURGIA] Buscando: {ano:04d}-{mes:02d}-{dia:02d}")
            resultado = getReturnLiturgia(
                parametros={"ano": ano, "mes": mes, "dia": dia}
            )
            return jsonify({"Liturgia": resultado})
        except Exception as e:
            print("\n========== ERRO POST ==========")
            print(str(e))
            traceback.print_exc()
            print("===============================\n")
            return jsonify({"erro": "Erro ao buscar a liturgia.", "detalhes": str(e)}), 500

    try:
        print("[LITURGIA] Buscando liturgia de hoje...")
        resultado = getReturnLiturgia()
        return jsonify({"Liturgia": resultado})
    except Exception as e:
        print("\n========== ERRO GET ==========")
        print(str(e))
        traceback.print_exc()
        print("==============================\n")
        return jsonify({"erro": "Erro ao buscar a liturgia.", "detalhes": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

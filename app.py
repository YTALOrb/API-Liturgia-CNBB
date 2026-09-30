from flask import Flask, request, jsonify
from scraping import getReturnLiturgia
import os
import traceback

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "api": "API Liturgia CNBB",
        "endpoints": {
            "liturgia": "/api/liturgia"
        }
    })


@app.route("/api/liturgia", methods=["GET", "POST"])
def get_liturgia():

    # =====================================================
    # POST - data específica
    # =====================================================

    if request.method == "POST":

        if not request.is_json:
            return jsonify({
                "erro": "O Content-Type precisa ser application/json."
            }), 400

        try:
            content = request.get_json()

            ano = int(content["ano"])
            mes = int(content["mes"])
            dia = int(content["dia"])

        except (TypeError, ValueError, KeyError):
            return jsonify({
                "erro": "Envie ano, mes e dia corretamente.",
                "exemplo": {
                    "ano": 2026,
                    "mes": 9,
                    "dia": 30
                }
            }), 400

        try:
            print(
                f"[LITURGIA] Buscando: "
                f"{ano:04d}-{mes:02d}-{dia:02d}"
            )

            resultado = getReturnLiturgia(
                parametros={
                    "ano": ano,
                    "mes": mes,
                    "dia": dia
                }
            )

            return jsonify({
                "Liturgia": resultado
            })

        except Exception as e:

            print("\n========== ERRO POST ==========")
            print(str(e))
            traceback.print_exc()
            print("===============================\n")

            return jsonify({
                "erro": "Erro ao buscar a liturgia.",
                "detalhes": str(e)
            }), 500

    # =====================================================
    # GET - hoje
    # =====================================================

    try:

        print("[LITURGIA] Buscando liturgia de hoje...")

        resultado = getReturnLiturgia()

        return jsonify({
            "Liturgia": resultado
        })

    except Exception as e:

        print("\n========== ERRO GET ==========")
        print(str(e))
        traceback.print_exc()
        print("==============================\n")

        return jsonify({
            "erro": "Erro ao buscar a liturgia.",
            "detalhes": str(e)
        }), 500


# =========================================================
# DESENVOLVIMENTO LOCAL
# =========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )

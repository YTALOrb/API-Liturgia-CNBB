from flask import Flask, request, jsonify
from scraping import *

import os


app = Flask(__name__)

# Erro para Content-Type incorreto
jsontypeerror = {
    "dados": [
        {
            "Message": "Invalid content-type. Must be application/json."
        }
    ]
}


@app.route('/api/liturgia', methods=['GET', 'POST'])
def getLiturgia():

    # POST = buscar liturgia de uma data específica
    if request.method == 'POST':

        # Verifica se o conteúdo é JSON
        if request.content_type != 'application/json':
            return jsonify(jsontypeerror), 400

        try:
            content = request.get_json()

            ano = int(content['ano'])
            mes = int(content['mes'])
            dia = int(content['dia'])

        except (TypeError, ValueError, KeyError):
            return jsonify({
                "erro": "Envie ano, mes e dia corretamente."
            }), 400

        try:
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
            return jsonify({
                "erro": "Erro ao buscar a liturgia.",
                "detalhes": str(e)
            }), 500

    # GET = liturgia do dia
    try:
        resultado = getReturnLiturgia()

        return jsonify({
            "Liturgia": resultado
        })

    except Exception as e:
        return jsonify({
            "erro": "Erro ao buscar a liturgia.",
            "detalhes": str(e)
        }), 500


# Configuração para hospedagem
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )
```

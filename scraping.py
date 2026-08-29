import requests


API_URL = "https://api-liturgia-diaria.vercel.app/"


def getReturnLiturgia(**kwargs):
    """
    Busca a liturgia diária através da API externa.

    Sem parâmetros:
        retorna a liturgia de hoje.

    Com parâmetros:
        parametros={
            "ano": 2026,
            "mes": 8,
            "dia": 29
        }
    """

    parametros = kwargs.get("parametros")

    try:

        # ---------------------------------------------------------
        # Buscar uma data específica
        # ---------------------------------------------------------
        if parametros:

            ano = int(parametros["ano"])
            mes = int(parametros["mes"])
            dia = int(parametros["dia"])

            data = f"{ano:04d}-{mes:02d}-{dia:02d}"

            response = requests.get(
                API_URL,
                params={
                    "date": data
                },
                timeout=30
            )

        # ---------------------------------------------------------
        # Buscar liturgia de hoje
        # ---------------------------------------------------------
        else:

            response = requests.get(
                API_URL,
                timeout=30
            )

        response.raise_for_status()

        dados = response.json()

        return dados

    except requests.exceptions.Timeout:
        raise Exception(
            "A API de liturgia demorou muito para responder."
        )

    except requests.exceptions.ConnectionError as e:
        raise Exception(
            f"Não foi possível conectar à API de liturgia: {str(e)}"
        )

    except requests.exceptions.HTTPError as e:
        raise Exception(
            f"A API de liturgia retornou um erro HTTP: {str(e)}"
        )

    except requests.exceptions.JSONDecodeError:
        raise Exception(
            "A API de liturgia retornou uma resposta que não é JSON."
        )

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Erro ao consultar a API de liturgia: {str(e)}"
        )

    except Exception as e:
        raise Exception(
            f"Erro ao obter a liturgia: {str(e)}"
        )

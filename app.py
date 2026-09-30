import requests


# =============================================================
# CONFIGURAÇÃO
# =============================================================

API_URL = "https://api-liturgia-diaria.vercel.app/"

TIMEOUT = 30


# =============================================================
# FUNÇÃO PRINCIPAL
# =============================================================

def getReturnLiturgia(**kwargs):

    """
    Busca a liturgia através da API externa.

    Sem parâmetros:
        Busca a liturgia de hoje.

    Com parâmetros:

        parametros={
            "ano": 2026,
            "mes": 9,
            "dia": 30
        }

    """

    parametros = kwargs.get("parametros")

    try:

        # =====================================================
        # DATA ESPECÍFICA
        # =====================================================

        if parametros:

            ano = int(parametros["ano"])
            mes = int(parametros["mes"])
            dia = int(parametros["dia"])

            data = f"{ano:04d}-{mes:02d}-{dia:02d}"

            print(
                f"[SCRAPING] Buscando liturgia da data: {data}"
            )

            response = requests.get(
                API_URL,
                params={
                    "date": data
                },
                timeout=TIMEOUT
            )

        # =====================================================
        # LITURGIA DE HOJE
        # =====================================================

        else:

            print(
                "[SCRAPING] Buscando liturgia de hoje..."
            )

            response = requests.get(
                API_URL,
                timeout=TIMEOUT
            )

        # =====================================================
        # INFORMAÇÕES DA RESPOSTA
        # =====================================================

        print(
            f"[SCRAPING] Status HTTP: {response.status_code}"
        )

        print(
            f"[SCRAPING] URL final: {response.url}"
        )

        print(
            f"[SCRAPING] Content-Type: "
            f"{response.headers.get('Content-Type')}"
        )

        # =====================================================
        # ERRO HTTP
        # =====================================================

        if response.status_code != 200:

            resposta = response.text[:1000]

            print(
                "[SCRAPING] API externa retornou erro:"
            )

            print(resposta)

            raise Exception(
                f"API externa retornou HTTP "
                f"{response.status_code}. "
                f"Resposta: {resposta}"
            )

        # =====================================================
        # CONVERTER PARA JSON
        # =====================================================

        try:

            dados = response.json()

        except ValueError:

            resposta = response.text[:1000]

            print(
                "[SCRAPING] Resposta não é JSON:"
            )

            print(resposta)

            raise Exception(
                "A API externa não retornou JSON. "
                f"Resposta: {resposta}"
            )

        # =====================================================
        # SUCESSO
        # =====================================================

        print(
            "[SCRAPING] Liturgia recebida com sucesso."
        )

        return dados

    # =========================================================
    # TIMEOUT
    # =========================================================

    except requests.exceptions.Timeout:

        raise Exception(
            "A API externa demorou mais de "
            f"{TIMEOUT} segundos para responder."
        )

    # =========================================================
    # ERRO DE CONEXÃO
    # =========================================================

    except requests.exceptions.ConnectionError as e:

        raise Exception(
            "Não foi possível conectar à API externa. "
            f"Detalhes: {e}"
        )

    # =========================================================
    # ERRO HTTP
    # =========================================================

    except requests.exceptions.HTTPError as e:

        raise Exception(
            f"Erro HTTP ao consultar a API externa: {e}"
        )

    # =========================================================
    # OUTROS ERROS
    # =========================================================

    except Exception as e:

        raise Exception(
            f"Erro ao obter a liturgia: {e}"
        )

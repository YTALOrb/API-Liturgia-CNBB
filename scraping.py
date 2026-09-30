import requests


# =========================================================
# API OFICIAL DO NOSSO BACKEND
# =========================================================

API_URL = "https://liturgia.up.railway.app/v2/"

TIMEOUT = 30


# =========================================================
# BUSCAR LITURGIA
# =========================================================

def getReturnLiturgia(**kwargs):

    parametros = kwargs.get("parametros")

    try:

        # =====================================================
        # DATA ESPECÍFICA
        # =====================================================

        if parametros:

            ano = int(parametros["ano"])
            mes = int(parametros["mes"])
            dia = int(parametros["dia"])

            print(
                f"[LITURGIA] Buscando data: "
                f"{dia:02d}/{mes:02d}/{ano}"
            )

            response = requests.get(
                API_URL,
                params={
                    "dia": dia,
                    "mes": mes,
                    "ano": ano
                },
                timeout=TIMEOUT
            )

        # =====================================================
        # LITURGIA DE HOJE
        # =====================================================

        else:

            print("[LITURGIA] Buscando liturgia de hoje...")

            response = requests.get(
                API_URL,
                timeout=TIMEOUT
            )

        # =====================================================
        # DEBUG
        # =====================================================

        print(
            f"[LITURGIA] URL consultada: {response.url}"
        )

        print(
            f"[LITURGIA] Status HTTP: "
            f"{response.status_code}"
        )

        print(
            f"[LITURGIA] Content-Type: "
            f"{response.headers.get('Content-Type')}"
        )

        # =====================================================
        # ERRO HTTP
        # =====================================================

        if response.status_code != 200:

            print(
                "[LITURGIA] Resposta da API:"
            )

            print(response.text[:1000])

            raise Exception(
                f"A API de liturgia retornou HTTP "
                f"{response.status_code}."
            )

        # =====================================================
        # JSON
        # =====================================================

        try:

            dados = response.json()

        except ValueError:

            print(
                "[LITURGIA] A resposta não é JSON:"
            )

            print(response.text[:1000])

            raise Exception(
                "A API de liturgia retornou "
                "uma resposta que não é JSON."
            )

        # =====================================================
        # SUCESSO
        # =====================================================

        print(
            "[LITURGIA] Liturgia recebida com sucesso!"
        )

        return dados

    # =========================================================
    # TIMEOUT
    # =========================================================

    except requests.exceptions.Timeout:

        raise Exception(
            "A API de liturgia demorou mais de "
            f"{TIMEOUT} segundos para responder."
        )

    # =========================================================
    # CONEXÃO
    # =========================================================

    except requests.exceptions.ConnectionError as e:

        raise Exception(
            "Não foi possível conectar à API de liturgia. "
            f"Detalhes: {e}"
        )

    # =========================================================
    # REQUEST
    # =========================================================

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"Erro ao consultar a API de liturgia: {e}"
        )

    # =========================================================
    # ERRO GERAL
    # =========================================================

    except Exception as e:

        raise Exception(
            f"Erro ao obter a liturgia: {e}"
        )

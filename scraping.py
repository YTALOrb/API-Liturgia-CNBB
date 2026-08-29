import requests
from bs4 import BeautifulSoup
from urllib import parse as urlDict


URL = "https://liturgiadiaria.cnbb.org.br/app/user/user/UserView.php"


def _parser_data(response):
    soup = BeautifulSoup(response.text, "html.parser")

    post = soup.find_all("div", class_="blog-post")

    leitura = ""

    for item in post:
        leitura += item.get_text()

    return [
        texto.replace("\n", "").replace("\t", "")
        for texto in leitura.split("\n\n\n\n\t\t\t\t\t\t\t\t")
    ]


def _fazer_requisicao(parametros=None):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }

    try:
        if parametros:
            url = URL + "?" + urlDict.urlencode(parametros)
        else:
            url = URL

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response

    except requests.exceptions.SSLError as e:
        raise Exception(
            "O servidor da CNBB recusou a conexão SSL. "
            f"Detalhes: {str(e)}"
        )

    except requests.exceptions.Timeout:
        raise Exception(
            "O servidor da CNBB demorou muito para responder."
        )

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Erro ao acessar a fonte da liturgia: {str(e)}"
        )


def getReturnLiturgia(**kwargs):

    parametros = kwargs.get("parametros")

    response = _fazer_requisicao(parametros)

    return _parser_data(response)

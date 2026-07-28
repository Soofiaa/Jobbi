import pytest

from utils.portal_detector import PORTALES, detectar_portal


@pytest.mark.parametrize("dominio,nombre", PORTALES.items())
def test_detecta_cada_portal_reconocido(dominio, nombre):
    url = f"https://www.{dominio}/aviso/12345"
    assert detectar_portal(url) == nombre


def test_url_sin_protocolo_no_se_reconoce_actualmente():
    # Comportamiento actual: sin esquema, urlparse() interpreta todo como
    # path (netloc queda vacío), así que no matchea ningún portal y cae en
    # "Otro". Este test documenta el comportamiento real; si se decide
    # soportar URLs pegadas sin "https://", requiere un fix aparte en
    # utils/portal_detector.py (fuera del alcance de esta migración de tests).
    assert detectar_portal("www.linkedin.com/jobs/view/123456") == "Otro"


def test_dominio_no_reconocido_devuelve_otro():
    assert detectar_portal("https://www.unaempresa-random.cl/postula") == "Otro"


@pytest.mark.parametrize("url", ["", None])
def test_url_vacia_o_none_devuelve_string_vacio(url):
    assert detectar_portal(url) == ""


def test_url_malformada_no_lanza_excepcion():
    # urlparse lanza ValueError con URLs IPv6 mal formadas; detectar_portal
    # debe capturarla y devolver "Otro" en vez de propagar la excepción.
    assert detectar_portal("http://[::1") == "Otro"

import calendar
from datetime import date, datetime

from services.postulaciones import (
    crear_postulacion,
    editar_postulacion,
    eliminar_postulacion,
    obtener_postulaciones,
)


# ─────────────────────────────────────────
# crear_postulacion
# ─────────────────────────────────────────
def test_crear_postulacion_arma_el_payload_correcto(fake_client):
    query = fake_client(data=[{"id": 1, "puesto": "Analista", "empresa": "Acme"}])

    resultado = crear_postulacion(
        puesto="Analista",
        empresa="Acme",
        portal="LinkedIn",
        url="https://linkedin.com/jobs/1",
        descripcion="desc",
        estado="Postulado",
        notas="notas",
        fecha_postulacion="2026-01-15",
    )

    _, args, _ = query.llamada("insert")
    payload = args[0]
    assert payload == {
        "puesto": "Analista",
        "empresa": "Acme",
        "portal": "LinkedIn",
        "url": "https://linkedin.com/jobs/1",
        "descripcion": "desc",
        "estado": "Postulado",
        "notas": "notas",
        "fecha_postulacion": "2026-01-15",
    }


def test_crear_postulacion_usa_hoy_si_no_se_da_fecha(fake_client):
    query = fake_client(data=[{"id": 1}])
    crear_postulacion(puesto="Analista", empresa="Acme")
    _, args, _ = query.llamada("insert")
    assert args[0]["fecha_postulacion"] == str(date.today())


def test_crear_postulacion_devuelve_primer_elemento_de_response_data(fake_client):
    fake_client(data=[{"id": 1, "puesto": "A"}, {"id": 2, "puesto": "B"}])
    resultado = crear_postulacion(puesto="A", empresa="Acme")
    assert resultado == {"id": 1, "puesto": "A"}


def test_crear_postulacion_devuelve_none_si_no_hay_data(fake_client):
    fake_client(data=[])
    resultado = crear_postulacion(puesto="A", empresa="Acme")
    assert resultado is None


# ─────────────────────────────────────────
# obtener_postulaciones — filtros
# ─────────────────────────────────────────
def test_obtener_postulaciones_sin_filtros_no_llama_eq_ni_ilike(fake_client):
    query = fake_client(data=[])
    obtener_postulaciones()
    assert query.llamada("eq") is None
    assert query.llamada("ilike") is None
    assert query.llamada("gte") is None


def test_obtener_postulaciones_filtra_por_estado(fake_client):
    query = fake_client(data=[])
    obtener_postulaciones(filtro_estado="Entrevista")
    assert query.llamada("eq") == ("eq", ("estado", "Entrevista"), {})


def test_obtener_postulaciones_no_filtra_por_estado_todos(fake_client):
    query = fake_client(data=[])
    obtener_postulaciones(filtro_estado="Todos")
    assert query.llamada("eq") is None


def test_obtener_postulaciones_filtra_por_empresa_con_ilike(fake_client):
    query = fake_client(data=[])
    obtener_postulaciones(filtro_empresa="acme")
    assert query.llamada("ilike") == ("ilike", ("empresa", "%acme%"), {})


def test_obtener_postulaciones_filtra_por_mes_con_rango_de_fechas(fake_client):
    query = fake_client(data=[])
    obtener_postulaciones(filtro_mes="2026-02")

    ultimo_dia = calendar.monthrange(2026, 2)[1]
    assert query.llamada("gte") == ("gte", ("fecha_postulacion", "2026-02-01"), {})
    assert query.llamada("lte") == ("lte", ("fecha_postulacion", f"2026-02-{ultimo_dia}"), {})


def test_obtener_postulaciones_devuelve_data_o_lista_vacia(fake_client):
    fake_client(data=None)
    assert obtener_postulaciones() == []


# ─────────────────────────────────────────
# editar_postulacion — regresión bug fecha_actualizacion
# ─────────────────────────────────────────
def test_editar_postulacion_no_envia_now_como_string_literal(fake_client):
    query = fake_client(data=[{"id": 1}])
    editar_postulacion(id=1, puesto="A", empresa="Acme")

    _, args, _ = query.llamada("update")
    payload = args[0]
    valor = payload["fecha_actualizacion"]
    assert valor != "now()"
    # Debe ser un timestamp real y parseable, no un texto literal sin evaluar.
    datetime.fromisoformat(valor)


def test_editar_postulacion_devuelve_primer_elemento_de_response_data(fake_client):
    fake_client(data=[{"id": 1, "estado": "En proceso"}])
    resultado = editar_postulacion(id=1, puesto="A", empresa="Acme")
    assert resultado == {"id": 1, "estado": "En proceso"}


# ─────────────────────────────────────────
# eliminar_postulacion
# ─────────────────────────────────────────
def test_eliminar_postulacion_devuelve_true_si_hay_data(fake_client):
    fake_client(data=[{"id": 1}])
    assert eliminar_postulacion(1) is True


def test_eliminar_postulacion_devuelve_false_si_no_hay_data(fake_client):
    fake_client(data=[])
    assert eliminar_postulacion(1) is False

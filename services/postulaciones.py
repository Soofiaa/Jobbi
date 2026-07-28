from db.connection import get_client
from datetime import date, datetime, timezone

# ─────────────────────────────────────────
# CREAR una nueva postulación
# ─────────────────────────────────────────
def crear_postulacion(puesto: str, empresa: str, portal: str = None,
                      url: str = None, descripcion: str = None,
                      estado: str = "Postulado", notas: str = None,
                      fecha_postulacion: str = None) -> dict:
    client = get_client()
    data = {
        "puesto":             puesto,
        "empresa":            empresa,
        "portal":             portal,
        "url":                url,
        "descripcion":        descripcion,
        "estado":             estado,
        "notas":              notas,
        "fecha_postulacion":  fecha_postulacion or str(date.today())
    }
    response = client.table("postulaciones").insert(data).execute()
    return response.data[0] if response.data else None


# ─────────────────────────────────────────
# OBTENER todas las postulaciones
# ─────────────────────────────────────────
def obtener_postulaciones(filtro_estado: str = None,
                           filtro_empresa: str = None,
                           orden_desc: bool = False,
                           filtro_mes: str = None) -> list:
    client = get_client()
    query = client.table("postulaciones").select("*").order("fecha_postulacion", desc=orden_desc)

    if filtro_estado and filtro_estado != "Todos":
        query = query.eq("estado", filtro_estado)
    if filtro_empresa and filtro_empresa.strip() != "":
        query = query.ilike("empresa", f"%{filtro_empresa}%")
    if filtro_mes and filtro_mes != "Todos":
        anio, mes = filtro_mes.split("-")
        import calendar
        ultimo_dia = calendar.monthrange(int(anio), int(mes))[1]
        query = query.gte("fecha_postulacion", f"{anio}-{mes}-01")
        query = query.lte("fecha_postulacion", f"{anio}-{mes}-{ultimo_dia}")

    response = query.execute()
    return response.data or []


# ─────────────────────────────────────────
# OBTENER una postulación por ID
# ─────────────────────────────────────────
def obtener_postulacion_por_id(id: int) -> dict:
    client = get_client()
    response = client.table("postulaciones").select("*").eq("id", id).execute()
    return response.data[0] if response.data else None


# ─────────────────────────────────────────
# EDITAR una postulación existente
# ─────────────────────────────────────────
def editar_postulacion(id: int, puesto: str, empresa: str, portal: str = None,
                        url: str = None, descripcion: str = None,
                        estado: str = "Postulado", notas: str = None,
                        fecha_postulacion: str = None) -> dict:
    client = get_client()
    data = {
        "puesto":               puesto,
        "empresa":              empresa,
        "portal":               portal,
        "url":                  url,
        "descripcion":          descripcion,
        "estado":               estado,
        "notas":                notas,
        # Fix: "now()" se enviaba como texto literal, no como función SQL evaluada por Postgres.
        # No se confirmó un trigger de Postgres/Supabase que la calcule automáticamente,
        # así que se calcula acá.
        "fecha_actualizacion":  datetime.now(timezone.utc).isoformat(),
        "fecha_postulacion":    fecha_postulacion or str(date.today())
    }
    response = client.table("postulaciones").update(data).eq("id", id).execute()
    return response.data[0] if response.data else None


# ─────────────────────────────────────────
# ELIMINAR una postulación
# ─────────────────────────────────────────
def eliminar_postulacion(id: int) -> bool:
    client = get_client()
    response = client.table("postulaciones").delete().eq("id", id).execute()
    return True if response.data else False


# ─────────────────────────────────────────
# OBTENER lista de estados únicos (para filtros)
# ─────────────────────────────────────────
ESTADOS = [
    "Postulado",
    "En proceso",
    "Entrevista",
    "Oferta",
    "Descartado",
    "Rechazado"
]
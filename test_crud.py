from services.postulaciones import (
    crear_postulacion,
    obtener_postulaciones,
    editar_postulacion,
    eliminar_postulacion
)
from utils.portal_detector import detectar_portal

# 1. Detectar portal
url = "https://www.linkedin.com/jobs/view/123456"
print("Portal detectado:", detectar_portal(url))

# 2. Crear
nueva = crear_postulacion(
    puesto="Analista de Datos Jr.",
    empresa="Empresa Test",
    portal=detectar_portal(url),
    url=url,
    descripcion="Posición de prueba",
    estado="Postulado",
    notas="Solo un test"
)
print("Creada:", nueva)

# 3. Listar
todas = obtener_postulaciones()
print(f"Total postulaciones: {len(todas)}")

# 4. Editar
if nueva:
    editada = editar_postulacion(
        id=nueva["id"],
        puesto="Analista de Datos Jr.",
        empresa="Empresa Test",
        estado="En proceso"
    )
    print("Editada:", editada)

# 5. Eliminar
if nueva:
    eliminada = eliminar_postulacion(nueva["id"])
    print("Eliminada correctamente:", eliminada)
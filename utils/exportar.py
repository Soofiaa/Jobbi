import pandas as pd
from tkinter import filedialog, messagebox
from services.postulaciones import obtener_postulaciones

def exportar_excel(filtro_estado=None, filtro_empresa=None):
    datos = obtener_postulaciones(filtro_estado=filtro_estado,
                                   filtro_empresa=filtro_empresa)
    if not datos:
        messagebox.showwarning("Sin datos", "No hay postulaciones para exportar.")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel", "*.xlsx")],
        initialfile="jobbi_postulaciones.xlsx",
        title="Guardar exportación"
    )
    if not ruta:
        return

    columnas = {
        "puesto":             "Puesto",
        "empresa":            "Empresa",
        "portal":             "Portal",
        "url":                "URL",
        "estado":             "Estado",
        "descripcion":        "Descripción",
        "notas":              "Notas",
        "fecha_postulacion":  "Fecha postulación",
        "fecha_actualizacion":"Última actualización",
    }

    df = pd.DataFrame(datos)
    df = df[[c for c in columnas if c in df.columns]]
    df.rename(columns=columnas, inplace=True)
    df.fillna("", inplace=True)

    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Postulaciones")

        ws = writer.sheets["Postulaciones"]

        # Ancho de columnas automático
        for col_cells in ws.columns:
            max_len = max((len(str(c.value or "")) for c in col_cells), default=10)
            ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 4, 60)

    messagebox.showinfo("Exportación exitosa",
                        f"Se exportaron {len(datos)} postulaciones a:\n{ruta}")
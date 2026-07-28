import customtkinter as ctk
from services.postulaciones import obtener_postulaciones, ESTADOS

COLORES = {
    "bg_principal":  "#0f0f10",
    "bg_sidebar":    "#161618",
    "bg_tabla":      "#1a1a1d",
    "bg_panel":      "#161618",
    "acento":        "#4f8ef7",
    "texto_prim":    "#f0f0f0",
    "texto_sec":     "#888890",
    "borde":         "#2a2a30",
    "estados": {
        "Postulado":   ("#1e3a5f", "#4f8ef7"),
        "En proceso":  ("#3a2a1a", "#e8922a"),
        "Entrevista":  ("#1a3a2a", "#3dc47e"),
        "Oferta":      ("#2a1a3a", "#a855f7"),
        "Descartado":  ("#2a1a1a", "#888890"),
        "Rechazado":   ("#3a1a1a", "#e85555"),
    }
}

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=COLORES["bg_principal"], **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._construir()

    def _construir(self):
        # Título
        topbar = ctk.CTkFrame(self, height=64, corner_radius=0,
                               fg_color=COLORES["bg_principal"])
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_propagate(False)
        ctk.CTkLabel(topbar, text="Dashboard",
                     font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                     text_color=COLORES["texto_prim"]).pack(side="left", padx=24)

        # Contenido scrollable
        scroll = ctk.CTkScrollableFrame(self, fg_color=COLORES["bg_principal"])
        scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        scroll.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Fix: sin orden_desc=True, "datos[:5]" tomaba las 5 más antiguas en vez de las últimas.
        datos = obtener_postulaciones(orden_desc=True)
        total = len(datos)

        # Contar por estado
        conteo = {e: 0 for e in ESTADOS}
        for p in datos:
            estado = p.get("estado", "Postulado")
            if estado in conteo:
                conteo[estado] += 1

        activas   = conteo["Postulado"] + conteo["En proceso"] + conteo["Entrevista"]
        ofertas   = conteo["Oferta"]
        descartadas = conteo["Descartado"] + conteo["Rechazado"]

        # ── Tarjetas resumen ──
        tarjetas = [
            ("Total",       str(total),      "#4f8ef7", "postulaciones"),
            ("Activas",     str(activas),    "#3dc47e", "en curso"),
            ("Ofertas",     str(ofertas),    "#a855f7", "recibidas"),
            ("Descartadas", str(descartadas),"#e85555", "o rechazadas"),
        ]

        for i, (titulo, valor, color, sub) in enumerate(tarjetas):
            card = ctk.CTkFrame(scroll, corner_radius=12,
                                fg_color=COLORES["bg_tabla"],
                                border_width=1, border_color=COLORES["borde"])
            card.grid(row=0, column=i, padx=(0 if i == 0 else 8, 0), pady=(0, 20), sticky="ew")
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=titulo,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=COLORES["texto_sec"]).grid(row=0, column=0, padx=16, pady=(16, 4), sticky="w")
            ctk.CTkLabel(card, text=valor,
                         font=ctk.CTkFont(size=32, weight="bold"),
                         text_color=color).grid(row=1, column=0, padx=16, pady=(0, 4), sticky="w")
            ctk.CTkLabel(card, text=sub,
                         font=ctk.CTkFont(size=10),
                         text_color=COLORES["texto_sec"]).grid(row=2, column=0, padx=16, pady=(0, 16), sticky="w")

        # ── Gráfico de barras por estado ──
        seccion = ctk.CTkFrame(scroll, corner_radius=12,
                                fg_color=COLORES["bg_tabla"],
                                border_width=1, border_color=COLORES["borde"])
        seccion.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        seccion.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(seccion, text="Postulaciones por estado",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=COLORES["texto_prim"]).grid(row=0, column=0, padx=20, pady=(16, 12), sticky="w")

        max_val = max(conteo.values()) if any(conteo.values()) else 1

        for i, estado in enumerate(ESTADOS):
            val     = conteo[estado]
            bg, fg  = COLORES["estados"][estado]
            pct     = val / max_val if max_val > 0 else 0

            fila = ctk.CTkFrame(seccion, fg_color="transparent")
            fila.grid(row=i + 1, column=0, sticky="ew", padx=20, pady=4)
            fila.grid_columnconfigure(1, weight=1)

            # Etiqueta estado
            ctk.CTkLabel(fila, text=estado, width=110,
                         font=ctk.CTkFont(size=11),
                         text_color=fg, anchor="w").grid(row=0, column=0, padx=(0, 12))

            # Barra
            barra_bg = ctk.CTkFrame(fila, height=24, corner_radius=6,
                                     fg_color=COLORES["bg_principal"])
            barra_bg.grid(row=0, column=1, sticky="ew")
            barra_bg.grid_propagate(False)
            barra_bg.grid_columnconfigure(0, weight=1)

            if pct > 0:
                barra_fill = ctk.CTkFrame(barra_bg, height=24,
                                          corner_radius=6, fg_color=fg)
                barra_fill.place(relx=0, rely=0, relwidth=pct, relheight=1)

            # Número
            ctk.CTkLabel(fila, text=str(val), width=32,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=COLORES["texto_sec"],
                         anchor="e").grid(row=0, column=2, padx=(8, 0))

        # Padding final
        ctk.CTkFrame(seccion, height=16, fg_color="transparent").grid(
            row=len(ESTADOS) + 1, column=0)

        # ── Últimas 5 postulaciones ──
        recientes = ctk.CTkFrame(scroll, corner_radius=12,
                                  fg_color=COLORES["bg_tabla"],
                                  border_width=1, border_color=COLORES["borde"])
        recientes.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        recientes.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(recientes, text="Últimas postulaciones",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=COLORES["texto_prim"]).grid(
                         row=0, column=0, columnspan=4, padx=20, pady=(16, 8), sticky="w")

        ultimas = datos[:5]
        if not ultimas:
            ctk.CTkLabel(recientes, text="Aún no hay postulaciones.",
                         text_color=COLORES["texto_sec"]).grid(
                             row=1, column=0, padx=20, pady=(0, 16))
        else:
            for i, p in enumerate(ultimas):
                estado  = p.get("estado", "Postulado")
                _, fg   = COLORES["estados"].get(estado, ("#1a1a1d", "#888890"))

                ctk.CTkLabel(recientes, text=p.get("puesto", ""),
                             font=ctk.CTkFont(size=12, weight="bold"),
                             text_color=COLORES["texto_prim"],
                             anchor="w").grid(row=i + 1, column=1, padx=(20, 8),
                                              pady=(4, 0), sticky="w")
                ctk.CTkLabel(recientes, text=p.get("empresa", ""),
                             font=ctk.CTkFont(size=11),
                             text_color=COLORES["texto_sec"],
                             anchor="w").grid(row=i + 1, column=2, padx=(0, 8),
                                              pady=(4, 0), sticky="w")
                ctk.CTkLabel(recientes, text=estado,
                             font=ctk.CTkFont(size=10, weight="bold"),
                             text_color=fg,
                             anchor="e").grid(row=i + 1, column=3, padx=(0, 20),
                                              pady=(4, 0), sticky="e")

            ctk.CTkFrame(recientes, height=16, fg_color="transparent").grid(
                row=len(ultimas) + 1, column=0)
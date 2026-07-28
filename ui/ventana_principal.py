import customtkinter as ctk
from tkinter import ttk, messagebox
from services.postulaciones import obtener_postulaciones, eliminar_postulacion, ESTADOS
from ui.theme import COLORES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jobbi")
        self.geometry("1200x700")
        self.minsize(900, 550)
        self.configure(fg_color=COLORES["bg_principal"])
        self._panel_visible = False
        self._id_editar = None
        self._formulario_widget = None

        self._aplicar_estilo_tabla()
        self._construir_ui()
        self.cargar_postulaciones()

    # ─────────────────────────────────────────
    # ESTILOS TTK
    # ─────────────────────────────────────────
    def _aplicar_estilo_tabla(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Jobbi.Treeview",
            background=COLORES["bg_tabla"],
            foreground=COLORES["texto_prim"],
            fieldbackground=COLORES["bg_tabla"],
            rowheight=44,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10),
        )
        style.configure("Jobbi.Treeview.Heading",
            background=COLORES["bg_sidebar"],
            foreground=COLORES["texto_sec"],
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=(12, 10),
        )
        style.map("Jobbi.Treeview",
            background=[("selected", "#1e2d45")],
            foreground=[("selected", COLORES["acento"])],
        )
        style.map("Jobbi.Treeview.Heading",
            background=[("active", COLORES["bg_tabla"])],
        )
        style.configure("Jobbi.Vertical.TScrollbar",
            background=COLORES["bg_tabla"],
            troughcolor=COLORES["bg_tabla"],
            borderwidth=0,
            relief="flat",
            arrowsize=0,
        )

    # ─────────────────────────────────────────
    # CONSTRUCCIÓN UI
    # ─────────────────────────────────────────
    def _construir_ui(self):
        # Layout raíz: sidebar | contenido | panel
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar ──
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0,
                                fg_color=COLORES["bg_sidebar"])
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(14, weight=1)

        ctk.CTkLabel(sidebar, text="Jobbi",
                     font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
                     text_color=COLORES["acento"]).grid(row=0, column=0, padx=24, pady=(28, 4), sticky="w")
        ctk.CTkLabel(sidebar, text="Job Tracker",
                     font=ctk.CTkFont(size=11),
                     text_color=COLORES["texto_sec"]).grid(row=1, column=0, padx=24, pady=(0, 16), sticky="w")

        self.btn_nav_lista = ctk.CTkButton(
            sidebar, text="  ☰  Postulaciones", anchor="w", width=180,
            fg_color=COLORES["acento"], hover_color=COLORES["acento_hover"],
            font=ctk.CTkFont(size=12),
            command=self._mostrar_lista
        )
        self.btn_nav_lista.grid(row=2, column=0, padx=16, pady=(0, 6), sticky="ew")

        self.btn_nav_dash = ctk.CTkButton(
            sidebar, text="  ◈  Dashboard", anchor="w", width=180,
            fg_color="transparent", hover_color=COLORES["bg_tabla"],
            border_width=1, border_color=COLORES["borde"],
            text_color=COLORES["texto_sec"],
            font=ctk.CTkFont(size=12),
            command=self._mostrar_dashboard
        )
        self.btn_nav_dash.grid(row=3, column=0, padx=16, pady=(0, 16), sticky="ew")

        # Estadísticas rápidas en sidebar
        self.lbl_total_side = ctk.CTkLabel(sidebar, text="0 postulaciones",
                                            font=ctk.CTkFont(size=12, weight="bold"),
                                            text_color=COLORES["texto_prim"])
        self.lbl_total_side.grid(row=4, column=0, padx=24, pady=(0, 4), sticky="w")

        self.lbl_activas_side = ctk.CTkLabel(sidebar, text="0 activas",
                                              font=ctk.CTkFont(size=11),
                                              text_color=COLORES["texto_sec"])
        self.lbl_activas_side.grid(row=5, column=0, padx=24, pady=(0, 24), sticky="w")

        # Separador
        sep = ctk.CTkFrame(sidebar, height=1, fg_color=COLORES["borde"])
        sep.grid(row=6, column=0, sticky="ew", padx=16, pady=(0, 24))

        # Filtro por estado (sidebar)
        ctk.CTkLabel(sidebar, text="FILTRAR POR MES",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=COLORES["texto_sec"]).grid(row=7, column=0, padx=24, sticky="w")

        self.filtro_mes = ctk.CTkOptionMenu(
            sidebar,
            values=["Todos"],
            width=180,
            fg_color=COLORES["bg_tabla"],
            button_color=COLORES["bg_tabla"],
            button_hover_color=COLORES["borde"],
            dropdown_fg_color=COLORES["bg_tabla"],
            text_color=COLORES["texto_prim"],
            command=lambda _: self.cargar_postulaciones()
        )
        self.filtro_mes.grid(row=8, column=0, padx=20, pady=(6, 16), sticky="ew")

        ctk.CTkLabel(sidebar, text="FILTRAR POR ESTADO",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=COLORES["texto_sec"]).grid(row=9, column=0, padx=24, sticky="w")

        self.filtro_estado = ctk.CTkOptionMenu(
            sidebar,
            values=["Todos"] + ESTADOS,
            width=180,
            fg_color=COLORES["bg_tabla"],
            button_color=COLORES["bg_tabla"],
            button_hover_color=COLORES["borde"],
            dropdown_fg_color=COLORES["bg_tabla"],
            text_color=COLORES["texto_prim"],
            command=lambda _: self.cargar_postulaciones()
        )
        self.filtro_estado.grid(row=10, column=0, padx=20, pady=(6, 16), sticky="ew")

        # Búsqueda empresa
        # Fix: compartía row=7 con "FILTRAR POR MES", causando superposición visual.
        ctk.CTkLabel(sidebar, text="BUSCAR EMPRESA",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=COLORES["texto_sec"]).grid(row=11, column=0, padx=24, sticky="w")

        self.filtro_empresa = ctk.CTkEntry(
            sidebar,
            placeholder_text="Nombre empresa...",
            fg_color=COLORES["bg_tabla"],
            border_color=COLORES["borde"],
            text_color=COLORES["texto_prim"],
            placeholder_text_color=COLORES["texto_sec"],
            width=180,
        )
        self.filtro_empresa.grid(row=12, column=0, padx=20, pady=(6, 12), sticky="ew")
        self.filtro_empresa.bind("<KeyRelease>", lambda _: self.cargar_postulaciones())

        ctk.CTkButton(sidebar, text="Limpiar filtros", width=180,
                      fg_color="transparent", border_width=1,
                      border_color=COLORES["borde"],
                      text_color=COLORES["texto_sec"],
                      hover_color=COLORES["bg_tabla"],
                      command=self.limpiar_filtros).grid(row=13, column=0, padx=20, pady=(0, 16), sticky="ew")

        # Botón exportar abajo del sidebar
        ctk.CTkButton(sidebar, text="↓  Exportar datos", width=180,
                      fg_color="transparent", border_width=1,
                      border_color=COLORES["borde"],
                      text_color=COLORES["texto_sec"],
                      hover_color=COLORES["bg_tabla"],
                      command=self.exportar).grid(row=15, column=0, padx=20, pady=(0, 20), sticky="sew")

        # ── Área central ──
        self._centro = ctk.CTkFrame(self, corner_radius=0, fg_color=COLORES["bg_principal"])
        self._centro.grid(row=0, column=1, sticky="nsew")
        centro = self._centro
        centro.grid_columnconfigure(0, weight=1)
        centro.grid_rowconfigure(1, weight=1)

        # Topbar
        topbar = ctk.CTkFrame(centro, height=64, corner_radius=0,
                               fg_color=COLORES["bg_principal"])
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_propagate(False)

        ctk.CTkLabel(topbar, text="Mis postulaciones",
                     font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                     text_color=COLORES["texto_prim"]).grid(row=0, column=0, padx=24, sticky="w")

        self.btn_nueva = ctk.CTkButton(
            topbar, text="+ Nueva postulación", width=180,
            fg_color=COLORES["acento"],
            hover_color=COLORES["acento_hover"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.abrir_panel_crear
        )
        self.btn_nueva.grid(row=0, column=1, padx=20)

        # Tabla
        tabla_frame = ctk.CTkFrame(centro, corner_radius=12,
                                    fg_color=COLORES["bg_tabla"])
        tabla_frame.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)

        cols = ("puesto", "empresa", "portal", "estado", "fecha")
        self.tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                                   style="Jobbi.Treeview", selectmode="browse")

        encabezados = {
            "puesto":  ("Puesto",   300),
            "empresa": ("Empresa",  180),
            "portal":  ("Portal",   130),
            "estado":  ("Estado",   130),
            "fecha":   ("Fecha",    110),
        }
        self._orden_fecha = False  # False = ascendente, True = descendente

        def alternar_orden_fecha():
            self._orden_fecha = not self._orden_fecha
            simbolo = " ↑" if not self._orden_fecha else " ↓"
            self.tabla.heading("fecha", text="Fecha" + simbolo,
                               command=alternar_orden_fecha)
            self.cargar_postulaciones()

        for col, (titulo, ancho) in encabezados.items():
            if col == "fecha":
                self.tabla.heading(col, text=titulo + " ↑",
                                   command=alternar_orden_fecha)
            else:
                self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=ancho,
                               anchor="center" if col in ("estado", "fecha", "portal") else "w",
                               minwidth=80)

        scroll = ttk.Scrollbar(tabla_frame, orient="vertical",
                                command=self.tabla.yview,
                                style="Jobbi.Vertical.TScrollbar")
        self.tabla.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns", pady=4)
        self.tabla.grid(row=0, column=0, sticky="nsew", padx=(4, 0), pady=4)
        self.tabla.tag_configure("par",   background=COLORES["bg_fila_par"])
        self.tabla.tag_configure("impar", background=COLORES["bg_fila_impar"])

        for estado, (bg, fg) in COLORES["estados"].items():
            self.tabla.tag_configure(f"estado_{estado}", background=bg, foreground=fg)
        self.tabla.bind("<Double-1>", self.abrir_panel_editar)
        self.tabla.bind("<ButtonRelease-1>", self._actualizar_boton_eliminar)

        # Barra inferior
        pie = ctk.CTkFrame(centro, height=44, corner_radius=0,
                            fg_color=COLORES["bg_principal"])
        pie.grid(row=2, column=0, sticky="ew")
        pie.grid_columnconfigure(0, weight=1)
        pie.grid_propagate(False)

        self.lbl_total = ctk.CTkLabel(pie, text="",
                                       font=ctk.CTkFont(size=11),
                                       text_color=COLORES["texto_sec"])
        self.lbl_total.grid(row=0, column=0, padx=20, sticky="w")

        self.btn_eliminar = ctk.CTkButton(
            pie, text="Eliminar seleccionada", width=170,
            fg_color="#3a1a1a", hover_color="#5a2020",
            text_color="#e85555",
            font=ctk.CTkFont(size=12),
            command=self.eliminar_seleccionada,
            state="disabled"
        )
        self.btn_eliminar.grid(row=0, column=1, padx=16, pady=6)

        # ── Panel lateral derecho ──
        self.panel = ctk.CTkFrame(self, width=380, corner_radius=0,
                                   fg_color=COLORES["bg_panel"])
        self._ids_postulaciones = []
        
        # Dashboard (oculto por defecto)
        from ui.dashboard import Dashboard
        self.vista_dashboard = Dashboard(self)
        self._vista_actual = "lista"

    # ─────────────────────────────────────────
    # PANEL LATERAL
    # ─────────────────────────────────────────
    def _mostrar_panel(self):
        if not self._panel_visible:
            self.panel.grid(row=0, column=2, sticky="nsew")
            self.panel.grid_propagate(False)
            self._panel_visible = True

    def _ocultar_panel(self):
        if self._panel_visible:
            self.panel.grid_forget()
            self._panel_visible = False
        self._id_editar = None

    def abrir_panel_crear(self):
        self._id_editar = None
        self._mostrar_panel()
        self._construir_formulario(titulo="Nueva postulación")

    def abrir_panel_editar(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        idx = self.tabla.index(seleccion[0])
        if idx < len(self._ids_postulaciones):
            self._id_editar = self._ids_postulaciones[idx]
            self._mostrar_panel()
            self._construir_formulario(titulo="Editar postulación",
                                        id_editar=self._id_editar)

    # ─────────────────────────────────────────
    # FORMULARIO DENTRO DEL PANEL
    # ─────────────────────────────────────────
    def _construir_formulario(self, titulo: str, id_editar=None):
        from services.postulaciones import (crear_postulacion, editar_postulacion,
                                             obtener_postulacion_por_id)
        from utils.portal_detector import detectar_portal

        for w in self.panel.winfo_children():
            w.destroy()

        self.panel.grid_columnconfigure(0, weight=1)

        # Header del panel
        header = ctk.CTkFrame(self.panel, height=56, corner_radius=0,
                               fg_color=COLORES["bg_sidebar"])
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_propagate(False)

        ctk.CTkLabel(header, text=titulo,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORES["texto_prim"]).grid(row=0, column=0, padx=20, sticky="w")

        ctk.CTkButton(header, text="✕", width=32, height=32,
                      fg_color="transparent",
                      hover_color=COLORES["bg_tabla"],
                      text_color=COLORES["texto_sec"],
                      command=self._ocultar_panel).grid(row=0, column=1, padx=12)

        # Scroll frame para el contenido
        scroll_frame = ctk.CTkScrollableFrame(self.panel,
                                               fg_color=COLORES["bg_panel"],
                                               scrollbar_button_color=COLORES["borde"],
                                               scrollbar_button_hover_color=COLORES["texto_sec"])
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.panel.grid_rowconfigure(1, weight=1)
        scroll_frame.grid_columnconfigure(0, weight=1)

        def label(texto):
            ctk.CTkLabel(scroll_frame, text=texto,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=COLORES["texto_sec"],
                         anchor="w").pack(fill="x", padx=20, pady=(14, 2))

        def entrada(placeholder):
            e = ctk.CTkEntry(scroll_frame,
                             placeholder_text=placeholder,
                             fg_color=COLORES["bg_tabla"],
                             border_color=COLORES["borde"],
                             text_color=COLORES["texto_prim"],
                             placeholder_text_color=COLORES["texto_sec"],
                             height=38)
            e.pack(fill="x", padx=20, pady=(0, 2))
            return e

        label("PUESTO *")
        campo_puesto = entrada("")

        label("EMPRESA *")
        campo_empresa = entrada("Ej: Falabella")

        label("URL DEL AVISO")
        campo_url = entrada("https://...")

        label("PORTAL")
        campo_portal = entrada("Autodetectado desde la URL")

        def autodetectar(event=None):
            url = campo_url.get()
            portal = detectar_portal(url)
            if portal and portal != "Otro":
                campo_portal.delete(0, "end")
                campo_portal.insert(0, portal)

        campo_url.bind("<FocusOut>", autodetectar)
        campo_url.bind("<KeyRelease>", autodetectar)

        label("ESTADO")
        campo_estado = ctk.CTkOptionMenu(
            scroll_frame, values=ESTADOS,
            fg_color=COLORES["bg_tabla"],
            button_color=COLORES["bg_tabla"],
            button_hover_color=COLORES["borde"],
            dropdown_fg_color=COLORES["bg_tabla"],
            text_color=COLORES["texto_prim"],
            height=38
        )
        campo_estado.set("Postulado")
        campo_estado.pack(fill="x", padx=20, pady=(0, 2))

        label("DESCRIPCIÓN")
        campo_desc = ctk.CTkTextbox(scroll_frame, height=90,
                                     fg_color=COLORES["bg_tabla"],
                                     border_color=COLORES["borde"],
                                     text_color=COLORES["texto_prim"])
        campo_desc.pack(fill="x", padx=20, pady=(0, 2))

        label("NOTAS PERSONALES")
        campo_notas = ctk.CTkTextbox(scroll_frame, height=70,
                                      fg_color=COLORES["bg_tabla"],
                                      border_color=COLORES["borde"],
                                      text_color=COLORES["texto_prim"])
        campo_notas.pack(fill="x", padx=20, pady=(0, 2))

        label("FECHA DE POSTULACIÓN  (dd-mm-aaaa)")
        campo_fecha = ctk.CTkEntry(scroll_frame,
                                   fg_color=COLORES["bg_tabla"],
                                   border_color=COLORES["borde"],
                                   text_color=COLORES["texto_prim"],
                                   placeholder_text_color=COLORES["texto_sec"],
                                   height=38)
        campo_fecha.pack(fill="x", padx=20, pady=(0, 16))

        # Fecha por defecto: hoy en dd-mm-aaaa
        from datetime import date
        campo_fecha.insert(0, date.today().strftime("%d-%m-%Y"))

        # Cargar datos si es edición
        if id_editar:
            datos = obtener_postulacion_por_id(id_editar)
            if datos:
                campo_puesto.insert(0, datos.get("puesto", ""))
                campo_empresa.insert(0, datos.get("empresa", ""))
                campo_url.insert(0, datos.get("url", "") or "")
                campo_portal.insert(0, datos.get("portal", "") or "")
                campo_estado.set(datos.get("estado", "Postulado"))
                campo_desc.insert("1.0", datos.get("descripcion", "") or "")
                campo_notas.insert("1.0", datos.get("notas", "") or "")
                fecha_db = datos.get("fecha_postulacion", "")
                if fecha_db:
                    from datetime import datetime
                    try:
                        fecha_fmt = datetime.strptime(str(fecha_db), "%Y-%m-%d").strftime("%d-%m-%Y")
                        campo_fecha.delete(0, "end")
                        campo_fecha.insert(0, fecha_fmt)
                    except ValueError:
                        pass

        # Botones
        def guardar():
            puesto  = campo_puesto.get().strip()
            empresa = campo_empresa.get().strip()
            if not puesto or not empresa:
                messagebox.showwarning("Campos requeridos",
                                       "El puesto y la empresa son obligatorios.")
                return
            from datetime import datetime
            fecha_str = campo_fecha.get().strip()
            fecha_db  = None
            try:
                fecha_db = datetime.strptime(fecha_str, "%d-%m-%Y").strftime("%Y-%m-%d")
            except ValueError:
                from tkinter import messagebox
                messagebox.showwarning("Fecha inválida",
                                       "La fecha debe tener el formato dd-mm-aaaa.")
                return

            kwargs = dict(
                puesto             = puesto,
                empresa            = empresa,
                portal             = campo_portal.get().strip() or None,
                url                = campo_url.get().strip() or None,
                descripcion        = campo_desc.get("1.0", "end").strip() or None,
                estado             = campo_estado.get(),
                notas              = campo_notas.get("1.0", "end").strip() or None,
                fecha_postulacion  = fecha_db,
            )
            try:
                if id_editar:
                    editar_postulacion(id=id_editar, **kwargs)
                else:
                    crear_postulacion(**kwargs)
            except Exception as e:
                messagebox.showerror("Error de conexión",
                                      f"No se pudo guardar la postulación.\n\n{e}")
                return
            self.cargar_postulaciones()
            self._ocultar_panel()

        botones = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        botones.pack(fill="x", padx=20, pady=(4, 20))
        botones.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(botones, text="Cancelar",
                      fg_color="transparent", border_width=1,
                      border_color=COLORES["borde"],
                      text_color=COLORES["texto_sec"],
                      hover_color=COLORES["bg_tabla"],
                      command=self._ocultar_panel).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(botones, text="Guardar",
                      fg_color=COLORES["acento"],
                      hover_color=COLORES["acento_hover"],
                      font=ctk.CTkFont(weight="bold"),
                      command=guardar).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    # ─────────────────────────────────────────
    # CARGAR DATOS
    # ─────────────────────────────────────────
    def cargar_postulaciones(self):
        estado  = self.filtro_estado.get()
        empresa = self.filtro_empresa.get()
        etiqueta_mes = self.filtro_mes.get()
        if hasattr(self, "_meses_clave") and etiqueta_mes != "Todos":
            idx  = self._meses_etiqueta.index(etiqueta_mes) if hasattr(self, "_meses_etiqueta") and etiqueta_mes in self._meses_etiqueta else -1
            mes  = self._meses_clave[idx] if idx > 0 else "Todos"
        else:
            mes  = "Todos"
        try:
            datos = obtener_postulaciones(filtro_estado=estado, filtro_empresa=empresa,
                                           orden_desc=self._orden_fecha, filtro_mes=mes)
            self._actualizar_opciones_mes()
        except Exception as e:
            messagebox.showerror("Error de conexión",
                                  f"No se pudieron cargar las postulaciones.\n\n{e}")
            return

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        self._ids_postulaciones = []
        activas = 0

        for i, p in enumerate(datos):
            estado_val = p.get("estado", "Postulado")
            if estado_val in ("Postulado", "En proceso", "Entrevista"):
                activas += 1
            tag_fila  = "par" if i % 2 == 0 else "impar"
            tag_estado = f"estado_{estado_val}"
            self.tabla.insert("", "end", tags=(tag_fila, tag_estado), values=(
                p["puesto"],
                p["empresa"],
                p.get("portal") or "—",
                estado_val,
                p.get("fecha_postulacion") or "—",
            ))
            self._ids_postulaciones.append(p["id"])

        total = len(datos)
        self.lbl_total.configure(text=f"{total} postulación(es) encontrada(s)")
        self.lbl_total_side.configure(text=f"{total} postulaciones")
        self.lbl_activas_side.configure(text=f"{activas} activas")
        self.btn_eliminar.configure(state="disabled")
        
    def _actualizar_opciones_mes(self):
        from services.postulaciones import obtener_postulaciones as _get
        todos = _get()
        meses_vistos = {}
        for p in todos:
            fecha = p.get("fecha_postulacion", "")
            if fecha and len(str(fecha)) >= 7:
                clave = str(fecha)[:7]          # "YYYY-MM"
                anio, mes_num = clave.split("-")
                import locale
                MESES = {
                    "01": "Enero",   "02": "Febrero", "03": "Marzo",
                    "04": "Abril",   "05": "Mayo",    "06": "Junio",
                    "07": "Julio",   "08": "Agosto",  "09": "Septiembre",
                    "10": "Octubre", "11": "Noviembre","12": "Diciembre"
                }
                etiqueta = f"{MESES.get(mes_num, mes_num)} {anio}"
                meses_vistos[clave] = etiqueta

        opciones_clave    = ["Todos"] + sorted(meses_vistos.keys(), reverse=True)
        opciones_etiqueta = ["Todos"] + [meses_vistos[k] for k in opciones_clave[1:]]

        self._meses_clave = opciones_clave
        self.filtro_mes.configure(values=opciones_etiqueta)

        actual = self.filtro_mes.get()
        if actual not in opciones_etiqueta:
            self.filtro_mes.set("Todos")
            
    # ─────────────────────────────────────────
    # ELIMINAR
    # ─────────────────────────────────────────
    def _actualizar_boton_eliminar(self, event=None):
        if self.tabla.selection():
            self.btn_eliminar.configure(state="normal")
        else:
            self.btn_eliminar.configure(state="disabled")

    def eliminar_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        idx = self.tabla.index(seleccion[0])
        valores = self.tabla.item(seleccion[0])["values"]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{valores[0]}' en {valores[1]}?"):
            return
        if idx < len(self._ids_postulaciones):
            try:
                eliminar_postulacion(self._ids_postulaciones[idx])
            except Exception as e:
                messagebox.showerror("Error de conexión",
                                      f"No se pudo eliminar la postulación.\n\n{e}")
                return
        self._ocultar_panel()
        self.cargar_postulaciones()
        
    # ─────────────────────────────────────────
    # NAVEGACIÓN ENTRE VISTAS
    # ─────────────────────────────────────────
    def _mostrar_lista(self):
        if self._vista_actual == "lista":
            return
        self.vista_dashboard.grid_forget()
        self._centro.grid(row=0, column=1, sticky="nsew")
        self._vista_actual = "lista"
        self.btn_nav_lista.configure(fg_color=COLORES["acento"],
                                      text_color=COLORES["texto_prim"],
                                      border_width=0)
        self.btn_nav_dash.configure(fg_color="transparent",
                                     text_color=COLORES["texto_sec"],
                                     border_width=1)

    def _mostrar_dashboard(self):
        if self._vista_actual == "dashboard":
            return
        self._centro.grid_forget()
        from ui.dashboard import Dashboard
        self.vista_dashboard.destroy()
        self.vista_dashboard = Dashboard(self)
        self.vista_dashboard.grid(row=0, column=1, sticky="nsew")
        self._vista_actual = "dashboard"
        self.btn_nav_dash.configure(fg_color=COLORES["acento"],
                                     text_color=COLORES["texto_prim"],
                                     border_width=0)
        self.btn_nav_lista.configure(fg_color="transparent",
                                      text_color=COLORES["texto_sec"],
                                      border_width=1)

    # ─────────────────────────────────────────
    # UTILIDADES
    # ─────────────────────────────────────────
    def limpiar_filtros(self):
        self.filtro_estado.set("Todos")
        self.filtro_empresa.delete(0, "end")
        self.filtro_mes.set("Todos")
        self.cargar_postulaciones()

    def exportar(self):
        from utils.exportar import exportar_excel
        exportar_excel(
            filtro_estado=self.filtro_estado.get(),
            filtro_empresa=self.filtro_empresa.get()
        )
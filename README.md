# Jobbi

Aplicación de escritorio para llevar el registro de postulaciones laborales:
puesto, empresa, portal, estado, notas y fechas, con dashboard de métricas y
exportación a Excel.

Construida en Python con interfaz nativa (CustomTkinter) y persistencia en
Supabase (Postgres + REST), empaquetada como ejecutable de Windows con
PyInstaller e instalador con Inno Setup.

---

## Características

- **Registro de postulaciones**: puesto, empresa, portal de origen (con
  autodetección desde la URL), descripción, notas personales, estado y
  fechas de postulación/actualización.
- **Filtros combinables**: por estado, por empresa (búsqueda parcial) y por
  mes de postulación.
- **Dashboard**: totales por estado, postulaciones activas vs. descartadas,
  gráfico de barras por estado y listado de las últimas postulaciones
  registradas.
- **Exportación a Excel** (`.xlsx`) de los datos filtrados, con ancho de
  columnas autoajustado.
- **Autodetección de portal** (LinkedIn, Indeed, Trabajando.com, Bumeran,
  Get on Board, Laborum, Glassdoor, Computrabajo, InfoJobs, Hired) a partir
  de la URL del aviso.
- **Empaquetado standalone**: distribuible como `.exe` con instalador,
  sin necesidad de tener Python instalado en el equipo destino.

## Capturas de pantalla

> _Agregar aquí 2-3 capturas: vista de lista de postulaciones, dashboard,
> y formulario de nueva postulación._

## Stack técnico

| Capa            | Tecnología                                  |
|-----------------|----------------------------------------------|
| UI              | Python, CustomTkinter, ttk (Treeview)         |
| Backend/lógica  | Python (capa de servicios sobre el cliente Supabase) |
| Persistencia    | Supabase (Postgres + REST vía `supabase-py`)  |
| Exportación     | pandas, openpyxl                              |
| Empaquetado     | PyInstaller (`.exe`) + Inno Setup (instalador) |
| Tests           | pytest, mocks del cliente de Supabase         |

## Estructura del proyecto

```
Jobbi/
├── main.py                    # Punto de entrada
├── db/
│   └── connection.py          # Cliente de Supabase y carga de variables de entorno
├── services/
│   └── postulaciones.py       # Lógica de negocio: CRUD y filtros sobre postulaciones
├── ui/
│   ├── ventana_principal.py   # Ventana principal, sidebar, tabla y panel lateral
│   ├── dashboard.py           # Vista de métricas y gráfico por estado
│   └── theme.py               # Paleta de colores unificada de la app
├── utils/
│   ├── portal_detector.py     # Detección de portal de empleo desde una URL
│   └── exportar.py            # Exportación de postulaciones a Excel
├── tests/                     # Suite de tests (pytest, con mocks de Supabase)
├── requirements.txt            # Dependencias de producción
├── requirements-dev.txt        # Dependencias de desarrollo (pytest, etc.)
├── jobbi.spec                  # Configuración de PyInstaller
└── jobbi_installer.iss         # Configuración de Inno Setup
```

## Instalación (modo desarrollo)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Soofiaa/Jobbi.git
cd Jobbi
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
pip install -r requirements-dev.txt   # solo si vas a correr tests
```

### 3. Configurar variables de entorno

Copia `.env.example` a `.env` en la raíz del proyecto y completa tus
credenciales de Supabase:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
```

> **Importante:** usa siempre la **anon key** de Supabase, nunca la
> `service_role key`, ya que esta aplicación se distribuye como ejecutable
> y cualquier credencial embebida en ella puede ser extraída. Ver la
> sección [Seguridad](#seguridad) más abajo.

### 4. Ejecutar la aplicación

```bash
python main.py
```

## Tests

El proyecto cuenta con una suite de pytest que mockea el cliente de
Supabase, por lo que corre sin conexión a internet ni credenciales reales.

```bash
pytest -v
```

Cobertura actual:
- `tests/test_portal_detector.py`: detección de portal a partir de URLs
  (casos válidos, sin protocolo, dominio no reconocido, URL vacía/`None`).
- `tests/test_postulaciones.py`: creación, filtros combinados
  (estado/empresa/mes), edición y eliminación de postulaciones.

## Generar el ejecutable

```bash
pyinstaller jobbi.spec
```

Esto genera el ejecutable en `dist/Jobbi/`. Para crear el instalador de
Windows, compila `jobbi_installer.iss` con [Inno Setup](https://jrsoftware.org/isinfo.php).

> Los directorios `build/`, `dist/` e `installer/*.exe` no se versionan en
> este repositorio (ver `.gitignore`); se generan localmente al ejecutar
> los pasos anteriores.

## Seguridad

- La aplicación usa la **anon key** de Supabase (verificado decodificando
  el JWT), no la `service_role key`.
- La app no implementa autenticación de usuario, por lo que la protección
  real de los datos depende de las **políticas de Row Level Security (RLS)**
  configuradas en el proyecto de Supabase. **Pendiente de verificación
  manual**: confirmar en el dashboard de Supabase (Authentication → Policies)
  que las tablas tienen RLS habilitado con políticas restrictivas antes de
  distribuir el instalador ampliamente.
- Nunca subas tu archivo `.env` al repositorio (ya está excluido vía
  `.gitignore`).

## Roadmap / mejoras conocidas

- [ ] `detectar_portal()` no reconoce URLs sin esquema (ej.
      `www.linkedin.com/...` sin `https://`) — ver issue correspondiente.
- [ ] Extraer manejo de errores de red a un decorador reutilizable en
      lugar de `try/except` repetidos en la UI.

## Autora

Sofía Menzel — [GitHub](https://github.com/Soofiaa)

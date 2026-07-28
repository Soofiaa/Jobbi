# Jobbi

Jobbi es una app de escritorio para llevar el registro de tus postulaciones
laborales: dónde postulaste, en qué estado está cada proceso, cuándo
aplicaste y qué notas dejaste sobre cada una. Pensada para uso personal,
sin cuentas ni multiusuario.

## Funcionalidades

- Alta, edición y eliminación de postulaciones (puesto, empresa, portal,
  URL del aviso, estado, fecha, descripción y notas).
- Autodetección del portal (LinkedIn, Indeed, Get on Board, Bumeran,
  Laborum, Glassdoor, Computrabajo, InfoJobs, Hired, Trabajando.com) a
  partir de la URL pegada.
- Filtros por estado, por mes y por nombre de empresa.
- Dashboard con totales, postulaciones activas/ofertas/descartadas,
  distribución por estado y las últimas postulaciones cargadas.
- Exportación a Excel.

## Stack técnico

- **Python 3.13**
- **CustomTkinter** — UI de escritorio
- **Supabase** (Postgres + REST) — persistencia de datos
- **pandas / openpyxl** — exportación a Excel
- **PyInstaller** + **Inno Setup** — empaquetado del `.exe` e instalador
  para Windows
- **pytest / pytest-mock** — tests

## Instalación y configuración

1. Cloná el repo y creá un entorno virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copiá `.env.example` a `.env` y completá tus credenciales de Supabase:

   ```
   SUPABASE_URL=https://tu-proyecto.supabase.co
   SUPABASE_KEY=tu-anon-key
   ```

   El `.env` debe quedar en la raíz del proyecto. Nunca lo subas a git
   (ya está en `.gitignore`).

## Modo desarrollo

```bash
python main.py
```

`db/connection.py` detecta si corre como script o como `.exe` compilado
(`sys.frozen`) y busca el `.env` en la raíz del proyecto en el primer
caso, y junto al ejecutable en el segundo.

## Generar el `.exe`

```bash
python build.py
```

Esto corre PyInstaller con `jobbi.spec` y copia el `.env` a
`dist/Jobbi/.env` para que el ejecutable tenga sus credenciales. El
instalador de Windows se genera aparte con Inno Setup a partir de
`jobbi_installer.iss`. Ni `build/`, `dist/` ni `installer/` se versionan
en git — son artefactos regenerables.

## Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

La suite corre sin conexión a internet ni credenciales reales: las
llamadas a Supabase están mockeadas (`tests/conftest.py`).

## Seguridad: tipo de key de Supabase

`SUPABASE_KEY` es la **anon key** (se verificó decodificando el claim
`role` del JWT), no la service_role key — es la que corresponde usar en
un cliente distribuido, porque la service_role key tiene acceso total de
lectura/escritura sin restricciones y cualquiera podría extraerla del
`.exe`.

Dicho eso, la app no tiene login de usuario: se conecta directo con la
anon key. La protección real depende entonces de las **políticas RLS**
configuradas en la tabla `postulaciones` en el dashboard de Supabase, que
no se pudo verificar de forma remota (solo hay credenciales REST en
`.env`, no una conexión directa a Postgres). Si vas a distribuir el
`.exe` más ampliamente, confirmá en Supabase → Authentication → Policies
que RLS esté habilitado con políticas acotadas para esa tabla.

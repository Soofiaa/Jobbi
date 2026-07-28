# Issues conocidos

## `detectar_portal` no reconoce URLs pegadas sin protocolo

**Encontrado durante:** QA sobre `utils/portal_detector.py` al migrar los
tests a pytest (ver `tests/test_portal_detector.py`).

**Estado:** abierto, sin fix aplicado todavía (fuera del alcance de la
migración de tests para no mezclar responsabilidades).

### Repro

```python
from utils.portal_detector import detectar_portal

detectar_portal("www.linkedin.com/jobs/view/123456")
# -> "Otro"   (se esperaría "LinkedIn")

detectar_portal("https://www.linkedin.com/jobs/view/123456")
# -> "LinkedIn"  (funciona bien con protocolo)
```

### Causa

`urlparse()` de `urllib.parse` solo interpreta el `netloc` (host) cuando
la URL tiene un esquema explícito (`http://`, `https://`). Sin esquema,
trata todo el string como `path`, así que `urlparse(url).netloc` queda
vacío y `detectar_portal` no puede matchear ningún dominio de
`PORTALES`, cayendo siempre en `"Otro"`.

```python
from urllib.parse import urlparse
urlparse("www.linkedin.com/jobs/view/123456").netloc   # -> '' (vacío)
urlparse("https://www.linkedin.com/jobs/view/1").netloc # -> 'www.linkedin.com'
```

### Impacto

En `ui/ventana_principal.py`, el autodetectado de portal se dispara al
tipear/perder foco en el campo URL (`campo_url.bind("<FocusOut>", ...)`
y `<KeyRelease>`). Si el usuario pega una URL sin `https://` (algo común
al copiar desde la barra de direcciones de algunos navegadores o desde
texto plano), el campo "Portal" no se autocompleta y queda vacío —no
rompe nada, pero se pierde la conveniencia principal de la feature para
ese caso, que además es común.

### Fix propuesto (no aplicado)

En `detectar_portal`, si `urlparse(url).netloc` viene vacío pero el
string no está vacío, reintentar anteponiendo `"//"` (o `"https://"`)
antes de parsear:

```python
def detectar_portal(url: str) -> str:
    if not url or url.strip() == "":
        return ""
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower().replace("www.", "")
        if not host:
            # URL sin esquema: reintentar como si fuera "//dominio/..."
            parsed = urlparse("//" + url)
            host = parsed.netloc.lower().replace("www.", "")
        for dominio, nombre in PORTALES.items():
            if dominio.lower() in host:
                return nombre
    except Exception:
        pass
    return "Otro"
```

Habría que agregar el caso de test correspondiente en
`tests/test_portal_detector.py` (`test_url_sin_protocolo_no_se_reconoce_actualmente`
pasaría a testear el comportamiento corregido) al aplicar el fix.

from urllib.parse import urlparse

PORTALES = {
    "linkedin.com":       "LinkedIn",
    "indeed.com":         "Indeed",
    "trabajando.com":     "Trabajando.com",
    "bumeran.com":        "Bumeran",
    "getonbrd.com":       "Get on Board",
    "laborum.com":        "Laborum",
    "glassdoor.com":      "Glassdoor",
    "computrabajo.com":   "Computrabajo",
    "InfoJobs.net":       "InfoJobs",
    "hired.com":          "Hired",
}

def detectar_portal(url: str) -> str:
    """Recibe una URL y retorna el nombre del portal si lo reconoce."""
    if not url or url.strip() == "":
        return ""
    try:
        host = urlparse(url).netloc.lower().replace("www.", "")
        for dominio, nombre in PORTALES.items():
            if dominio.lower() in host:
                return nombre
    except Exception:
        pass
    return "Otro"
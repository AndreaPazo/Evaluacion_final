# ============================================================
# Módulo: mesa_partes/utilidades.py
# Responsable: Integrante 2
# Función: pedir el trámite y sus datos adicionales (lo usan recepción física y virtual).
# ============================================================

from data.tramites import TRAMITES
from mesa_partes.documentos import validar_n_orden
from servicios.entradas import leer_opcion, leer_texto


def seleccionar_tramite():
    """Devuelve (nombre_tramite, subtipo, clave_tramite) o (None, None, None) si cancela."""
    opciones = {k: v["nombre"] for k, v in TRAMITES.items()}
    clave = leer_opcion("Tipo de trámite:", opciones)
    if clave is None:
        return None, None, None
    tramite = TRAMITES[clave]
    subtipo = None
    if tramite["subtipos"]:
        sub = leer_opcion(f"Tipo de {tramite['nombre'].lower()}:", tramite["subtipos"])
        if sub is None:
            return None, None, None
        subtipo = tramite["subtipos"][sub]
    return tramite["nombre"], subtipo, clave


def pedir_datos_adicionales(clave_tramite):
    """Pide los campos extra del trámite (área donde laboró, N° de orden, firma)."""
    datos = {}
    for clave, etiqueta in TRAMITES[clave_tramite]["campos"]:
        if clave == "firma":
            eleccion = leer_opcion("Tipo de firma:", {"1": "MANUSCRITA", "2": "DIGITAL"}, cancelar=False)
            datos[clave] = "MANUSCRITA" if eleccion == "1" else "DIGITAL"
        elif clave == "n_orden":
            datos[clave] = pedir_n_orden(etiqueta)
        else:
            datos[clave] = leer_texto(etiqueta).upper()
    return datos


def pedir_n_orden(etiqueta):
    """Repite hasta que el N° de orden tenga el formato 0002999-2026-ENTIDAD."""
    while True:
        n_orden = leer_texto(etiqueta).upper()
        if validar_n_orden(n_orden):
            return n_orden
        print("[ERROR] Formato incorrecto. Debe ser 7 dígitos-año-siglas (ejemplo: 0002999-2026-ENTIDAD).")

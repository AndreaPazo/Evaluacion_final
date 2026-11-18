# ============================================================
# Módulo: mesa_partes/recepcion_virtual.py
# Responsable: Integrante 2
# Función: recibir documentos por la casilla electrónica (canal virtual).
# Lo usan Mesa de Partes (con el documento del ciudadano) y el propio ciudadano
# (opción "Nueva solicitud" de su casilla).
# ============================================================

from data.personas import buscar_persona_por_documento, codigo_casilla
from data.usuarios import buscar_usuario_por_persona
from mesa_partes.documentos import registrar_documento
from mesa_partes.utilidades import pedir_datos_adicionales, seleccionar_tramite
from servicios.entradas import (
    leer_opcion,
    leer_texto,
    pedir_adjunto_pdf,
    pedir_folios,
    pedir_numero_documento,
    pedir_tipo_documento,
)


def validar_casilla(persona):
    """La casilla existe solo si la persona tiene una cuenta de usuario. Devuelve el código o None."""
    if persona is None or buscar_usuario_por_persona(persona["id_persona"]) is None:
        return None
    return codigo_casilla(persona["id_persona"])


def generar_constancia_virtual(exp):
    """Imprime la constancia de recepción virtual."""
    print("\n" + "=" * 40)
    print(" SOLICITUD REGISTRADA - CASILLA ELECTRÓNICA")
    print("=" * 40)
    print(f"Constancia : {exp['codigo_constancia']}")
    print(f"Expediente : {exp['codigo']}")
    print(f"Casilla    : {exp['casilla']}")
    print(f"Trámite    : {exp['tramite']}")
    print(f"Estado     : {exp['estado']}")
    print("=" * 40)


def _capturar_y_registrar(persona, usuario):
    """Pide los datos del trámite virtual y registra el expediente."""
    casilla = validar_casilla(persona)
    if casilla is None:
        print("[ERROR] La persona no tiene casilla electrónica (necesita una cuenta de usuario).")
        return None
    tramite, subtipo, clave = seleccionar_tramite()
    if tramite is None:
        return None
    asunto = leer_texto("Asunto digital")
    folios = pedir_folios("Cantidad de folios digitales")
    datos = pedir_datos_adicionales(clave)
    adjunto = pedir_adjunto_pdf()

    if leer_opcion("¿Confirmar envío?", {"1": "Sí", "2": "No"}, cancelar=False) == "2":
        print("Envío cancelado.")
        return None

    exp, errores = registrar_documento(
        persona,
        "VIRTUAL",
        tramite,
        subtipo,
        asunto,
        folios,
        datos,
        usuario,
        casilla=casilla,
        adjunto=adjunto,
    )
    if errores:
        print("\n[ERROR] No se pudo registrar el trámite virtual:")
        for err in errores:
            print(f"- {err}")
        return None
    generar_constancia_virtual(exp)
    return exp


def registrar_documento_virtual(sesion):
    """Mesa de Partes registra un documento virtual indicando el documento del ciudadano."""
    print("\n--- INGRESO CANAL VIRTUAL ---")
    tipo_doc = pedir_tipo_documento()
    num_doc = pedir_numero_documento(tipo_doc, "Número de documento del ciudadano")
    persona = buscar_persona_por_documento(tipo_doc, num_doc)
    if persona is None:
        print("[ERROR] La persona no está registrada.")
        return None
    return _capturar_y_registrar(persona, sesion["usuario"])


def enviar_solicitud_virtual(sesion, persona):
    """El propio ciudadano envía su solicitud desde su casilla."""
    print("\n--- ENVÍO DE SOLICITUD (CASILLA ELECTRÓNICA) ---")
    return _capturar_y_registrar(persona, sesion["usuario"])


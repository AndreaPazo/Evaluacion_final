# ============================================================
# Módulo: mesa_partes/recepcion_fisica.py
# Responsable: Integrante 2
# Función: recibir documentos que el ciudadano entrega en papel.
# ============================================================

from autenticacion.registro import pedir_datos_persona
from data.personas import buscar_persona_por_documento
from mesa_partes.documentos import registrar_documento
from mesa_partes.utilidades import pedir_datos_adicionales, seleccionar_tramite
from servicios.entradas import (
    leer_opcion,
    leer_texto,
    pedir_folios,
    pedir_numero_documento,
    pedir_tipo_documento,
)


def generar_constancia_fisica(exp):
    """Imprime el cargo de recepción que se entrega al ciudadano."""
    print("\n" + "=" * 40)
    print(" CARGO DE RECEPCIÓN - MESA DE PARTES FÍSICA")
    print("=" * 40)
    print(f"Constancia : {exp['codigo_constancia']}")
    print(f"Expediente : {exp['codigo']}")
    print(f"Solicitante: {exp['administrado']}")
    print(f"Trámite    : {exp['tramite']}  | Folios: {exp['folios']}")
    print(f"Fecha      : {exp['fecha_registro']}")
    print("=" * 40)


def registrar_documento_fisico(sesion):
    """Pide los datos del documento en papel y crea el expediente. Devuelve el expediente o None."""
    print("\n--- INGRESO CANAL FÍSICO ---")
    tipo_doc = pedir_tipo_documento()
    num_doc = pedir_numero_documento(tipo_doc)
    persona = buscar_persona_por_documento(tipo_doc, num_doc)

    if persona is None:
        print("La persona no está registrada en la data maestra.")
        if (
            leer_opcion(
                "¿Desea registrarla ahora?", {"1": "Sí", "2": "No"}, cancelar=False
            )
            == "2"
        ):
            return None
        persona = pedir_datos_persona(tipo_doc, num_doc)
        if persona is None:
            return None

    tramite, subtipo, clave = seleccionar_tramite()
    if tramite is None:
        return None
    asunto = leer_texto("Asunto del trámite")
    folios = pedir_folios()
    datos = pedir_datos_adicionales(clave)

    exp, errores = registrar_documento(
        persona,
        "FISICO",
        tramite,
        subtipo,
        asunto,
        folios,
        datos,
        sesion["usuario"],
    )
    if errores:
        print("\n[ERROR] No se pudo registrar el documento:")
        for err in errores:
            print(f"- {err}")
        return None
    print(
        f"\n[OK] Expediente físico creado: {exp['codigo']} | Estado: {exp['estado']}"
    )
    generar_constancia_fisica(exp)
    return exp
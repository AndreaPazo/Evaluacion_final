# ============================================================
# Módulo: funcionario/procesamiento.py
# Responsable: Integrante 3
# Función: operaciones que cambian el estado de un expediente.
#
# Estados:  RECIBIDO -> DERIVADO -> EN_PROCESO -> OBSERVADO -> SUBSANADO
#           -> ATENDIDO -> ARCHIVADO        (y RECIBIDO -> ANULADO)
# Cada operación guarda el cambio, anota el historial y notifica al ciudadano.
# ============================================================

from data.expedientes import guardar_expedientes
from servicios.historial import registrar_historial
from servicios.notificaciones import (notificar_derivacion, notificar_observacion,
                                      notificar_subsanacion, notificar_atencion,
                                      notificar_archivo)


def cambiar_estado(expediente, nuevo_estado, usuario=""):
    """Cambia el estado y deja el movimiento en el historial."""
    anterior = expediente["estado"]
    expediente["estado"] = nuevo_estado
    registrar_historial(expediente, "CAMBIO DE ESTADO", f"{anterior} -> {nuevo_estado}", usuario)


def esta_cerrado(expediente):
    """True si el expediente ya no admite cambios (anulado o archivado)."""
    return expediente["estado"] in ("ANULADO", "ARCHIVADO")


def aceptar(expediente, usuario):
    """RECIBIDO/DERIVADO -> EN_PROCESO. Devuelve (True/False, mensaje)."""
    if expediente["estado"] == "RECIBIDO":
        return False, "Mesa de Partes todavía no deriva este expediente."
    if expediente["estado"] != "DERIVADO":
        return False, "El expediente no puede aceptarse en su estado actual."
    cambiar_estado(expediente, "EN_PROCESO", usuario)
    return True, "Expediente aceptado. Estado: EN_PROCESO"


def derivar(expediente, area_destino, usuario):
    """Envía el expediente a otra área. Devuelve (True/False, mensaje)."""
    if esta_cerrado(expediente):
        return False, "El expediente está cerrado y no se puede derivar."
    if area_destino == expediente["area"]:
        return False, "El expediente ya pertenece a esa área."
    expediente["area"] = area_destino
    cambiar_estado(expediente, "DERIVADO", usuario)
    notificar_derivacion(expediente)
    return True, "Expediente derivado a: " + area_destino


def registrar_observacion(expediente, motivo, usuario):
    """EN_PROCESO/SUBSANADO -> OBSERVADO. Devuelve (True/False, mensaje)."""
    if expediente["estado"] not in ("EN_PROCESO", "SUBSANADO"):
        return False, "No se puede observar en el estado actual."
    expediente["observacion"] = motivo
    cambiar_estado(expediente, "OBSERVADO", usuario)
    notificar_observacion(expediente)
    return True, "Documento observado correctamente."


def registrar_subsanacion(expediente, detalle, usuario):
    """OBSERVADO -> SUBSANADO. Lo registra el ciudadano (o el funcionario si lo entregó en papel)."""
    if expediente["estado"] != "OBSERVADO":
        return False, "El expediente no está observado."
    expediente["subsanacion"] = detalle
    cambiar_estado(expediente, "SUBSANADO", usuario)
    notificar_subsanacion(expediente)
    return True, "Subsanación registrada correctamente."


def registrar_respuesta(expediente, respuesta, usuario):
    """Guarda la respuesta del funcionario y la anota en el historial."""
    expediente["respuesta"] = respuesta
    registrar_historial(expediente, "RESPUESTA", respuesta, usuario)


def atender(expediente, respuesta, usuario):
    """EN_PROCESO/SUBSANADO -> ATENDIDO. Devuelve (True/False, mensaje)."""
    if expediente["estado"] not in ("EN_PROCESO", "SUBSANADO"):
        return False, "El expediente debe estar en proceso o subsanado."
    if not respuesta.strip():
        return False, "La respuesta no puede estar vacía."
    registrar_respuesta(expediente, respuesta.strip(), usuario)
    cambiar_estado(expediente, "ATENDIDO", usuario)
    notificar_atencion(expediente)
    return True, "Expediente atendido correctamente."


def finalizar_expediente(expediente, usuario):
    """ATENDIDO -> ARCHIVADO. Devuelve (True/False, mensaje)."""
    if expediente["estado"] == "ARCHIVADO":
        return False, "El expediente ya está archivado."
    if expediente["estado"] != "ATENDIDO":
        return False, "Primero debes atender el expediente."
    cambiar_estado(expediente, "ARCHIVADO", usuario)
    notificar_archivo(expediente)
    guardar_expedientes()
    return True, "Expediente archivado correctamente."

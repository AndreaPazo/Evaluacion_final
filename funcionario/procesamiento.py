# ============================================================
# Módulo: funcionario/procesamiento.py
# Responsable: Integrante 3
# Función: operaciones que cambian el estado de un expediente.
# ============================================================

from data.conexion import transaccion
from data.expedientes import guardar_expediente
from servicios.historial import registrar_historial
from servicios.notificaciones import (notificar_derivacion, notificar_observacion,
                                      notificar_subsanacion, notificar_atencion,
                                      notificar_archivo)


def cambiar_estado(expediente, nuevo_estado, usuario=""):
    """Cambia el estado y registra el movimiento en el historial en UNA sola transacción."""
    anterior = expediente["estado"]
    expediente["estado"] = nuevo_estado
    try:
        with transaccion() as cur:
            guardar_expediente(expediente, cursor=cur)
            registrar_historial(
                expediente,
                "CAMBIO DE ESTADO",
                f"{anterior} -> {nuevo_estado}",
                usuario,
                cursor=cur,
            )
    except Exception:
        expediente["estado"] = anterior
        raise


def esta_cerrado(expediente):
    """True si el expediente ya no admite cambios (anulado o archivado)."""
    return expediente["estado"] in ("ANULADO", "ARCHIVADO")


def aceptar(expediente, usuario):
    """DERIVADO -> EN_PROCESO. Devuelve (True/False, mensaje)."""
    if expediente["estado"] == "RECIBIDO":
        return False, "Mesa de Partes todavía no deriva este expediente."
    if expediente["estado"] != "DERIVADO":
        return False, "El expediente no puede aceptarse en su estado actual."
    cambiar_estado(expediente, "EN_PROCESO", usuario)
    return True, "Expediente aceptado. Estado: EN_PROCESO"


def derivar(expediente, area_destino, usuario, motivo=""):
    """Envía el expediente a otra área exigiendo motivo y guardando origen, destino y motivo."""
    if esta_cerrado(expediente):
        return False, "El expediente está cerrado y no se puede derivar."
    if area_destino == expediente["area"]:
        return False, "El expediente ya pertenece a esa área."
    motivo_limpio = "" if motivo is None else str(motivo).strip()
    if not motivo_limpio:
        return False, "Debe ingresar el motivo de la derivación."

    origen = expediente["area"]
    estado_anterior = expediente["estado"]
    expediente["area"] = area_destino
    expediente["estado"] = "DERIVADO"
    try:
        with transaccion() as cur:
            guardar_expediente(expediente, cursor=cur)
            registrar_historial(
                expediente,
                "DERIVACION",
                f"Origen: {origen} -> Destino: {area_destino} | Motivo: {motivo_limpio}",
                usuario,
                cursor=cur,
            )
    except Exception:
        expediente["area"] = origen
        expediente["estado"] = estado_anterior
        raise

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
    with transaccion() as cur:
        guardar_expediente(expediente, cursor=cur)
        registrar_historial(expediente, "RESPUESTA", respuesta, usuario, cursor=cur)


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
    return True, "Expediente archivado correctamente."
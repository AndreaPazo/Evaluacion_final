# ============================================================
# Módulo: servicios/notificaciones.py  (COMPARTIDO)
# Responsable: Integrante 4
# Función: crear y consultar las notificaciones de la casilla electrónica en SQL Server.
# ============================================================

from datetime import datetime
from data.conexion import obtener_conexion, transaccion
from data.expedientes import formatear_fecha
from data.personas import codigo_casilla

_SELECT_NOTIF = (
    "SELECT n.IdNotificacion, n.IdPersona, e.Codigo, n.Tipo, n.Mensaje, n.Fecha, n.Leida "
    "FROM dbo.Notificacion n "
    "LEFT JOIN dbo.Expediente e ON e.IdExpediente = n.IdExpediente"
)


def _a_diccionario(fila):
    return {
        "id_notificacion": fila[0],
        "id_persona": fila[1],
        "codigo_expediente": fila[2],
        "tipo": fila[3],
        "mensaje": fila[4],
        "fecha": formatear_fecha(fila[5]),
        "leida": bool(fila[6]),
    }


def crear_notificacion(id_persona, mensaje, codigo_expediente=None, tipo="GENERAL"):
    """Guarda una notificación nueva (sin leer) en dbo.Notificacion y la devuelve."""
    tipo_sql = "GENERAL" if not tipo or tipo.upper() == "INFORMACION" else tipo.upper()
    ahora_dt = datetime.now()

    with transaccion() as cur:
        id_exp = None
        if codigo_expediente:
            cur.execute("SELECT IdExpediente FROM dbo.Expediente WHERE Codigo = ?", (codigo_expediente,))
            fila_exp = cur.fetchone()
            id_exp = fila_exp[0] if fila_exp else None

        cur.execute(
            "INSERT INTO dbo.Notificacion (IdPersona, IdExpediente, Tipo, Mensaje, Fecha, Leida) "
            "OUTPUT INSERTED.IdNotificacion "
            "VALUES (?, ?, ?, ?, ?, 0)",
            (id_persona, id_exp, tipo_sql, mensaje, ahora_dt),
        )
        id_notif = cur.fetchone()[0]

    return {
        "id_notificacion": id_notif,
        "id_persona": id_persona,
        "codigo_expediente": codigo_expediente,
        "tipo": tipo_sql,
        "mensaje": mensaje,
        "fecha": formatear_fecha(ahora_dt),
        "leida": False,
    }


def enviar_notificacion(id_persona, mensaje, codigo_expediente=None, tipo="GENERAL"):
    """Crea la notificación y simula el envío por consola."""
    n = crear_notificacion(id_persona, mensaje, codigo_expediente, tipo)
    print(f"  ✓ NOTIFICACIÓN ENVIADA a la casilla {codigo_casilla(id_persona)} "
          f"(N.º {n['id_notificacion']}, {n['tipo']})")
    return n


def listar_notificaciones(id_persona):
    """Notificaciones de una persona."""
    con = obtener_conexion()
    try:
        cur = con.cursor()
        cur.execute(_SELECT_NOTIF + " WHERE n.IdPersona = ? ORDER BY n.Fecha DESC, n.IdNotificacion DESC", (id_persona,))
        return [_a_diccionario(f) for f in cur.fetchall()]
    finally:
        con.close()


def listar_todas():
    """Todas las notificaciones del sistema."""
    con = obtener_conexion()
    try:
        cur = con.cursor()
        cur.execute(_SELECT_NOTIF + " ORDER BY n.IdNotificacion ASC")
        return [_a_diccionario(f) for f in cur.fetchall()]
    finally:
        con.close()


def contar_no_leidas(id_persona):
    """Cantidad de notificaciones sin leer de una persona."""
    con = obtener_conexion()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM dbo.Notificacion WHERE IdPersona = ? AND Leida = 0",
            (id_persona,),
        )
        return cur.fetchone()[0]
    finally:
        con.close()


def marcar_leida(id_notificacion, id_persona):
    """Marca como leída una notificación de esa persona. True si la encontró."""
    with transaccion() as cur:
        cur.execute(
            "UPDATE dbo.Notificacion SET Leida = 1 WHERE IdNotificacion = ? AND IdPersona = ?",
            (id_notificacion, id_persona),
        )
        return cur.rowcount > 0


# --- Una función por cada hito del trámite ---
def _notificar(exp, mensaje, tipo):
    return enviar_notificacion(exp["id_persona"], mensaje, exp["codigo"], tipo)


def notificar_registro(exp):
    return _notificar(exp, f"Su solicitud de {exp['tramite']} fue recibida. "
                           f"Se generó el expediente {exp['codigo']}.", "REGISTRO")


def notificar_derivacion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue derivado a {exp['area']}.", "DERIVACION")


def notificar_observacion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue OBSERVADO: {exp.get('observacion', '')}. "
                           "Ingrese a su casilla para subsanar.", "OBSERVACION")


def notificar_subsanacion(exp):
    return _notificar(exp, f"Se registró la subsanación del expediente {exp['codigo']}.", "SUBSANACION")


def notificar_atencion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue ATENDIDO.", "ATENCION")


def notificar_archivo(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue ARCHIVADO.", "ARCHIVO")


def notificar_anulacion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue ANULADO. "
                           f"Motivo: {exp['motivo_anulacion']}.", "ANULACION")

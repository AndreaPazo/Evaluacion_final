# Función: expedientes guardados en SQL Server (dbo.Expediente).
# Cada función devuelve el MISMO diccionario de siempre (con JOIN a Persona,
# Tramite, Subtipo, Area y Usuario), así los demás módulos no cambian.

from datetime import datetime
from uuid import uuid4

from data.conexion import obtener_conexion, transaccion
from data.personas import codigo_casilla

ESTADOS = ["RECIBIDO", "DERIVADO", "EN_PROCESO", "OBSERVADO",
           "SUBSANADO", "ATENDIDO", "ARCHIVADO", "ANULADO"]

FORMATO_FECHA = "%d/%m/%Y %H:%M"

# Consulta base: une el expediente con su persona, trámite, subtipo, área y usuario
# para devolver los NOMBRES (la tabla Expediente solo guarda los Id).
_SELECT = (
    "SELECT e.IdExpediente, e.Codigo, e.CodigoConstancia, e.IdPersona, p.TipoDocumento, "
    "p.NumeroDocumento, p.Nombres, p.Apellidos, e.Canal, t.Nombre, s.Nombre, a.Nombre, "
    "e.Asunto, e.Folios, e.Adjunto, e.Estado, e.FechaRegistro, u.NombreUsuario, "
    "e.MotivoAnulacion, e.Observacion, e.Subsanacion, e.Respuesta, e.FechaCierre, "
    "e.AreaLaboro, e.NumeroOrden, e.TipoFirma "
    "FROM dbo.Expediente e "
    "JOIN dbo.Persona p ON p.IdPersona = e.IdPersona "
    "JOIN dbo.Tramite t ON t.IdTramite = e.IdTramite "
    "LEFT JOIN dbo.SubtipoTramite s ON s.IdTramite = e.IdTramite AND s.IdSubtipo = e.IdSubtipo "
    "JOIN dbo.Area a ON a.IdArea = e.IdArea "
    "JOIN dbo.Usuario u ON u.IdUsuario = e.IdUsuarioRegistro"
)


# Funciones internas

def ahora():
    """Fecha y hora actual como texto: 'dd/mm/aaaa hh:mm'."""
    return datetime.now().strftime(FORMATO_FECHA)

def formatear_fecha(valor):
    """Convierte una fecha de la base (datetime) al texto 'dd/mm/aaaa hh:mm'."""
    if valor is None:
        return None
    if isinstance(valor, str):
        return valor
    return valor.strftime(FORMATO_FECHA)

def _a_diccionario(f):
    """Convierte una fila de _SELECT en el diccionario de expediente."""
    datos_adicionales = {}
    if f[23] is not None:
        datos_adicionales["area_laboro"] = f[23]
    if f[24] is not None:
        datos_adicionales["n_orden"] = f[24]
    if f[25] is not None:
        datos_adicionales["firma"] = f[25]
    exp = {
        "id_expediente": f[0],
        "codigo": f[1],
        "codigo_constancia": f[2],
        "id_persona": f[3],
        "tipo_identificacion": f[4],
        "numero_identificacion": f[5],
        "administrado": f[6] + " " + f[7],
        "canal": f[8],
        "casilla": codigo_casilla(f[3]) if f[8] == "VIRTUAL" else None,
        "tramite": f[9],
        "subtipo": f[10],
        "area": f[11],
        "asunto": f[12],
        "folios": f[13],
        "datos_adicionales": datos_adicionales,
        "adjunto": f[14],
        "estado": f[15],
        "fecha_registro": formatear_fecha(f[16]),
        "registrado_por": f[17],
        "motivo_anulacion": f[18],
        "anulado": f[15] == "ANULADO",
        "historial": [],
    }
    # Estos campos solo existen cuando tienen valor (igual que antes).
    for clave, valor in (("observacion", f[19]), ("subsanacion", f[20]),
                         ("respuesta", f[21]), ("fecha_cierre", formatear_fecha(f[22]))):
        if valor is not None:
            exp[clave] = valor
    return exp

def _cargar_historiales(cursor, expedientes):
    """Llena exp['historial'] de todos los expedientes con UNA sola consulta."""
    if not expedientes:
        return
    por_id = {e["id_expediente"]: e for e in expedientes}
    cursor.execute(
        "SELECT h.IdExpediente, h.Fecha, h.Accion, h.Detalle, u.NombreUsuario "
        "FROM dbo.HistorialExpediente h LEFT JOIN dbo.Usuario u ON u.IdUsuario = h.IdUsuario "
        "ORDER BY h.IdHistorial"
    )
    for id_exp, fecha, accion, detalle, usuario in cursor.fetchall():
        if id_exp in por_id:
            por_id[id_exp]["historial"].append({
                "fecha": formatear_fecha(fecha),
                "accion": accion,
                "detalle": detalle or "",
                "usuario": usuario or "",
            })

def _consultar(where="", parametros=()):
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute(_SELECT + where + " ORDER BY e.IdExpediente", parametros)
        lista = [_a_diccionario(f) for f in cursor.fetchall()]
        _cargar_historiales(cursor, lista)
        return lista
    finally:
        con.close()

# Funciones públicas

def cargar_expedientes():
    """Comprueba la conexión y devuelve cuántos expedientes hay en la base."""
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.Expediente")
        return cursor.fetchone()[0]
    finally:
        con.close()

def guardar_expediente(exp, cursor=None):
    """Guarda en la base los campos que pueden cambiar (estado, área, textos).
    Si recibe un cursor, usa la transacción de quien lo llama."""
    if exp["estado"] == "ARCHIVADO" and not exp.get("fecha_cierre"):
        exp["fecha_cierre"] = ahora()
    cierre = None
    if exp.get("fecha_cierre"):
        cierre = datetime.strptime(exp["fecha_cierre"], "%d/%m/%Y %H:%M")
    sql = ("UPDATE dbo.Expediente SET Estado = ?, IdArea = (SELECT IdArea FROM dbo.Area WHERE Nombre = ?), "
           "MotivoAnulacion = ?, Observacion = ?, Subsanacion = ?, Respuesta = ?, FechaCierre = ? "
           "WHERE IdExpediente = ?")
    parametros = (exp["estado"], exp["area"], exp.get("motivo_anulacion"), exp.get("observacion"),
                  exp.get("subsanacion"), exp.get("respuesta"), cierre, exp["id_expediente"])
    if cursor is not None:
        cursor.execute(sql, parametros)
        return
    with transaccion() as cur:
        cur.execute(sql, parametros)

def crear_expediente(datos):
    """Inserta el expediente, genera el código EXP-AAAA-NNNNNN (correlativo, no se repite)
    y la constancia CONST-AAAA-NNNNNN. Devuelve el expediente completo."""
    ahora_dt = datetime.now()
    temporal = "TMP" + uuid4().hex[:16]          # se reemplaza en la misma transacción
    adicionales = datos.get("datos_adicionales") or {}
    with transaccion() as cursor:
        cursor.execute(
            "INSERT INTO dbo.Expediente (Codigo, CodigoConstancia, IdPersona, IdTramite, IdSubtipo, "
            "IdArea, Canal, Asunto, Folios, Adjunto, Estado, FechaRegistro, IdUsuarioRegistro, "
            "AreaLaboro, NumeroOrden, TipoFirma) "
            "OUTPUT INSERTED.IdExpediente "
            "VALUES (?, NULL, ?, "
            "(SELECT IdTramite FROM dbo.Tramite WHERE Nombre = ?), "
            "(SELECT s.IdSubtipo FROM dbo.SubtipoTramite s JOIN dbo.Tramite t ON t.IdTramite = s.IdTramite "
            "  WHERE t.Nombre = ? AND s.Nombre = ?), "
            "(SELECT IdArea FROM dbo.Area WHERE Nombre = ?), "
            "?, ?, ?, ?, 'RECIBIDO', ?, "
            "(SELECT IdUsuario FROM dbo.Usuario WHERE NombreUsuario = ?), ?, ?, ?)",
            (temporal, datos["id_persona"], datos["tramite"], datos["tramite"], datos.get("subtipo"),
             datos["area"], datos["canal"], datos["asunto"], datos.get("folios"), datos.get("adjunto"),
             ahora_dt, datos["registrado_por"], adicionales.get("area_laboro"),
             adicionales.get("n_orden"), adicionales.get("firma")),
        )
        id_exp = cursor.fetchone()[0]
        codigo = "EXP-%d-%06d" % (ahora_dt.year, id_exp)
        cursor.execute(
            "UPDATE dbo.Expediente SET Codigo = ?, CodigoConstancia = ? WHERE IdExpediente = ?",
            (codigo, "CONST-%d-%06d" % (ahora_dt.year, id_exp), id_exp),
        )
    return buscar_expediente(codigo)

def buscar_expediente(codigo):
    """Busca por código (acepta minúsculas). Devuelve el expediente o None."""
    lista = _consultar(" WHERE e.Codigo = ?", (codigo.strip().upper(),))
    return lista[0] if lista else None

def listar_expedientes():
    """Devuelve todos los expedientes (en el orden en que se registraron)."""
    return _consultar()

def listar_expedientes_persona(id_persona):
    """Expedientes que pertenecen a una persona."""
    return _consultar(" WHERE e.IdPersona = ?", (id_persona,))

def actualizar_expediente(codigo, **cambios):
    """Cambia campos de un expediente y guarda. Devuelve el expediente o None."""
    exp = buscar_expediente(codigo)
    if exp is None:
        return None
    exp.update(cambios)
    guardar_expediente(exp)
    return exp

# ============================================================
# Módulo: servicios/historial.py  (COMPARTIDO por los 4 integrantes)
# Función: registrar y mostrar los movimientos de un expediente en SQL Server.
# ============================================================

from datetime import datetime
from data.conexion import obtener_conexion, transaccion
from data.expedientes import formatear_fecha


def _resolver_id_expediente(cursor, exp):
    if exp.get("id_expediente"):
        return exp["id_expediente"]
    cursor.execute("SELECT IdExpediente FROM dbo.Expediente WHERE Codigo = ?", (exp["codigo"],))
    fila = cursor.fetchone()
    return fila[0] if fila else None


def _resolver_id_usuario(cursor, usuario):
    if not usuario:
        return None
    cursor.execute(
        "SELECT IdUsuario FROM dbo.Usuario WHERE LOWER(NombreUsuario) = ?",
        (str(usuario).strip().lower(),),
    )
    fila = cursor.fetchone()
    return fila[0] if fila else None


def registrar_historial(exp, accion, detalle="", usuario="", cursor=None):
    """Inserta un movimiento en dbo.HistorialExpediente.
    Si recibe un cursor, usa la transacción de quien lo llama."""
    ahora_dt = datetime.now()

    def _insertar(cur):
        id_exp = _resolver_id_expediente(cur, exp)
        if id_exp is None:
            raise ValueError(f"No se encontró el expediente {exp.get('codigo')} en la base de datos.")
        id_usr = _resolver_id_usuario(cur, usuario)
        cur.execute(
            "INSERT INTO dbo.HistorialExpediente (IdExpediente, Fecha, Accion, Detalle, IdUsuario) "
            "VALUES (?, ?, ?, ?, ?)",
            (id_exp, ahora_dt, accion, detalle or None, id_usr),
        )

    if cursor is not None:
        _insertar(cursor)
    else:
        with transaccion() as cur:
            _insertar(cur)

    # Mantiene sincronizada la lista en memoria del diccionario
    exp.setdefault("historial", []).append({
        "fecha": formatear_fecha(ahora_dt),
        "accion": accion,
        "detalle": detalle or "",
        "usuario": usuario or "",
    })


def listar_historial(exp):
    """Consulta los movimientos del expediente con JOIN a dbo.Usuario."""
    con = obtener_conexion()
    try:
        cur = con.cursor()
        id_exp = _resolver_id_expediente(cur, exp)
        if id_exp is None:
            return []
        cur.execute(
            "SELECT h.Fecha, h.Accion, h.Detalle, u.NombreUsuario "
            "FROM dbo.HistorialExpediente h "
            "LEFT JOIN dbo.Usuario u ON u.IdUsuario = h.IdUsuario "
            "WHERE h.IdExpediente = ? "
            "ORDER BY h.IdHistorial ASC",
            (id_exp,),
        )
        return [
            {
                "fecha": formatear_fecha(f[0]),
                "accion": f[1],
                "detalle": f[2] or "",
                "usuario": f[3] or "",
            }
            for f in cur.fetchall()
        ]
    finally:
        con.close()


def ver_historial(exp):
    """Muestra en pantalla todos los movimientos de un expediente."""
    movimientos = listar_historial(exp)
    exp["historial"] = movimientos
    print(f"\nHISTORIAL - {exp['codigo']}")
    print("-" * 48)
    if not movimientos:
        print("  Sin movimientos registrados.")
    for mov in movimientos:
        print(mov["fecha"])
        detalle = f" | {mov['detalle']}" if mov["detalle"] else ""
        print(f"  {mov['accion']}{detalle}")
        if mov["usuario"]:
            print(f"  Usuario: {mov['usuario']}")
    print("-" * 48)

    
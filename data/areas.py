# Función: las áreas de la entidad, leídas de dbo.Area (SQL Server).
# AREAS es una lista que se llena con cargar_areas() al iniciar el sistema.

from data.conexion import obtener_conexion

AREAS = []

def _consultar(sql, parametros=()):
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        con.close()

def cargar_areas():
    """Lee dbo.Area y llena la lista AREAS (sin cambiar el objeto lista)."""
    filas = _consultar("SELECT Nombre FROM dbo.Area ORDER BY IdArea")
    AREAS[:] = [fila[0] for fila in filas]
    return AREAS

def listar_areas():
    """Muestra las áreas numeradas en pantalla."""
    if not AREAS:
        cargar_areas()
    print("\n===== ÁREAS DISPONIBLES =====")
    for numero, area in enumerate(AREAS, start=1):
        print(f"{numero}. {area}")

def buscar_area(nombre):
    """Devuelve el área si existe (sin importar mayúsculas), o None."""
    if not AREAS:
        cargar_areas()
    for area in AREAS:
        if area == nombre.strip().upper():
            return area
    return None

def determinar_area_por_tramite(tramite):
    """Enrutamiento automático: devuelve el área responsable del trámite, o None."""
    filas = _consultar(
        "SELECT a.Nombre FROM dbo.Tramite t JOIN dbo.Area a ON a.IdArea = t.IdArea "
        "WHERE UPPER(t.Nombre) = ?",
        (tramite.strip().upper(),),
    )
    return filas[0][0] if filas else None

def listar_funcionarios_por_area(usuarios, area):
    """Filtra una lista de usuarios y devuelve los FUNCIONARIOS de un área."""
    return [u for u in usuarios if u["rol"] == "FUNCIONARIO" and u.get("area") == area]
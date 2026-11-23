import os
import pyodbc

# Cada equipo se configura con variables de entorno (sin contraseñas en el código).
# Docker:  MESA_PARTES_SQL=localhost,1433  MESA_PARTES_USUARIO=sa  MESA_PARTES_CLAVE=...
# Windows: no hace falta configurar nada.
SERVIDOR = os.environ.get("MESA_PARTES_SQL", r"localhost\SQLEXPRESS")
USUARIO = os.environ.get("MESA_PARTES_USUARIO")
CLAVE = os.environ.get("MESA_PARTES_CLAVE", "")
BASE_DATOS = "MesaPartes"


class ErrorConexion(Exception):
    """Excepción lanzada cuando no se puede conectar a SQL Server."""
    pass


def _obtener_driver():
    drivers = pyodbc.drivers()
    for favorito in ("ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"):
        if favorito in drivers:
            return favorito
    return "SQL Server"


def obtener_conexion(base_datos=BASE_DATOS):
    driver = _obtener_driver()
    cadena = (
        f"DRIVER={{{driver}}};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={base_datos};"
        "TrustServerCertificate=yes;"
    )
    if USUARIO:
        cadena += f"UID={USUARIO};PWD={CLAVE};"     # Docker: usuario de SQL Server
    else:
        cadena += "Trusted_Connection=yes;"          # Windows: usuario de Windows
    try:
        return pyodbc.connect(cadena, timeout=5)
    except pyodbc.Error as err:
        raise ErrorConexion(
            f"No se pudo conectar a la base de datos en {SERVIDOR}: {err}"
        ) from err

    @contextmanager
    def transaccion(base_datos=None):
    #Abre una conexión en modo transacción: hace commit al terminar o rollback si hay error."""
     con = obtener_conexion(base_datos)
     con.autocommit = False
    try:
        cursor = con.cursor()
        yield cursor
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
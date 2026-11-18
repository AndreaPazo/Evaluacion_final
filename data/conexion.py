import pyodbc

SERVIDOR = r"localhost\SQLEXPRESS"
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
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    try:
        return pyodbc.connect(cadena, timeout=5)
    except pyodbc.Error as err:
        raise ErrorConexion("No se pudo conectar a la base de datos") from err

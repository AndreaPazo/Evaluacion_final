from data.conexion import obtener_conexion

CANALES = {
    "1": "FISICO",
    "2": "VIRTUAL",
}

TIPOS_IDENTIDAD = {"1": "DNI", "2": "CE", "3": "RUC"}

CAMPOS_CONSTANCIA = [
    ("area_laboro", "Área/Dirección donde laboró"),
    ("n_orden", "N° Orden de Servicio/Contrato (ej. 0002999-2026-ENTIDAD)"),
    ("firma", "Firma (1=MANUSCRITA, 2=DIGITAL)"),
]


TRAMITES = {}


def cargar_tramites():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT IdTramite, Nombre, PideDatosAdicionales "
            "FROM dbo.Tramite ORDER BY IdTramite"
        )
        nuevos = {}
        for id_tramite, nombre, pide_datos in cursor.fetchall():
            clave = str(id_tramite)
            nuevos[clave] = {
                "nombre": nombre,
                "subtipos": {},
                "campos": list(CAMPOS_CONSTANCIA) if pide_datos else [],
            }

        cursor.execute(
            "SELECT IdTramite, IdSubtipo, Nombre "
            "FROM dbo.SubtipoTramite ORDER BY IdTramite, IdSubtipo"
        )
        for id_tramite, id_subtipo, nombre_sub in cursor.fetchall():
            clave_t = str(id_tramite)
            if clave_t in nuevos:
                nuevos[clave_t]["subtipos"][str(id_subtipo)] = nombre_sub

        TRAMITES.clear()
        TRAMITES.update(nuevos)
    finally:
        conexion.close()
    return TRAMITES

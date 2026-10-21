# Módulo: data/tramites.py
# Responsable: Integrante 2 (Wanda) - Mesa de Partes
# Catálogo de los 5 trámites, sus subtipos y los datos adicionales que exige cada uno.

CANALES = {
    "1": "FISICO",
    "2": "VIRTUAL",
}

TIPOS_IDENTIDAD = {"1": "DNI", "2": "CE", "3": "RUC"}

# Campos adicionales: (clave, etiqueta). Salen del caso real observado
# (Solicitud de Constancia de Prestación de Servicios - ENTIDAD).
CAMPOS_CONSTANCIA = [
    ("area_laboro", "Área/Dirección donde laboró"),
    ("n_orden", "N° Orden de Servicio/Contrato (ej. 0002999-2026-ENTIDAD)"),
    ("firma", "Firma (1=MANUSCRITA, 2=DIGITAL)"),
]

TRAMITES = {
    "1": {"nombre": "LICENCIA", "subtipos": {"1": "CON GOCE", "2": "SIN GOCE"}, "campos": []},
    "2": {"nombre": "DESCANSO MEDICO", "subtipos": {}, "campos": []},
    "3": {"nombre": "CONSTANCIA DE TRABAJO", "subtipos": {}, "campos": CAMPOS_CONSTANCIA},
    "4": {"nombre": "SOLICITUD DE ORDEN DE SERVICIOS", "subtipos": {}, "campos": CAMPOS_CONSTANCIA},
    "5": {"nombre": "REPROGRAMACION DE VACACIONES", "subtipos": {}, "campos": []},
}

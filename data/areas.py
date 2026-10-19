
AREAS = [
    "RECURSOS HUMANOS",
    "ABASTECIMIENTO",
    "SERVICIOS AL USUARIO",
    "PRESUPUESTO PUBLICO",
    "FINANZAS",
]

# Relación entre cada trámite y su área responsable
AREAS_POR_TRAMITE = {
    "LICENCIA": "RECURSOS HUMANOS",
    "DESCANSO MEDICO": "RECURSOS HUMANOS",
    "CONSTANCIA DE TRABAJO": "RECURSOS HUMANOS",
    "REPROGRAMACION DE VACACIONES": "RECURSOS HUMANOS",
    "SOLICITUD DE ORDEN DE SERVICIOS": "ABASTECIMIENTO",
}

def listar_areas():
    """Muestra las áreas numeradas en pantalla."""
    print("\n===== ÁREAS DISPONIBLES =====")
    for numero, area in enumerate(AREAS, start=1):
        print(f"{numero}. {area}")


def buscar_area(nombre):
    """Devuelve el área si existe (sin importar mayúsculas), o None."""
    for area in AREAS:
        if area == nombre.strip().upper():
            return area
    return None


def determinar_area_por_tramite(tramite):
    """Devuelve el área responsable de un trámite, o None."""
    return AREAS_POR_TRAMITE.get(tramite.strip().upper())


def listar_funcionarios_por_area(usuarios, area):
    """Filtra una lista de usuarios y devuelve los FUNCIONARIOS de un área."""
    return [u for u in usuarios if u["rol"] == "FUNCIONARIO" and u.get("area") == area]


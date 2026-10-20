# ============================================================
# Módulo: personas.py
# Responsable: Integrante 1
# Función: registrar, buscar, modificar, listar y activar/desactivar
#          personas (DNI, CE o RUC).
# Los datos se guardan en data/base_personas.py (formato Python).
# ============================================================

import os

from data.almacen import cargar_lista, guardar_lista

ARCHIVO_PERSONAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_personas.py")
VARIABLE = "PERSONAS"
TIPOS_DOCUMENTO = ("DNI", "CE", "RUC")


# ------------------------------------------------------------
# Funciones internas (empiezan con _ : no se usan desde afuera)
# ------------------------------------------------------------
def _cargar_personas():
    """Lee la lista de personas guardada."""
    return cargar_lista(ARCHIVO_PERSONAS, VARIABLE)


def _guardar_personas(personas):
    """Guarda la lista completa de personas."""
    guardar_lista(ARCHIVO_PERSONAS, VARIABLE, personas)


def _texto(valor):
    """Convierte cualquier valor en texto sin espacios sobrantes (None -> '')."""
    return "" if valor is None else str(valor).strip()


def _correo_valido(correo):
    """Revisa un formato básico de correo: algo@dominio.ext"""
    if correo.count("@") != 1 or " " in correo:
        return False
    usuario, dominio = correo.split("@")
    return bool(usuario) and "." in dominio and not dominio.startswith(".") and not dominio.endswith(".")


# ------------------------------------------------------------
# Funciones públicas
# ------------------------------------------------------------
def formato_id(id_persona):
    """Devuelve el ID con seis dígitos. Ejemplo: 1 -> '000001'."""
    return str(id_persona).zfill(6)


def codigo_casilla(id_persona):
    """Código de la casilla electrónica de la persona. Ejemplo: 1 -> 'CE-000001'."""
    return "CE-" + formato_id(id_persona)


def validar_documento(tipo_documento, numero):
    """Comprueba el formato del documento.

    DNI: 8 dígitos | RUC: 11 dígitos | CE: 1 letra y 7 dígitos.
    """
    tipo = _texto(tipo_documento).upper()
    numero = _texto(numero)
    if tipo == "DNI":
        return numero.isdigit() and len(numero) == 8
    if tipo == "RUC":
        return numero.isdigit() and len(numero) == 11
    if tipo == "CE":
        # CE: exactamente 8 caracteres donde el primero es letra y los 7 siguientes son dígitos
        return len(numero) == 8 and numero[0].isalpha() and numero[1:].isdigit()
    return False


def buscar_persona_por_documento(tipo_documento, numero):
    """Busca por tipo y número de documento. Devuelve la persona o None."""
    tipo = _texto(tipo_documento).upper()
    numero = _texto(numero).upper()
    for persona in _cargar_personas():
        if persona["tipo_documento"] == tipo and persona["numero_documento"].upper() == numero:
            return persona
    return None


def buscar_persona(id_persona):
    """Busca una persona por su ID interno. Devuelve la persona o None."""
    for persona in _cargar_personas():
        if persona["id_persona"] == id_persona:
            return persona
    return None


def registrar_persona(tipo_documento, numero_documento, nombres, apellidos, correo, telefono):
    """Valida los datos y registra una persona.

    Devuelve (persona, mensaje). Si hay un error, persona es None.
    """
    tipo = _texto(tipo_documento).upper()
    numero = _texto(numero_documento).upper()
    nombres = _texto(nombres)
    apellidos = _texto(apellidos)
    correo = _texto(correo)
    telefono = _texto(telefono)

    if not validar_documento(tipo, numero):
        return None, "Documento inválido. DNI: 8 dígitos; RUC: 11 dígitos; CE: 1 letra y 7 dígitos."
    if buscar_persona_por_documento(tipo, numero):
        return None, "Ya existe una persona con ese tipo y número de documento."
    if not nombres or not apellidos:
        return None, "Los nombres y apellidos son obligatorios."
    if not _correo_valido(correo):
        return None, "Ingrese un correo válido (ejemplo: nombre@dominio.com)."
    if not telefono:
        return None, "El teléfono es obligatorio."

    personas = _cargar_personas()
    # El ID se genera solo: el mayor ID existente + 1.
    nuevo_id = max([p["id_persona"] for p in personas], default=0) + 1
    persona = {
        "id_persona": nuevo_id,
        "tipo_documento": tipo,
        "numero_documento": numero,
        "nombres": nombres,
        "apellidos": apellidos,
        "correo": correo,
        "telefono": telefono,
        "estado": "ACTIVO",
    }
    personas.append(persona)
    _guardar_personas(personas)
    return persona, "Persona registrada correctamente."


def modificar_persona(id_persona, nombres=None, apellidos=None, correo=None, telefono=None):
    """Cambia solo los campos indicados. El documento no se modifica.

    Devuelve (True/False, mensaje).
    """
    personas = _cargar_personas()
    for persona in personas:
        if persona["id_persona"] == id_persona:
            nuevos = {
                "nombres": _texto(nombres),
                "apellidos": _texto(apellidos),
                "correo": _texto(correo),
                "telefono": _texto(telefono),
            }
            if nuevos["correo"] and not _correo_valido(nuevos["correo"]):
                return False, "El correo no tiene un formato válido."
            for campo, valor in nuevos.items():
                if valor:  # los campos vacíos se dejan como estaban
                    persona[campo] = valor
            _guardar_personas(personas)
            return True, "Persona modificada correctamente."
    return False, "No se encontró la persona."


def cambiar_estado_persona(id_persona, estado):
    """Marca a la persona como ACTIVO o INACTIVO (no se borra el registro)."""
    estado = _texto(estado).upper()
    if estado not in ("ACTIVO", "INACTIVO"):
        return False, "Estado no válido."
    personas = _cargar_personas()
    for persona in personas:
        if persona["id_persona"] == id_persona:
            persona["estado"] = estado
            _guardar_personas(personas)
            return True, f"Persona actualizada: {estado}."
    return False, "No se encontró la persona."


def activar_persona(id_persona):
    """Activa una persona."""
    return cambiar_estado_persona(id_persona, "ACTIVO")


def desactivar_persona(id_persona):
    """Desactiva una persona."""
    return cambiar_estado_persona(id_persona, "INACTIVO")


def listar_personas():
    """Devuelve todas las personas registradas."""
    return _cargar_personas()
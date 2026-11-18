# Función: registrar, buscar, modificar, listar y activar/desactivar
# personas (DNI, CE o RUC).

import pyodbc
from data.conexion import obtener_conexion

TIPOS_DOCUMENTO = ("DNI", "CE", "RUC")

# Columnas de dbo.Persona, en el orden que espera _a_diccionario()
_COLUMNAS = "IdPersona, TipoDocumento, NumeroDocumento, Nombres, Apellidos, Correo, Telefono, Estado"

# Funciones internas (empiezan con _ : no se usan desde afuera)
def _ejecutar(sql, parametros=(), uno=False, todos=False, guardar=False):
    """Ejecuta una consulta y cierra la conexión al terminar.

    uno=True    -> devuelve una fila (o None)
    todos=True  -> devuelve una lista de filas
    guardar=True -> confirma los cambios (INSERT / UPDATE)
    Si no se pide uno ni todos, devuelve cuántas filas se modificaron.
    """
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        if parametros:
            cursor.execute(sql, parametros)
        else:
            cursor.execute(sql)
        if uno:
            resultado = cursor.fetchone()
        elif todos:
            resultado = cursor.fetchall()
        else:
            resultado = cursor.rowcount
        if guardar:
            con.commit()
        return resultado
    finally:
        con.close()


def _a_diccionario(fila):
    """Convierte una fila de dbo.Persona en el diccionario de siempre."""
    if fila is None:
        return None
    return {
        "id_persona": fila[0],
        "tipo_documento": fila[1],
        "numero_documento": fila[2],
        "nombres": fila[3],
        "apellidos": fila[4],
        "correo": fila[5],
        "telefono": fila[6].strip(),
        "estado": fila[7],
    }

def _texto(valor):
    """Convierte cualquier valor en texto sin espacios sobrantes (None -> '')."""
    return "" if valor is None else str(valor).strip()

# Funciones públicas
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

def telefono_valido(telefono):
       """Celular: 9 dígitos y empieza con 9."""
       return telefono.isdigit() and len(telefono) == 9 and telefono.startswith("9")

def solo_letras(texto):
    """Nombres y apellidos: solo letras, espacios, guiones y apóstrofes."""
    return bool(texto) and all(c.isalpha() or c in (" ", "-", "'") for c in texto)

def correo_valido(correo):
    """Revisa un formato básico de correo: algo@dominio.ext"""
    if correo.count("@") != 1 or " " in correo:
        return False
    usuario, dominio = correo.split("@")
    return bool(usuario) and "." in dominio and not dominio.startswith(".") and not dominio.endswith(".")

# Funciones públicas: consultas a dbo.Persona

def buscar_persona_por_documento(tipo_documento, numero):
    """Busca por tipo y número de documento. Devuelve la persona o None."""
    fila = _ejecutar(
        f"SELECT {_COLUMNAS} FROM dbo.Persona WHERE TipoDocumento = ? AND UPPER(NumeroDocumento) = ?",
        (_texto(tipo_documento).upper(), _texto(numero).upper()),
        uno=True,
    )
    return _a_diccionario(fila)
    
def buscar_persona(id_persona):
    """Busca una persona por su ID interno. Devuelve la persona o None."""
    fila = _ejecutar(f"SELECT {_COLUMNAS} FROM dbo.Persona WHERE IdPersona = ?", (id_persona,), uno=True)
    return _a_diccionario(fila)

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
    if not solo_letras(nombres) or not solo_letras(apellidos):
        return None, "Los nombres y apellidos son obligatorios y solo pueden tener letras."
    if not correo_valido(correo):
        return None, "Ingrese un correo válido (ejemplo: nombre@dominio.com)."
    if not telefono_valido(telefono):
        return None, "Teléfono inválido. Debe tener 9 dígitos y empezar con 9."

    try:
        # El ID lo genera SQL Server (IDENTITY); OUTPUT INSERTED lo devuelve.
        fila = _ejecutar(
            "INSERT INTO dbo.Persona (TipoDocumento, NumeroDocumento, Nombres, Apellidos, Correo, Telefono, Estado) "
            "OUTPUT INSERTED.IdPersona VALUES (?, ?, ?, ?, ?, ?, 'ACTIVO')",
            (tipo, numero, nombres, apellidos, correo, telefono),
            uno=True,
            guardar=True,
        )
    except pyodbc.IntegrityError:
        # La restricción UNIQUE de la tabla es la última barrera contra duplicados.
        return None, "Ya existe una persona con ese tipo y número de documento."
    return buscar_persona(fila[0]), "Persona registrada correctamente."

def modificar_persona(id_persona, nombres=None, apellidos=None, correo=None, telefono=None):
    """Cambia solo los campos indicados. El documento no se modifica.
    Devuelve (True/False, mensaje).
    """
    
    if buscar_persona(id_persona) is None:
        return False, "No se encontró la persona."
    nuevos = {
        "nombres": _texto(nombres),
        "apellidos": _texto(apellidos),
        "correo": _texto(correo),
        "telefono": _texto(telefono),
    }
    if not any(nuevos.values()):  # los 4 campos llegaron vacíos
        return False, "No se realizaron cambios."
    for campo in ("nombres", "apellidos"):
        if nuevos[campo] and not solo_letras(nuevos[campo]):
            return False, f"Los {campo} solo pueden tener letras y espacios."
    if nuevos["correo"] and not correo_valido(nuevos["correo"]):
        return False, "El correo no tiene un formato válido."
    if nuevos["telefono"] and not telefono_valido(nuevos["telefono"]):
        return False, "Teléfono inválido. Debe tener 9 dígitos y empezar con 9."
    
    # Solo se actualizan las columnas que llegaron con valor (las vacías se dejan como estaban).
    columnas = [columna for columna, valor in nuevos.items() if valor]
    asignaciones = ", ".join(f"{columna} = ?" for columna in columnas)
    valores = [nuevos[columna] for columna in columnas] + [id_persona]
    _ejecutar(f"UPDATE dbo.Persona SET {asignaciones} WHERE IdPersona = ?", valores, guardar=True)
    return True, "Persona modificada correctamente."

def cambiar_estado_persona(id_persona, estado):
    """Marca a la persona como ACTIVO o INACTIVO (no se borra el registro)."""
    estado = _texto(estado).upper()
    if estado not in ("ACTIVO", "INACTIVO"):
        return False, "Estado no válido."
    filas = _ejecutar("UPDATE dbo.Persona SET Estado = ? WHERE IdPersona = ?", (estado, id_persona), guardar=True)
    if filas == 0:
        return False, "No se encontró la persona."
    return True, f"Persona actualizada: {estado}."

def activar_persona(id_persona):
    """Activa una persona."""
    return cambiar_estado_persona(id_persona, "ACTIVO")

def desactivar_persona(id_persona):
    """Desactiva una persona."""
    return cambiar_estado_persona(id_persona, "INACTIVO")

def listar_personas():
    """Devuelve todas las personas registradas."""
    filas = _ejecutar(f"SELECT {_COLUMNAS} FROM dbo.Persona ORDER BY IdPersona", todos=True)
    return [_a_diccionario(fila) for fila in filas]
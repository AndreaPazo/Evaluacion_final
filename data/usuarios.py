# Función: crear usuarios, asignar roles y activar/desactivar cuentas.
# Cada usuario está vinculado a una persona (id_persona).

import hashlib
import hmac
import os

import pyodbc
from data.conexion import obtener_conexion

ROLES_VALIDOS = ("ADMINISTRADOR", "MESA_PARTES", "FUNCIONARIO", "CIUDADANO")
LARGO_MINIMO_CONTRASENA = 6
ITERACIONES = 100_000  # veces que se repite el cálculo de la huella (más = más seguro)

# Columnas que devuelve cada consulta, en el orden que espera _a_diccionario().
# El LEFT JOIN trae el nombre del área; los usuarios sin área (IdArea NULL) devuelven ''.
_SELECT_USUARIO = (
    "SELECT u.IdUsuario, u.IdPersona, u.NombreUsuario, u.ContrasenaHash, u.Rol, "
    "ISNULL(a.Nombre, ''), u.Estado "
    "FROM dbo.Usuario u LEFT JOIN dbo.Area a ON a.IdArea = u.IdArea"
)

# ------------------------------------------------------------
# Funciones internas
# ------------------------------------------------------------
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
    """Convierte una fila de la consulta en el diccionario de siempre."""
    if fila is None:
        return None
    return {
        "id_usuario": fila[0],
        "id_persona": fila[1],
        "nombre_usuario": fila[2],
        "contrasena_hash": fila[3],
        "rol": fila[4],
        "area": fila[5],
        "estado": fila[6],
    }

def _cargar_usuarios():
    """Lee las cuentas guardadas."""
    filas = _ejecutar(_SELECT_USUARIO + " ORDER BY u.IdUsuario", todos=True)
    return [_a_diccionario(fila) for fila in filas]

def _texto(valor):
    """Convierte cualquier valor en texto sin espacios sobrantes (None -> '')."""
    return "" if valor is None else str(valor).strip()

def _nombres_areas():
    """Nombres de las áreas registradas en dbo.Area."""
    return [fila[0] for fila in _ejecutar("SELECT Nombre FROM dbo.Area ORDER BY IdArea", todos=True)]

def _id_area(nombre_area):
    """Devuelve el IdArea de un área por su nombre, o None si no existe."""
    fila = _ejecutar("SELECT IdArea FROM dbo.Area WHERE Nombre = ?", (_texto(nombre_area).upper(),), uno=True)
    return fila[0] if fila else None

def _hash_contrasena(contrasena, sal=None):
    """Convierte la contraseña en una huella con 'sal' aleatoria.
    Se guarda como 'sal$huella'. Nunca se guarda la contraseña legible.
    """
    if sal is None:
        sal = os.urandom(16).hex()
    huella = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), bytes.fromhex(sal), ITERACIONES)
    return sal + "$" + huella.hex()

def _contrasena_correcta(contrasena, guardada):
    """Compara la contraseña escrita con la huella guardada."""
    try:
        sal, _ = guardada.split("$")
        return hmac.compare_digest(_hash_contrasena(contrasena, sal), guardada)
    except ValueError:
        return False

def _sin_huella(usuario):
    """Copia de la cuenta SIN la contraseña (para mostrar o devolver)."""
    return {k: v for k, v in usuario.items() if k != "contrasena_hash"}

def _queda_sin_administrador(usuarios, usuario):
    """True si este usuario es el único ADMINISTRADOR activo."""
    if usuario["rol"] != "ADMINISTRADOR" or usuario["estado"] != "ACTIVO":
        return False
    otros = _ejecutar(
        "SELECT COUNT(*) FROM dbo.Usuario WHERE Rol = 'ADMINISTRADOR' AND Estado = 'ACTIVO' AND IdUsuario <> ?",
        (usuario["id_usuario"],),
        uno=True,
    )[0]
    return otros == 0

# ------------------------------------------------------------
# Funciones públicas
# ------------------------------------------------------------
def buscar_usuario(nombre_usuario):
    """Busca una cuenta por nombre de usuario (sin distinguir mayúsculas). None si no existe.
    El resultado incluye la huella; no lo muestre en pantalla.
    """
    fila = _ejecutar(
        _SELECT_USUARIO + " WHERE LOWER(u.NombreUsuario) = ?",
        (_texto(nombre_usuario).lower(),),
        uno=True,
    )
    return _a_diccionario(fila)

def buscar_usuario_por_persona(id_persona):
    """Busca la cuenta vinculada a un ID de persona. None si no tiene."""
    fila = _ejecutar(_SELECT_USUARIO + " WHERE u.IdPersona = ?", (id_persona,), uno=True)
    return _a_diccionario(fila)

def hay_usuarios():
    """True si ya existe al menos una cuenta."""
    return _ejecutar("SELECT COUNT(*) FROM dbo.Usuario", uno=True)[0] > 0

def registrar_usuario(id_persona, nombre_usuario, contrasena, rol, area=""):
    """Crea una cuenta para una persona ya registrada.
    Si el rol es FUNCIONARIO, `area` es obligatoria (debe existir en data/areas.py).
    Devuelve (usuario_sin_huella, mensaje). Si hay error, usuario es None.
    """
    # Se importa aquí para evitar dependencias circulares entre módulos.
    from data.personas import buscar_persona

    nombre_usuario = _texto(nombre_usuario)
    rol = _texto(rol).upper()
    area = _texto(area).upper()
    contrasena = "" if contrasena is None else str(contrasena)

    if not isinstance(id_persona, int) or id_persona < 1:
        return None, "El ID de persona debe ser un número entero positivo."
    if buscar_persona(id_persona) is None:
        return None, "La persona no existe. Regístrela primero."
    if not nombre_usuario or " " in nombre_usuario:
        return None, "El nombre de usuario es obligatorio y no puede tener espacios."
    if len(contrasena) < LARGO_MINIMO_CONTRASENA:
        return None, f"La contraseña debe tener al menos {LARGO_MINIMO_CONTRASENA} caracteres."
    if rol not in ROLES_VALIDOS:
        return None, "Rol no válido. Roles: " + ", ".join(ROLES_VALIDOS) + "."
    id_area = None  # solo los funcionarios tienen área
    if rol == "FUNCIONARIO":
        id_area = _id_area(area)
        if id_area is None:
            return None, "El FUNCIONARIO necesita un área válida: " + ", ".join(_nombres_areas()) + "."
    if rol != "FUNCIONARIO":
        area = ""  # solo los funcionarios tienen área
    if buscar_usuario(nombre_usuario):
        return None, "Ese nombre de usuario ya está registrado."
    if buscar_usuario_por_persona(id_persona):
        return None, "Esta persona ya tiene una cuenta de usuario."

    try:
        fila = _ejecutar(
            "INSERT INTO dbo.Usuario (IdPersona, NombreUsuario, ContrasenaHash, Rol, IdArea, Estado) "
            "OUTPUT INSERTED.IdUsuario VALUES (?, ?, ?, ?, ?, 'ACTIVO')",
            (id_persona, nombre_usuario, _hash_contrasena(contrasena), rol, id_area),
            uno=True,
            guardar=True,
        )
    except pyodbc.IntegrityError:
        # Las restricciones UNIQUE de la tabla son la última barrera contra duplicados.
        return None, "Ese nombre de usuario o esa persona ya tienen una cuenta."
    return _sin_huella(buscar_usuario(nombre_usuario)), "Usuario creado correctamente."

def validar_credenciales(nombre_usuario, contrasena):
    """Devuelve la cuenta (sin huella) si usuario y contraseña son correctos y la cuenta está ACTIVA."""
    usuario = buscar_usuario(nombre_usuario)
    if usuario is None or usuario["estado"] != "ACTIVO":
        return None
    if _contrasena_correcta("" if contrasena is None else str(contrasena), usuario["contrasena_hash"]):
        return _sin_huella(usuario)
    return None

def modificar_usuario(nombre_usuario, nuevo_nombre=None, nueva_contrasena=None):
    """Cambia el nombre de usuario y/o la contraseña. Devuelve (True/False, mensaje)."""
    usuario = buscar_usuario(nombre_usuario)
    if usuario is None:
        return False, "No se encontró el usuario."
    nombre_limpio = _texto(nuevo_nombre)
    clave = "" if nueva_contrasena is None else str(nueva_contrasena)

    # Se valida TODO primero, para no guardar cambios a medias.
    if nombre_limpio:
        if " " in nombre_limpio:
            return False, "El nombre de usuario no puede tener espacios."
        otro = buscar_usuario(nombre_limpio)
        if otro is not usuario and otro["id_usuario"] != usuario["id_usuario"]:
            return False, "El nuevo nombre de usuario ya está registrado."
    if clave and len(clave) < LARGO_MINIMO_CONTRASENA:
        return False, f"La contraseña debe tener al menos {LARGO_MINIMO_CONTRASENA} caracteres."

    cambios, valores = [], []
    if nombre_limpio:
        cambios.append("NombreUsuario = ?")
        valores.append(nombre_limpio)
    if clave:
        cambios.append("ContrasenaHash = ?")
        valores.append(_hash_contrasena(clave))
    if cambios:
        _ejecutar(
            f"UPDATE dbo.Usuario SET {', '.join(cambios)} WHERE IdUsuario = ?",
            valores + [usuario["id_usuario"]],
            guardar=True,
        )
    return True, "Usuario modificado correctamente."
    
def asignar_rol(nombre_usuario, nuevo_rol, area=""):
    """Cambia el rol de una cuenta (si el rol es FUNCIONARIO hay que indicar el área).
    Devuelve (True/False, mensaje).
    """
    nuevo_rol = _texto(nuevo_rol).upper()
    if nuevo_rol not in ROLES_VALIDOS:
        return False, "Rol no válido. Roles: " + ", ".join(ROLES_VALIDOS) + "."
    usuarios = _cargar_usuarios()
    if usuario is None:
        return False, "No se encontró el usuario."
    if nuevo_rol != "ADMINISTRADOR" and _queda_sin_administrador(usuario):
        return False, "No se puede cambiar el rol del único administrador activo."
    id_area = None
    if nuevo_rol == "FUNCIONARIO":
        id_area = _id_area(area)
        if id_area is None:
            return False, "El FUNCIONARIO necesita un área válida: " + ", ".join(_nombres_areas()) + "."
    _ejecutar(
        "UPDATE dbo.Usuario SET Rol = ?, IdArea = ? WHERE IdUsuario = ?",
        (nuevo_rol, id_area, usuario["id_usuario"]),
        guardar=True,
    )
    return True, "Rol actualizado correctamente."
    
def cambiar_estado_usuario(nombre_usuario, estado):
    """Activa o desactiva una cuenta sin borrarla. Devuelve (True/False, mensaje)."""
    estado = _texto(estado).upper()
    if estado not in ("ACTIVO", "INACTIVO"):
        return False, "Estado no válido."
    usuario = buscar_usuario(nombre_usuario)
    if usuario is None:
        return False, "No se encontró el usuario."
    if estado == "INACTIVO" and _queda_sin_administrador(usuario):
        return False, "No se puede desactivar al único administrador activo."
    _ejecutar("UPDATE dbo.Usuario SET Estado = ? WHERE IdUsuario = ?", (estado, usuario["id_usuario"]), guardar=True)
    return True, f"Usuario actualizado: {estado}."
  
def activar_usuario(nombre_usuario):
    """Activa una cuenta."""
    return cambiar_estado_usuario(nombre_usuario, "ACTIVO")

def desactivar_usuario(nombre_usuario):
    """Desactiva una cuenta."""
    return cambiar_estado_usuario(nombre_usuario, "INACTIVO")

def listar_usuarios():
    """Lista las cuentas sin mostrar las contraseñas."""
    return [_sin_huella(u) for u in _cargar_usuarios()]

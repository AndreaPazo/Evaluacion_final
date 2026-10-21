# ============================================================
# Módulo: usuarios.py
# Responsable: Integrante 1
# Función: crear usuarios, asignar roles y activar/desactivar cuentas.
# Cada usuario está vinculado a una persona (id_persona).
# Los datos se guardan en data/base_usuarios.py (formato Python).
# ============================================================

import hashlib
import hmac
import os

from data.almacen import cargar_lista, guardar_lista
from data.areas import AREAS

ARCHIVO_USUARIOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_usuarios.py")
VARIABLE = "USUARIOS"
ROLES_VALIDOS = ("ADMINISTRADOR", "MESA_PARTES", "FUNCIONARIO", "CIUDADANO")
LARGO_MINIMO_CONTRASENA = 6
ITERACIONES = 100_000  # veces que se repite el cálculo de la huella (más = más seguro)


# ------------------------------------------------------------
# Funciones internas
# ------------------------------------------------------------
def _cargar_usuarios():
    """Lee las cuentas guardadas."""
    return cargar_lista(ARCHIVO_USUARIOS, VARIABLE)


def _guardar_usuarios(usuarios):
    """Guarda todas las cuentas."""
    guardar_lista(ARCHIVO_USUARIOS, VARIABLE, usuarios)


def _texto(valor):
    """Convierte cualquier valor en texto sin espacios sobrantes (None -> '')."""
    return "" if valor is None else str(valor).strip()


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
    otros = [u for u in usuarios if u is not usuario and u["rol"] == "ADMINISTRADOR" and u["estado"] == "ACTIVO"]
    return not otros


# ------------------------------------------------------------
# Funciones públicas
# ------------------------------------------------------------
def buscar_usuario(nombre_usuario):
    """Busca una cuenta por nombre de usuario (sin distinguir mayúsculas). None si no existe.

    El resultado incluye la huella; no lo muestre en pantalla.
    """
    buscado = _texto(nombre_usuario).lower()
    for usuario in _cargar_usuarios():
        if usuario["nombre_usuario"].lower() == buscado:
            return usuario
    return None


def buscar_usuario_por_persona(id_persona):
    """Busca la cuenta vinculada a un ID de persona. None si no tiene."""
    for usuario in _cargar_usuarios():
        if usuario["id_persona"] == id_persona:
            return usuario
    return None


def hay_usuarios():
    """True si ya existe al menos una cuenta."""
    return len(_cargar_usuarios()) > 0


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
    if rol == "FUNCIONARIO" and area not in AREAS:
        return None, "El FUNCIONARIO necesita un área válida: " + ", ".join(AREAS) + "."
    if rol != "FUNCIONARIO":
        area = ""  # solo los funcionarios tienen área
    if buscar_usuario(nombre_usuario):
        return None, "Ese nombre de usuario ya está registrado."
    if buscar_usuario_por_persona(id_persona):
        return None, "Esta persona ya tiene una cuenta de usuario."

    usuarios = _cargar_usuarios()
    nuevo_id = max([u["id_usuario"] for u in usuarios], default=0) + 1
    usuario = {
        "id_usuario": nuevo_id,
        "id_persona": id_persona,
        "nombre_usuario": nombre_usuario,
        "contrasena_hash": _hash_contrasena(contrasena),
        "rol": rol,
        "area": area,
        "estado": "ACTIVO",
    }
    usuarios.append(usuario)
    _guardar_usuarios(usuarios)
    return _sin_huella(usuario), "Usuario creado correctamente."


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
    buscado = _texto(nombre_usuario).lower()
    usuarios = _cargar_usuarios()
    for usuario in usuarios:
        if usuario["nombre_usuario"].lower() == buscado:
            nombre_limpio = _texto(nuevo_nombre)
            clave = "" if nueva_contrasena is None else str(nueva_contrasena)

            # Se valida TODO primero, para no guardar cambios a medias.
            if nombre_limpio:
                if " " in nombre_limpio:
                    return False, "El nombre de usuario no puede tener espacios."
                for otro in usuarios:
                    if otro is not usuario and otro["nombre_usuario"].lower() == nombre_limpio.lower():
                        return False, "El nuevo nombre de usuario ya está registrado."
            if clave and len(clave) < LARGO_MINIMO_CONTRASENA:
                return False, f"La contraseña debe tener al menos {LARGO_MINIMO_CONTRASENA} caracteres."

            if nombre_limpio:
                usuario["nombre_usuario"] = nombre_limpio
            if clave:
                usuario["contrasena_hash"] = _hash_contrasena(clave)
            _guardar_usuarios(usuarios)
            return True, "Usuario modificado correctamente."
    return False, "No se encontró el usuario."


def asignar_rol(nombre_usuario, nuevo_rol, area=""):
    """Cambia el rol de una cuenta (si el rol es FUNCIONARIO hay que indicar el área).

    Devuelve (True/False, mensaje).
    """
    nuevo_rol = _texto(nuevo_rol).upper()
    area = _texto(area).upper()
    if nuevo_rol not in ROLES_VALIDOS:
        return False, "Rol no válido. Roles: " + ", ".join(ROLES_VALIDOS) + "."
    buscado = _texto(nombre_usuario).lower()
    usuarios = _cargar_usuarios()
    for usuario in usuarios:
        if usuario["nombre_usuario"].lower() == buscado:
            if nuevo_rol != "ADMINISTRADOR" and _queda_sin_administrador(usuarios, usuario):
                return False, "No se puede cambiar el rol del único administrador activo."
            if nuevo_rol == "FUNCIONARIO" and area not in AREAS:
                return False, "El FUNCIONARIO necesita un área válida: " + ", ".join(AREAS) + "."
            usuario["rol"] = nuevo_rol
            usuario["area"] = area if nuevo_rol == "FUNCIONARIO" else ""
            _guardar_usuarios(usuarios)
            return True, "Rol actualizado correctamente."
    return False, "No se encontró el usuario."


def cambiar_estado_usuario(nombre_usuario, estado):
    """Activa o desactiva una cuenta sin borrarla. Devuelve (True/False, mensaje)."""
    estado = _texto(estado).upper()
    if estado not in ("ACTIVO", "INACTIVO"):
        return False, "Estado no válido."
    buscado = _texto(nombre_usuario).lower()
    usuarios = _cargar_usuarios()
    for usuario in usuarios:
        if usuario["nombre_usuario"].lower() == buscado:
            if estado == "INACTIVO" and _queda_sin_administrador(usuarios, usuario):
                return False, "No se puede desactivar al único administrador activo."
            usuario["estado"] = estado
            _guardar_usuarios(usuarios)
            return True, f"Usuario actualizado: {estado}."
    return False, "No se encontró el usuario."


def activar_usuario(nombre_usuario):
    """Activa una cuenta."""
    return cambiar_estado_usuario(nombre_usuario, "ACTIVO")


def desactivar_usuario(nombre_usuario):
    """Desactiva una cuenta."""
    return cambiar_estado_usuario(nombre_usuario, "INACTIVO")


def listar_usuarios():
    """Lista las cuentas sin mostrar las contraseñas."""
    return [_sin_huella(u) for u in _cargar_usuarios()]

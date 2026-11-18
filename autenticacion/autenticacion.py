# ============================================================
# Módulo: autenticacion.py
# Responsable: Integrante 1
# Función: iniciar sesión (login), consultar el rol y cerrar sesión (logout).
#
# FLUJO:  persona -> usuario -> login -> sesión (con rol) -> módulo del rol
# La "sesión" es un diccionario. Los demás integrantes lo reciben y usan
# sesion["rol"], sesion["id_persona"], etc.
# ============================================================

from data.personas import buscar_persona
from data.usuarios import validar_credenciales


def login(nombre_usuario, contrasena):
    """Valida usuario y contraseña. Devuelve (sesion, mensaje).

    Si algo falla, sesion es None. El mensaje no revela si falló el
    usuario o la contraseña (así no se ayuda a adivinar cuentas).
    """
    usuario = validar_credenciales(nombre_usuario, contrasena)
    if usuario is None:
        return None, "Acceso denegado: usuario, contraseña o estado incorrecto."

    persona = buscar_persona(usuario["id_persona"])
    if persona is None or persona["estado"] != "ACTIVO":
        return None, "Acceso denegado: la persona no existe o está inactiva."

    sesion = {
        "id_usuario": usuario["id_usuario"],
        "usuario": usuario["nombre_usuario"],
        "rol": usuario["rol"],
        "id_persona": persona["id_persona"],
        "area": usuario.get("area", ""),
        "nombre_completo": persona["nombres"] + " " + persona["apellidos"],
    }
    return sesion, "Inicio de sesión correcto."


def obtener_rol(sesion):
    """Devuelve el rol de la sesión, o None si no hay sesión."""
    if not sesion:
        return None
    return sesion.get("rol")


def tiene_rol(sesion, *roles):
    """True si la sesión tiene alguno de los roles indicados.

    Ejemplo: tiene_rol(sesion, "MESA_PARTES", "ADMINISTRADOR")
    """
    return obtener_rol(sesion) in roles


def logout(sesion):
    """Cierra la sesión. Devuelve (None, mensaje); guarde el None en su variable de sesión."""
    if not sesion:
        return None, "No hay una sesión activa."
    return None, f"Sesión cerrada para {sesion['usuario']}."

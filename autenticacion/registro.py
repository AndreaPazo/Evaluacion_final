# ============================================================
# Módulo: autenticacion/registro.py
# Responsable: Integrante 1
# Función: pantallas de registro (persona, ciudadano y primer administrador).
# ============================================================

from data.areas import AREAS
from data.personas import formato_id, registrar_persona
from data.usuarios import ROLES_VALIDOS, buscar_usuario, hay_usuarios, registrar_usuario
from servicios.entradas import (
    pedir_contrasena,
    pedir_contrasena_registro,
    pedir_correo,
    pedir_nombre_usuario,
    pedir_numero_documento,
    pedir_solo_letras,
    pedir_telefono,
    pedir_tipo_documento,
)


def pedir_datos_persona(tipo=None, numero=None):
    """Pide los datos y registra una persona. Devuelve la persona o None.

    Si ya se conoce el documento (por ejemplo, en recepción física),
    se pasan `tipo` y `numero` y no se vuelven a pedir.
    """
    if tipo is None or numero is None:
        tipo = pedir_tipo_documento()
        numero = pedir_numero_documento(tipo)
    else:
        print(f"Documento: {tipo} {numero}")
    nombres = pedir_solo_letras("Nombres")
    apellidos = pedir_solo_letras("Apellidos")
    correo = pedir_correo("Correo electrónico")
    telefono = pedir_telefono("Teléfono")
    persona, mensaje = registrar_persona(
        tipo, numero, nombres, apellidos, correo, telefono
    )
    print(mensaje)
    if persona:
        print("ID_PERSONA:", formato_id(persona["id_persona"]))
    return persona


def pedir_usuario_disponible():
    """Pide el nombre de usuario y lo repite mientras ya esté en uso."""
    while True:
        nombre_usuario = pedir_nombre_usuario("Nombre de usuario")
        if buscar_usuario(nombre_usuario) is None:
            return nombre_usuario
        print("[ERROR] Ese nombre de usuario ya está en uso. Ingrese otro usuario.")


def crear_usuario_para(persona, rol_fijo=None):
    """Pide usuario, contraseña y rol, y crea la cuenta de `persona`."""
    nombre_usuario = pedir_usuario_disponible()
    contrasena = pedir_contrasena_registro("Contraseña (entre 6 y 10 caracteres)")
    area = ""
    if rol_fijo:
        rol = rol_fijo
    else:
        print("Roles disponibles:", ", ".join(ROLES_VALIDOS))
        rol = input("Rol: ").strip().upper()
        if rol == "FUNCIONARIO":
            print("Áreas disponibles:", ", ".join(AREAS))
            area = input("Área del funcionario: ")
    usuario, mensaje = registrar_usuario(
        persona["id_persona"], nombre_usuario, contrasena, rol, area
    )
    print(mensaje)
    if usuario:
        print("ID_USUARIO:", formato_id(usuario["id_usuario"]))
    return usuario


def registro_ciudadano():
    """Auto-registro: crea la persona y su cuenta con rol CIUDADANO."""
    print("\n--- REGISTRO DE CIUDADANO ---")
    persona = pedir_datos_persona()
    if persona is None:
        return
    if crear_usuario_para(persona, rol_fijo="CIUDADANO") is None:
        print("[ERROR] No se pudo crear la cuenta. Intente registrarse nuevamente.")


def crear_administrador_inicial():
    """Solo funciona si todavía no existe ningún usuario."""
    if hay_usuarios():
        print(
            "Ya existen usuarios. Pida a un administrador que cree nuevas cuentas."
        )
        return
    print("\n--- CREAR ADMINISTRADOR INICIAL ---")
    persona = pedir_datos_persona()
    if persona is None:
        return
    if (
        crear_usuario_para(persona, rol_fijo="ADMINISTRADOR") is None
    ):  # noqa: E501
        print(
            "No se pudo crear la cuenta. Intente de nuevo con la opción 3."
        )
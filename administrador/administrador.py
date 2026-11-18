# ============================================================
# Módulo: administrador/administrador.py
# Responsable: Integrante 1
# Función: panel del ADMINISTRADOR (personas, usuarios, roles, áreas y consulta general).
# ============================================================

from autenticacion.registro import crear_usuario_para, pedir_datos_persona
from data.areas import AREAS, listar_funcionarios_por_area
from data.personas import (
    activar_persona,
    buscar_persona,
    buscar_persona_por_documento,
    desactivar_persona,
    formato_id,
    listar_personas,
    modificar_persona,
)
from data.usuarios import (
    ROLES_VALIDOS,
    activar_usuario,
    asignar_rol,
    buscar_usuario_por_persona,
    desactivar_usuario,
    listar_usuarios,
    modificar_usuario,
)
from servicios.entradas import (
    leer_entero,
    leer_opcion,
    pedir_numero_documento,
    pedir_contrasena_registro,
    pedir_tipo_documento,
)
from servicios.reportes import menu_reporte


def mostrar_persona(persona):
    print(f"  ID_PERSONA : {formato_id(persona['id_persona'])}")
    print(
        f"  Documento  : {persona['tipo_documento']} {persona['numero_documento']}"
    )
    print(f"  Nombre     : {persona['nombres']} {persona['apellidos']}")
    print(f"  Correo     : {persona['correo']}")
    print(f"  Teléfono   : {persona['telefono']}")
    print(f"  Estado     : {persona['estado']}")


def mostrar_usuario(usuario):
    area = f" | área {usuario['area']}" if usuario.get("area") else ""
    print(
        f"  ID_USUARIO {formato_id(usuario['id_usuario'])} | {usuario['nombre_usuario']} | "
        f"rol {usuario['rol']}{area} | persona {formato_id(usuario['id_persona'])} | {usuario['estado']}"
    )


# ---------------- PERSONAS ----------------
def opcion_registrar_persona():
    print("\n--- REGISTRAR PERSONA ---")
    pedir_datos_persona()


def opcion_buscar_persona():
    print("\n--- BUSCAR PERSONA ---")
    print("Buscar por: 1) ID  2) Documento")
    if input("Seleccione: ").strip() == "1":
        id_persona = leer_entero("ID_PERSONA")
        persona = buscar_persona(id_persona) if id_persona is not None else None
    else:
        tipo = pedir_tipo_documento()
        persona = buscar_persona_por_documento(tipo, pedir_numero_documento(tipo))
    if persona:
        mostrar_persona(persona)
    else:
        print("Persona no encontrada.")

def opcion_modificar_persona():
    print("\n--- MODIFICAR PERSONA ---")
    id_persona = leer_entero("ID_PERSONA a modificar")
    if id_persona is None:
        return
    print("Deje un campo vacío si no desea cambiarlo.")
    _, mensaje = modificar_persona(
        id_persona,
        input("Nombres nuevos: "),
        input("Apellidos nuevos: "),
        input("Correo nuevo: "),
        input("Teléfono nuevo: "),
    )
    print(mensaje)

def opcion_listar_personas():
    print("\n--- PERSONAS REGISTRADAS ---")
    personas = listar_personas()
    if not personas:
        print("Todavía no hay personas registradas.")
    for persona in personas:
        mostrar_persona(persona)
        print()


def opcion_estado_persona(activar):
    id_persona = leer_entero("ID_PERSONA")
    if id_persona is None:
        return
    _, mensaje = (activar_persona if activar else desactivar_persona)(id_persona)
    print(mensaje)


# ---------------- USUARIOS ----------------
def opcion_crear_usuario():
    print("\n--- CREAR USUARIO ---")
    tipo = pedir_tipo_documento()
    persona = buscar_persona_por_documento(
        tipo, pedir_numero_documento(tipo, "Número de documento de la persona")
    )
    if persona is None:
        print(
            "No existe una persona con ese documento. Regístrela primero (opción 1)."
        )
        return
    if buscar_usuario_por_persona(persona["id_persona"]):
        print("Esta persona ya tiene una cuenta.")
        return
    crear_usuario_para(persona)


def opcion_listar_usuarios():
    print("\n--- USUARIOS REGISTRADOS ---")
    usuarios = listar_usuarios()
    if not usuarios:
        print("Todavía no hay usuarios registrados.")
    for usuario in usuarios:
        mostrar_usuario(usuario)


def opcion_modificar_usuario():
    print("\n--- MODIFICAR USUARIO ---")
    nombre = input("Nombre de usuario actual: ")
    print("Deje el nombre vacío si no desea cambiarlo.")
    nuevo_nombre = input("Nuevo nombre de usuario: ")
    nueva_contrasena = ""  # vacío = no se cambia
    if leer_opcion("¿Desea cambiar la contraseña?", {"1": "Sí", "2": "No"}, cancelar=False) == "1":
        nueva_contrasena = pedir_contrasena_registro("Nueva contraseña (entre 6 y 10 caracteres)")
    _, mensaje = modificar_usuario(nombre, nuevo_nombre, nueva_contrasena)
    print(mensaje)

def opcion_asignar_rol():
    print("\n--- ASIGNAR / CAMBIAR ROL ---")
    nombre = input("Nombre de usuario: ")
    print("Roles disponibles:", ", ".join(ROLES_VALIDOS))
    rol = input("Nuevo rol: ")
    area = ""
    if rol.strip().upper() == "FUNCIONARIO":
        print("Áreas disponibles:", ", ".join(AREAS))
        area = input("Área del funcionario: ")
    _, mensaje = asignar_rol(nombre, rol, area)
    print(mensaje)


def opcion_estado_usuario(activar):
    nombre = input("Nombre de usuario: ")
    _, mensaje = (activar_usuario if activar else desactivar_usuario)(nombre)
    print(mensaje)


# ---------------- ÁREAS ----------------
def opcion_areas():
    print("\n--- ÁREAS Y FUNCIONARIOS ---")
    usuarios = listar_usuarios()
    for area in AREAS:
        print(area)
        funcionarios = listar_funcionarios_por_area(usuarios, area)
        if not funcionarios:
            print("   (sin funcionarios asignados)")
        for f in funcionarios:
            print("   -", f["nombre_usuario"])


def modulo_administrador_menu(sesion):
    """Punto de entrada del rol ADMINISTRADOR."""
    opciones = {
        "1": ("Registrar persona", opcion_registrar_persona),
        "2": ("Buscar persona", opcion_buscar_persona),
        "3": ("Modificar persona", opcion_modificar_persona),
        "4": ("Listar personas", opcion_listar_personas),
        "5": ("Activar persona", lambda: opcion_estado_persona(True)),
        "6": ("Desactivar persona", lambda: opcion_estado_persona(False)),
        "7": ("Crear usuario", opcion_crear_usuario),
        "8": ("Listar usuarios", opcion_listar_usuarios),
        "9": ("Modificar usuario (nombre/contraseña)", opcion_modificar_usuario),
        "10": ("Asignar/cambiar rol", opcion_asignar_rol),
        "11": ("Activar usuario", lambda: opcion_estado_usuario(True)),
        "12": ("Desactivar usuario", lambda: opcion_estado_usuario(False)),
        "13": ("Áreas y funcionarios", opcion_areas),
        "14": ("Consulta general de expedientes", menu_reporte),
    }
    while True:
        print("\n" + "=" * 48)
        print(f" PANEL DEL ADMINISTRADOR - {sesion['nombre_completo']}")
        print("=" * 48)
        for clave, (texto, _) in opciones.items():
            print(f"{clave}. {texto}")
        print("0. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            return
        if opcion in opciones:
            opciones[opcion][1]()
        else:
            print("Opción incorrecta. Intente nuevamente.")


# Nombre estándar que usa main.py (igual que los demás módulos)
menu_administrador = modulo_administrador_menu
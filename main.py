# FLUJO:
#   1. REGISTRAR persona/usuario  ->  2. LOGIN  ->  3. se identifica el ROL
#   4. el rol entra a su módulo   ->  5. LOGOUT

# ============================================================

from autenticacion.autenticacion import login, logout
from autenticacion.registro import registro_ciudadano
from ciudadano.ciudadano import menu_ciudadano
from data.almacen import ArchivoDanado
from data.expedientes import cargar_expedientes
from data.personas import listar_personas
from data.usuarios import listar_usuarios
from servicios.notificaciones import listar_todas
from mesa_partes.mesa_partes import menu_mesa_partes
from servicios.entradas import pedir_contrasena

# Diccionario que decide a qué módulo entra cada rol.
MODULOS_POR_ROL = {
    "MESA_PARTES": menu_mesa_partes,
    "CIUDADANO": menu_ciudadano,
    "ADMINISTRADOR": None,  # Módulo en construcción
    "FUNCIONARIO": None,    # Módulo en construcción
}


def opcion_login():
    """Inicia sesión, direcciona al módulo del rol correspondiente y gestiona el cierre"""
    print("\n--- INICIAR SESIÓN ---")
    nombre = input("Usuario: ")
    contrasena = pedir_contrasena("Contraseña")
    sesion, mensaje = login(nombre, contrasena)
    print(mensaje)

    if sesion is None:
        return
    
    print(f"Bienvenido/a: {sesion['nombre_completo']} | Rol: {sesion['rol']}")
    
    # Evalúa el rol asignado en la sesión
    if sesion["rol"] in MODULOS_POR_ROL:
        menu_del_rol = MODULOS_POR_ROL[sesion["rol"]]

        if menu_del_rol is None:
            # Las cuentas 'admin' o 'func_*' estan en construcción
            print(f"El módulo del rol {sesion['rol']} todavía está en construcción.")
        else:
            # Ejecuta los módulos terminados (Mesa de Partes o Ciudadano)
            menu_del_rol(sesion)
    else:
        print("\n[ERROR] Rol no reconocido por el sistema de seguridad.")

    sesion, mensaje = logout(sesion)
    print(mensaje)

def menu_principal():

    while True:
        print("\n" + "=" * 48)
        print(" MESA DE PARTES FÍSICA Y VIRTUAL - ENTIDAD")
        print("=" * 48)
        print("1. Iniciar sesión")
        print("2. Registrarse como ciudadano")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_login()
        elif opcion == "2":
            registro_ciudadano()
        elif opcion == "0":
            print("Programa finalizado. Los datos quedan guardados en la carpeta data.")
            return
        else:
            print("Opción incorrecta. Intente nuevamente.")


def iniciar_sistema():
    """Valida la persistencia de datos, monta las estructuras y despliega la UI."""
    # Mecanismo de protección de datos: si un archivo base_*.py está corrupto,
    # el programa se detiene en seco antes de sobrescribir el archivo .bak
    
    listar_personas()
    listar_usuarios()
    listar_todas()
    total = cargar_expedientes()
    print(f"Sistema iniciado. Expedientes cargados: {total}")
    menu_principal()


if __name__ == "__main__":
    try:
        iniciar_sistema()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido. Los datos guardados no se pierden.")
    except ArchivoDanado as error:
        print("\n[ERROR GRAVE] " + str(error))
        print("El programa se detuvo para no borrar sus datos.")
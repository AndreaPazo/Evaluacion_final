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
}


def opcion_login():
    """Inicia sesión, entra al módulo del rol y al salir hace logout."""
    print("\n--- INICIAR SESIÓN ---")
    nombre = input("Usuario: ")
    contrasena = pedir_contrasena("Contraseña")
    sesion, mensaje = login(nombre, contrasena)
    print(mensaje)
    if sesion is None:
        return
    print(f"Bienvenido/a: {sesion['nombre_completo']} | Rol: {sesion['rol']}")
    menu_del_rol = MODULOS_POR_ROL.get(sesion["rol"])
    if menu_del_rol is None:
        print(f"El módulo del rol {sesion['rol']} todavía está en construcción.")
    else:
        menu_del_rol(sesion)
    sesion, mensaje = logout(sesion)
    print(mensaje)


def menu_principal():
    """Menú inicial: se repite hasta que la persona elija salir."""
    while True:
        print("\n" + "=" * 48)
        print(" MESA DE PARTES FÍSICA Y VIRTUAL")
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
    """Revisa los archivos de datos, carga los expedientes y abre el menú principal."""
    # Leer todos los archivos al inicio: si alguno está dañado, el programa
    # se detiene ANTES de que se guarde algo encima.
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
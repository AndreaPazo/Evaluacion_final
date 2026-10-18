# ============================================================
# Proyecto: Mesa de Partes Física y Virtual - MEF (prototipo educativo)
# Archivo : main.py  (ÚNICO main del proyecto, integra a los 4 integrantes)
#
# Ejecutar desde esta carpeta:   python main.py
#
# FLUJO:
#   1. REGISTRAR persona/usuario  ->  2. LOGIN  ->  3. se identifica el ROL
#   4. el rol entra a su módulo   ->  5. LOGOUT
#
#   ADMINISTRADOR -> administrador/   (Integrante 1)
#   MESA_PARTES   -> mesa_partes/     (Integrante 2)
#   FUNCIONARIO   -> funcionario/     (Integrante 3)
#   CIUDADANO     -> ciudadano/       (Integrante 4)
#
# Los datos son "en duro": listas y diccionarios guardados en archivos
# data/base_*.py (sin base de datos SQL).
# ============================================================

from administrador.administrador import menu_administrador
from autenticacion.autenticacion import login, logout
from autenticacion.registro import registro_ciudadano, crear_administrador_inicial
from ciudadano.ciudadano import menu_ciudadano
from data.expedientes import cargar_expedientes
from data.usuarios import hay_usuarios
from funcionario.funcionario import menu_funcionario
from mesa_partes.mesa_partes import menu_mesa_partes
from servicios.entradas import pedir_contrasena

# Diccionario que decide a qué módulo entra cada rol.
MODULOS_POR_ROL = {
    "ADMINISTRADOR": menu_administrador,
    "MESA_PARTES": menu_mesa_partes,
    "FUNCIONARIO": menu_funcionario,
    "CIUDADANO": menu_ciudadano,
}


def opcion_login():
    """Inicia sesión, entra al módulo del rol y al salir hace logout."""
    print("\n--- INICIAR SESIÓN ---")
    nombre = input("Usuario: ")
    contrasena = pedir_contrasena("Contraseña: ")
    sesion, mensaje = login(nombre, contrasena)
    print(mensaje)
    if sesion is None:
        return
    print(f"Bienvenido/a: {sesion['nombre_completo']} | Rol: {sesion['rol']}")
    MODULOS_POR_ROL[sesion["rol"]](sesion)
    sesion, mensaje = logout(sesion)
    print(mensaje)


def menu_principal():
    """Menú inicial: se repite hasta que la persona elija salir."""
    while True:
        print("\n" + "=" * 48)
        print(" MESA DE PARTES FÍSICA Y VIRTUAL - MEF")
        print("=" * 48)
        print("1. Iniciar sesión")
        print("2. Registrarse como ciudadano")
        if not hay_usuarios():
            print("3. Crear administrador inicial (primer uso)")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_login()
        elif opcion == "2":
            registro_ciudadano()
        elif opcion == "3" and not hay_usuarios():
            crear_administrador_inicial()
        elif opcion == "0":
            print("Programa finalizado. Los datos quedan guardados en la carpeta data.")
            return
        else:
            print("Opción incorrecta. Intente nuevamente.")


def iniciar_sistema():
    """Carga los expedientes guardados y abre el menú principal."""
    total = cargar_expedientes()
    print(f"Sistema iniciado. Expedientes cargados: {total}")
    menu_principal()


if __name__ == "__main__":
    try:
        iniciar_sistema()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido. Los datos guardados no se pierden.")

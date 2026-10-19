# ============================================================
# Módulo: mesa_partes/mesa_partes.py
# Responsable: Integrante 2
# Función: menú de Mesa de Partes. main.py solo llama a menu_mesa_partes(sesion).
# ============================================================

from data.tramites import CANALES
from mesa_partes.documentos import anular_documento, consultar_documento, derivar_documento
from mesa_partes.recepcion_fisica import registrar_documento_fisico
from mesa_partes.recepcion_virtual import registrar_documento_virtual
from servicios.entradas import leer_opcion, leer_texto
from servicios.notificaciones import listar_todas
from servicios.reportes import menu_reporte


def seleccionar_canal():
    """Pregunta por qué canal llegó el documento. Devuelve 'FISICO', 'VIRTUAL' o None."""
    opciones = {"1": "MESA DE PARTES EXTERNA - FÍSICO",
                "2": "MESA DE PARTES VIRTUAL - CASILLA ELECTRÓNICA"}
    clave = leer_opcion("CANAL DE RECEPCIÓN", opciones)
    return CANALES[clave] if clave else None


def registrar_documento_canal(sesion):
    """Según el canal elegido, llama a la recepción física o virtual."""
    canal = seleccionar_canal()
    if canal == "FISICO":
        return registrar_documento_fisico(sesion)
    if canal == "VIRTUAL":
        return registrar_documento_virtual(sesion)
    return None


def _anular(sesion):
    codigo = leer_texto("Código de expediente")
    exp = consultar_documento(codigo)
    if exp is None:
        return
    if leer_opcion("¿Desea ANULAR el documento?", {"1": "Sí", "2": "No"}, cancelar=False) == "2":
        return
    motivo = leer_texto("Ingrese motivo de anulación")
    exp, error = anular_documento(codigo, motivo, sesion["usuario"])
    if error:
        print(f"[ERROR] {error}")
    else:
        print(f"\n[OK] DOCUMENTO ANULADO | {exp['codigo']} | Motivo: {exp['motivo_anulacion']}")
        print("  ✓ Se registró la anulación en el historial (el expediente NO se elimina).")


def _derivar(sesion):
    codigo = leer_texto("Código de expediente")
    exp, error = derivar_documento(codigo, sesion["usuario"])
    if error:
        print(f"[ERROR] {error}")
    else:
        print(f"[OK] Expediente {exp['codigo']} derivado a {exp['area']}. Estado: {exp['estado']}")


def _notificaciones():
    lista = listar_todas()
    if not lista:
        print("No hay notificaciones en el sistema.")
    for n in lista:
        estado = "LEÍDA" if n["leida"] else "NUEVA"
        print(f"[{estado}] {n['fecha']} | {n['tipo']} | {n['codigo_expediente']} "
              f"(persona {n['id_persona']})\n   {n['mensaje']}")


def menu_mesa_partes(sesion):
    """Punto de entrada del rol MESA_PARTES."""
    while True:
        print(f"\n{'=' * 40}\nMESA DE PARTES  -  Usuario: {sesion['usuario']}\n{'=' * 40}")
        print("1. Registrar documento")
        print("2. Consultar documento")
        print("3. Derivar documento")
        print("4. Anular documento")
        print("5. Consultar expedientes (ordenar / buscar)")
        print("6. Notificaciones")
        print("0. Cerrar sesión")
        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            registrar_documento_canal(sesion)
        elif opcion == "2":
            consultar_documento(leer_texto("Código de expediente"))
        elif opcion == "3":
            _derivar(sesion)
        elif opcion == "4":
            _anular(sesion)
        elif opcion == "5":
            menu_reporte()
        elif opcion == "6":
            _notificaciones()
        elif opcion == "0":
            print("Saliendo de Mesa de Partes...")
            return
        else:
            print("[ERROR] Opción no válida.")

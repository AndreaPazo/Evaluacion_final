# ============================================================
# Módulo: funcionario/funcionario.py
# Responsable: Integrante 3
# Función: menú del funcionario. Ve la bandeja de SU área, abre expedientes,
#          los acepta, deriva, observa, atiende y archiva.
# ============================================================

from data.areas import AREAS, listar_areas
from data.expedientes import buscar_expediente, listar_expedientes
from funcionario.procesamiento import (aceptar, derivar, registrar_observacion,
                                       registrar_subsanacion, atender, finalizar_expediente)
from servicios.entradas import leer_entero, leer_texto
from servicios.historial import ver_historial


def ver_bandeja(area):
    """Muestra los expedientes pendientes del área.
    No muestra RECIBIDO (Mesa de Partes aún no los deriva), ARCHIVADO ni ANULADO."""
    print("\n========== BANDEJA DE EXPEDIENTES ==========")
    encontrados = 0
    for exp in listar_expedientes():
        if exp["area"] == area and exp["estado"] not in ("RECIBIDO", "ARCHIVADO", "ANULADO"):
            print(f"{exp['codigo']} | {exp['tramite']:<32} | {exp['estado']}")
            encontrados += 1
    if encontrados == 0:
        print("No hay expedientes pendientes en esta área.")


def ver_expediente(codigo):
    """Muestra el detalle y el historial. Devuelve el expediente o None."""
    exp = buscar_expediente(codigo)
    if exp is None:
        print("Expediente no encontrado.")
        return None
    print("\n========== DETALLE DEL EXPEDIENTE ==========")
    print("Código       :", exp["codigo"])
    print("Solicitante  :", exp["administrado"])
    print("Trámite      :", exp["tramite"], "-", exp["subtipo"] or "N/A")
    print("Asunto       :", exp["asunto"])
    print("Área         :", exp["area"])
    print("Estado       :", exp["estado"])
    print("Canal        :", exp["canal"])
    print("Observación  :", exp.get("observacion", "Ninguna"))
    ver_historial(exp)
    return exp


def _pedir_area_destino():
    """Muestra las áreas y devuelve la elegida, o None."""
    listar_areas()
    opcion = leer_entero("Seleccione el área de destino")
    if opcion is None or opcion < 1 or opcion > len(AREAS):
        print("Área no válida.")
        return None
    return AREAS[opcion - 1]


def _ejecutar(opcion, exp, sesion):
    """Aplica la operación elegida y muestra el resultado."""
    usuario = sesion["usuario"]
    if opcion == "3":
        ok, msg = aceptar(exp, usuario)
    elif opcion == "4":
        destino = _pedir_area_destino()
        if destino is None:
            return
        ok, msg = derivar(exp, destino, usuario)
    elif opcion == "5":
        ok, msg = registrar_observacion(exp, leer_texto("Motivo de la observación"), usuario)
    elif opcion == "6":
        ok, msg = registrar_subsanacion(exp, leer_texto("Detalle de la subsanación recibida"), usuario)
    elif opcion == "7":
        ok, msg = atender(exp, leer_texto("Respuesta o resultado de la atención"), usuario)
    else:
        ok, msg = finalizar_expediente(exp, usuario)
    print(("[OK] " if ok else "[ERROR] ") + msg)


def menu_funcionario(sesion):
    """Punto de entrada del rol FUNCIONARIO."""
    area = sesion.get("area")
    if not area:
        print("El usuario no tiene un área asignada. Pida al administrador que se la asigne.")
        return
    while True:
        print("\n" + "=" * 40)
        print(f" MÓDULO DE FUNCIONARIO - {sesion['nombre_completo']}")
        print(f" Área: {area}")
        print("=" * 40)
        print("1. Ver bandeja")
        print("2. Abrir expediente")
        print("3. Aceptar expediente (pasa a EN_PROCESO)")
        print("4. Derivar expediente")
        print("5. Observar expediente")
        print("6. Registrar subsanación recibida")
        print("7. Atender expediente")
        print("8. Archivar expediente")
        print("0. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ver_bandeja(area)
        elif opcion == "2":
            ver_expediente(leer_texto("Código del expediente"))
        elif opcion in ("3", "4", "5", "6", "7", "8"):
            exp = buscar_expediente(leer_texto("Código del expediente"))
            if exp is None:
                print("Expediente no encontrado.")
            elif exp["area"] != area:
                print("Este expediente no pertenece a tu área.")
            else:
                _ejecutar(opcion, exp, sesion)
        elif opcion == "0":
            print("Saliendo del módulo de funcionario.")
            return
        else:
            print("Opción no válida.")

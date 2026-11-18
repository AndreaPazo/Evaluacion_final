# ============================================================
#  casilla.py


#Importa las funciones necesarias para manejar la casilla electrónica de un ciudadano.(MODULO)
from data.personas import buscar_persona, codigo_casilla 
from servicios.entradas import leer_entero
from servicios.notificaciones import (listar_notificaciones, marcar_leida,
                                      contar_no_leidas, enviar_notificacion)


#Funcion que crea una casilla para un ciudadano dado su id_persona. 
def crear_casilla(id_persona):
    """Devuelve los datos de la casilla de la persona, o None si no existe."""
    persona = buscar_persona(id_persona)
    if persona is None:
        return None
    return {
        "codigo": codigo_casilla(id_persona),
        "id_persona": id_persona,
        "titular": persona["nombres"] + " " + persona["apellidos"],
    }

#funcion que busca la casilla de un ciudadano dado su id_persona.
def buscar_casilla(id_persona):
    """Igual que crear_casilla: cada persona tiene una sola casilla."""
    return crear_casilla(id_persona)

#funcion que muestra el encabezado de la casilla con las notificaciones nuevas de un 
# ciudadano dado su id_persona.
def ver_casilla(id_persona):
    """Muestra el encabezado de la casilla con las notificaciones nuevas."""
    casilla = crear_casilla(id_persona)
    if casilla is None:
        print("No se encontró la persona asociada a la casilla.")
        return
    print("\n" + "=" * 34)
    print("       CASILLA ELECTRÓNICA")
    print("=" * 34)
    print("Ciudadano:", casilla["titular"])
    print("Casilla  :", casilla["codigo"])
    print("Notificaciones nuevas:", contar_no_leidas(id_persona))

#funcion que recibe un documento y lo deja en la casilla de un ciudadano dado su id_persona.
def recibir_documento(id_persona, mensaje, codigo_expediente=None):
    """Deja un aviso/documento en la casilla."""
    return enviar_notificacion(id_persona, mensaje, codigo_expediente, "DOCUMENTO")



def listar_mensajes(id_persona):
    """Muestra las notificaciones de la casilla. Devuelve la cantidad."""
    mensajes = listar_notificaciones(id_persona)
    if not mensajes:
        print("No tiene mensajes en su casilla.")
    for n in mensajes:
        marca = "✓ LEÍDA" if n["leida"] else "● NUEVA"
        print(f"[{n['id_notificacion']}] {n['fecha']} | {marca} | {n['tipo']}")
        print("    ", n["mensaje"])
    return len(mensajes)


def menu_mensajes(id_persona):
    """Lista las notificaciones y permite marcar una como leída."""
    if listar_mensajes(id_persona) == 0:
        return
    numero = leer_entero("Número de notificación para marcarla como leída (0 para volver)")
    if numero is None or numero == 0:
        return
    if marcar_leida(numero, id_persona):
        print("Notificación marcada como leída.")
    else:
        print("No se encontró esa notificación en su casilla.")

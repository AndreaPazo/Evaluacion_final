# ============================================================
# Módulo: ciudadano/ciudadano.py
# ============================================================

#se importan los modulos necesarios para manejar las funciones del ciudadano, 
# como ver perfil, crear solicitud, consultar expediente, consultar estado, ver constancias y
# el menu principal del ciudadano.
from ciudadano.casilla import ver_casilla, menu_mensajes
from data.expedientes import listar_expedientes_persona, buscar_expediente
from data.personas import buscar_persona, formato_id
from mesa_partes.recepcion_virtual import enviar_solicitud_virtual
from servicios.entradas import leer_texto
from servicios.historial import ver_historial


#define la funcion ver_perfil, tomando como parametro la sesion del ciudadano, 
# y mostrando sus datos personales
def ver_perfil(sesion):
    """Muestra los datos del ciudadano."""
    persona = buscar_persona(sesion["id_persona"])
    if persona is None:
        print("No se encontraron los datos del ciudadano.")
        """ si no se encuentra la persona, se retorna """
        return
    print("\n--- MI PERFIL ---")
    print("ID_PERSONA:", formato_id(persona["id_persona"]))
    print("Documento :", persona["tipo_documento"], persona["numero_documento"])
    print("Nombres   :", persona["nombres"])
    print("Apellidos :", persona["apellidos"])
    print("Correo    :", persona["correo"])
    print("Teléfono  :", persona["telefono"])

#define la funcion crear_solicitud que toma como parametro la sesion del ciudadano, 
# y envia una solicitud virtual generando el expediente, la constancia y la notificacion. 
def crear_solicitud(sesion):
    """Envía una solicitud virtual: se genera el expediente, la constancia y la notificación."""
    persona = buscar_persona(sesion["id_persona"])
    enviar_solicitud_virtual(sesion, persona)

#define la funcion consultar_expediente que toma como parametro la sesion del ciudadano, 
# y lista los expedientes del ciudadano, mostrando un mensaje si no tiene expedientes registrados.
def consultar_expediente(sesion):
    """Lista los expedientes del ciudadano."""
    expedientes = listar_expedientes_persona(sesion["id_persona"])
    if not expedientes:
        print("No tiene expedientes registrados.")
        return
    print("\n--- MIS EXPEDIENTES ---")
    for exp in expedientes:
        print(f"{exp['codigo']} | {exp['tramite']:<32} | {exp['estado']}")

#define la funcion _expediente_propio que toma como parametro la sesion del ciudadano, 
# y pide un codigo de expediente, devolviendo el expediente solo si pertenece al ciudadano.
def _expediente_propio(sesion):
    """Pide un código y devuelve el expediente solo si pertenece al ciudadano."""
    exp = buscar_expediente(leer_texto("Código de expediente"))
    if exp is None or exp["id_persona"] != sesion["id_persona"]:
        print("No se encontró el expediente o no pertenece a su cuenta.")
        return None
    return exp

#definir la funcion consultar_estado que toma como parametro la sesion del ciudadano,
# y muestra el seguimiento del expediente propio, incluyendo codigo, tramite, estado, area, canal
# y observacion, ademas de llamar a la funcion ver_historial para mostrar el historial
def consultar_estado(sesion):
    """Seguimiento de un expediente propio."""
    exp = _expediente_propio(sesion)
    if exp is None:
        return
    print("\n--- SEGUIMIENTO DEL EXPEDIENTE ---")
    print("Código     :", exp["codigo"])
    print("Trámite    :", exp["tramite"])
    print("Estado     :", exp["estado"])
    print("Área       :", exp["area"])
    print("Canal      :", exp["canal"])
    print("Observación:", exp.get("observacion", "Sin observaciones"))
    ver_historial(exp)


# def subsanar(sesion):
#     """El ciudadano responde a una observación: OBSERVADO -> SUBSANADO."""
#     exp = _expediente_propio(sesion)
#     if exp is None:
#         return
#     if exp["estado"] != "OBSERVADO":
#         print("Ese expediente no tiene observaciones pendientes.")
#         return
#     print("Observación del funcionario:", exp.get("observacion"))
#     detalle = leer_texto("Detalle de su subsanación")
#     ok, mensaje = registrar_subsanacion(exp, detalle, sesion["usuario"])
#     print(("[OK] " if ok else "[ERROR] ") + mensaje)

#definir la funcion ver_constancias que toma como parametro la sesion del ciudadano,
# y lista las constancias generadas en los expedientes del ciudadano, mostrando un mensaje si
# no hay constancias disponibles.
def ver_constancias(sesion):
    """Lista las constancias generadas en los expedientes del ciudadano."""
    constancias = [e for e in listar_expedientes_persona(sesion["id_persona"])
                   if e.get("codigo_constancia")]
    if not constancias:
        print("No hay constancias disponibles.")
        return
    print("\n--- CONSTANCIAS ---")
    for exp in constancias:
        print(f"{exp['codigo_constancia']}  (expediente {exp['codigo']}, {exp['fecha_registro']})")

#def menu_mensajes(id_persona):
# Muestra el menú de mensajes para un ciudadano, permitiéndole listar notificaciones,
# marcar notificaciones como leídas y volver al menú principal.
def menu_ciudadano(sesion):
    """Punto de entrada del rol CIUDADANO."""
    while True:
        """Muestra el menú principal del ciudadano y permite acceder a las diferentes opciones."""
        ver_casilla(sesion["id_persona"])
        print("\n1. Ver mi perfil")
        print("2. Nueva solicitud")
        print("3. Mis expedientes")
        print("4. Consultar estado / seguimiento")
        # print("5. Subsanar observación")
        print("6. Notificaciones")
        print("7. Constancias")
        print("0. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            ver_perfil(sesion)
        elif opcion == "2":
            crear_solicitud(sesion)
        elif opcion == "3":
            consultar_expediente(sesion)
        elif opcion == "4":
            consultar_estado(sesion)
        # elif opcion == "5":
        #     subsanar(sesion)
        elif opcion == "6":
            menu_mensajes(sesion["id_persona"])
        elif opcion == "7":
            ver_constancias(sesion)
        elif opcion == "0":
            print("Sesión del ciudadano finalizada.")
            return
        else:
            print("Opción no válida.")

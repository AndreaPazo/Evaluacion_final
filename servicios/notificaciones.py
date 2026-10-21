# ============================================================
# Módulo: servicios/notificaciones.py  (COMPARTIDO)
# Responsable: Integrante 4
# Función: crear y consultar las notificaciones de la casilla electrónica.
# No se envía correo real: la consola simula el envío.
# Datos en data/base_notificaciones.py
# ============================================================


#importa los modulos necesarios para manejar las notificaciones de la casilla electrónica de un ciudadano.
import os
from datetime import datetime

from data.almacen import CARPETA_DATA, cargar_lista, guardar_lista
from data.personas import codigo_casilla

#archivo donde se guardan las notificaciones.
ARCHIVO_NOTIFICACIONES = os.path.join(CARPETA_DATA, "base_notificaciones.py")
VARIABLE = "NOTIFICACIONES"

# Funciones privadas para cargar y guardar la lista de notificaciones
def _cargar():
    return cargar_lista(ARCHIVO_NOTIFICACIONES, VARIABLE)

# Función privada para guardar la lista de notificaciones
def _guardar(datos):
    guardar_lista(ARCHIVO_NOTIFICACIONES, VARIABLE, datos)

# Funciones públicas para manejar las notificaciones
def crear_notificacion(id_persona, mensaje, codigo_expediente=None, tipo="INFORMACION"):
    """Guarda una notificación nueva (sin leer) y la devuelve."""
    datos = _cargar()
    siguiente = max([n["id_notificacion"] for n in datos], default=0) + 1
    notificacion = {
        "id_notificacion": siguiente,
        "id_persona": id_persona,
        "codigo_expediente": codigo_expediente,
        "tipo": tipo,
        "mensaje": mensaje,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "leida": False,
    }
    datos.append(notificacion)
    _guardar(datos)
    return notificacion

# Función pública para enviar una notificación a la casilla de un ciudadano
def enviar_notificacion(id_persona, mensaje, codigo_expediente=None, tipo="INFORMACION"):
    """Crea la notificación y simula el envío por consola."""
    n = crear_notificacion(id_persona, mensaje, codigo_expediente, tipo)
    print(f"  ✓ NOTIFICACIÓN ENVIADA a la casilla {codigo_casilla(id_persona)} "
          f"(N.º {n['id_notificacion']}, {tipo})")
    return n

# Función pública para listar las notificaciones de una persona
def listar_notificaciones(id_persona):
    """Notificaciones de una persona."""
    return [n for n in _cargar() if n["id_persona"] == id_persona]

# Función pública para listar todas las notificaciones del sistema
def listar_todas():
    """Todas las notificaciones del sistema."""
    return _cargar()

# Función pública para contar las notificaciones no leídas de una persona
def contar_no_leidas(id_persona):
    """Cantidad de notificaciones sin leer de una persona."""
    return len([n for n in listar_notificaciones(id_persona) if not n["leida"]])

# Función pública para marcar una notificación como leída
def marcar_leida(id_notificacion, id_persona):
    """Marca como leída una notificación de esa persona. True si la encontró."""
    datos = _cargar()
    for n in datos:
        if n["id_notificacion"] == id_notificacion and n["id_persona"] == id_persona:
            n["leida"] = True
            _guardar(datos)
            return True
    return False


# --- Una función por cada hito del trámite ---
def _notificar(exp, mensaje, tipo):
    return enviar_notificacion(exp["id_persona"], mensaje, exp["codigo"], tipo)

#define la funcion notificar_registro, 
# que recibe un expediente y envia una notificacion de registro al ciudadano.
def notificar_registro(exp):
    return _notificar(exp, f"Su solicitud de {exp['tramite']} fue recibida. "
                           f"Se generó el expediente {exp['codigo']}.", "REGISTRO")

#define la funcion notificar_derivacion,que recibe un expediente y envia una 
# notificacion de derivacion al ciudadano.
def notificar_derivacion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue derivado a {exp['area']}.", "DERIVACION")

#define la funcion notificar_atencion, que recibe un expediente y envia una
#  notificacion de atencion al ciudadano.
def notificar_observacion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue OBSERVADO: {exp.get('observacion', '')}. "
                           "Ingrese a su casilla para subsanar.", "OBSERVACION")

#define la funcion notificar_subsanacion, que recibe un expediente y envia una
# notificacion de subsanacion al ciudadano.
def notificar_subsanacion(exp):
    return _notificar(exp, f"Se registró la subsanación del expediente {exp['codigo']}.", "SUBSANACION")

#define la funcion notificar_atencion, que recibe un expediente y envia una
# notificacion de atencion al ciudadano.
def notificar_atencion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue ATENDIDO.", "ATENCION")

#define la funcion notificar_archivo, que recibe un expediente y envia una
# notificacion de archivo al ciudadano.
def notificar_archivo(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue ARCHIVADO.", "ARCHIVO")

#define la funcion notificar_anulacion, que recibe un expediente y envia una
# notificacion de anulacion al ciudadano.
def notificar_anulacion(exp):
    return _notificar(exp, f"Su expediente {exp['codigo']} fue ANULADO. "
                           f"Motivo: {exp['motivo_anulacion']}.", "ANULACION")

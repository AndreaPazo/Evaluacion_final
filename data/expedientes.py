# Función: ÚNICA lista de expedientes. Vive en memoria mientras corre el
#          programa y se guarda en data/base_expedientes.py (datos en duro).

import os
from datetime import datetime
from data.almacen import CARPETA_DATA, cargar_lista, guardar_lista
from servicios.busqueda import buscar_lineal

ARCHIVO_EXPEDIENTES = os.path.join(CARPETA_DATA, "base_expedientes.py")
VARIABLE = "EXPEDIENTES"

ESTADOS = ["RECIBIDO", "DERIVADO", "EN_PROCESO", "OBSERVADO",
           "SUBSANADO", "ATENDIDO", "ARCHIVADO", "ANULADO"]

expedientes = []   # <- lista de expedientes viva en memoria

def ahora():
    """Fecha y hora actual como texto: 'dd/mm/aaaa hh:mm'."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def cargar_expedientes():
    """Lee el archivo y llena la lista en memoria (sin cambiar el objeto lista)."""
    expedientes[:] = cargar_lista(ARCHIVO_EXPEDIENTES, VARIABLE)
    return len(expedientes)

def guardar_expedientes():
    """Escribe la lista completa en el archivo de datos."""
    guardar_lista(ARCHIVO_EXPEDIENTES, VARIABLE, expedientes)

def crear_expediente(datos):
    """Asigna código EXP-AAAA-NNNNNN, completa los campos base y lo guarda."""
    anio = datetime.now().year
    correlativo = len(expedientes) + 1      # nunca se borran expedientes, así no se repite
    datos["codigo"] = "EXP-%d-%06d" % (anio, correlativo)
    datos.setdefault("estado", "RECIBIDO")
    datos.setdefault("fecha_registro", ahora())
    datos.setdefault("motivo_anulacion", None)
    datos.setdefault("historial", [])
    datos.setdefault("anulado", False)
    expedientes.append(datos)
    guardar_expedientes()
    return datos

def buscar_expediente(codigo):
    """Búsqueda LINEAL por código. Devuelve el expediente o None."""
    posicion = buscar_lineal(expedientes, "codigo", codigo.strip().upper())
    return expedientes[posicion] if posicion != -1 else None

def listar_expedientes():
    """Devuelve todos los expedientes (en el orden en que se registraron)."""
    return expedientes

def listar_expedientes_persona(id_persona):
    """Expedientes que pertenecen a una persona."""
    return [e for e in expedientes if e["id_persona"] == id_persona]

def actualizar_expediente(codigo, **cambios):
    """Cambia campos de un expediente y guarda. Devuelve el expediente o None."""
    exp = buscar_expediente(codigo)
    if exp is None:
        return None
    exp.update(cambios)
    guardar_expedientes()
    return exp

# Función: listar expedientes ordenados, buscar por código (binaria) y contar
#          por estado. Usa ARREGLOS PARALELOS, una matriz y los algoritmos
#          de servicios/ordenamiento.py y servicios/busqueda.py.

from data.expedientes import ESTADOS, listar_expedientes
from servicios.busqueda import buscar_binaria
from servicios.ordenamiento import (fecha_a_clave, ordenar_burbuja_matriz,ordenar_insercion_paralelos)

def construir_arreglos_paralelos():
    """Separa los expedientes en arreglos paralelos (misma posición = mismo expediente)."""
    codigos, estados, areas, fechas, tramites = [], [], [], [], []
    for exp in listar_expedientes():
        codigos.append(exp["codigo"])
        estados.append(exp["estado"])
        areas.append(exp["area"])
        fechas.append(exp["fecha_registro"])
        tramites.append(exp["tramite"])
    return codigos, estados, areas, fechas, tramites

def construir_matriz():
    """Matriz: cada fila es [codigo, estado, area, fecha, tramite]."""
    matriz = []
    codigos, estados, areas, fechas, tramites = construir_arreglos_paralelos()
    for i in range(len(codigos)):
        matriz.append([codigos[i], estados[i], areas[i], fechas[i], tramites[i]])
    return matriz

def listar_ordenado(criterio="CODIGO"):
    """Devuelve la matriz ordenada. criterio: CODIGO, FECHA, ESTADO o AREA."""
    matriz = construir_matriz()
    columnas = {"CODIGO": 0, "ESTADO": 1, "AREA": 2}
    if criterio == "FECHA":
        # Se agrega al final una clave de fecha ordenable y se ordena por ella.
        for fila in matriz:
            fila.append(fecha_a_clave(fila[3]))
        ordenar_burbuja_matriz(matriz, 5)
        for fila in matriz:
            fila.pop()
    else:
        ordenar_burbuja_matriz(matriz, columnas.get(criterio, 0))
    return matriz

def mostrar_tabla(matriz):
    """Imprime la matriz como tabla."""
    if not matriz:
        print("No hay expedientes registrados.")
        return
    print(f"{'CÓDIGO':<17}{'ESTADO':<12}{'ÁREA':<22}{'FECHA':<18}TRÁMITE")
    print("-" * 95)
    for f in matriz:
        print(f"{f[0]:<17}{f[1]:<12}{f[2]:<22}{f[3]:<18}{f[4]}")

def buscar_por_codigo_binaria(codigo):
    """Ordena los códigos (inserción) y los busca con búsqueda binaria.

    Devuelve la fila [codigo, estado, area, fecha, tramite] o None.
    """
    codigos, estados, areas, fechas, tramites = construir_arreglos_paralelos()
    ordenar_insercion_paralelos(codigos, estados, areas, fechas, tramites)
    pos = buscar_binaria(codigos, codigo.strip().upper())
    if pos == -1:
        return None
    return [codigos[pos], estados[pos], areas[pos], fechas[pos], tramites[pos]]

def contar_por_estado():
    """Cuenta expedientes por estado con dos arreglos paralelos: ESTADOS y conteos."""
    conteos = [0] * len(ESTADOS)
    for exp in listar_expedientes():
        posicion = ESTADOS.index(exp["estado"])
        conteos[posicion] += 1
    return ESTADOS, conteos

def menu_reporte():
    """Menú de consulta: ordenar, buscar por código y estadísticas (lo usan Mesa de Partes y el administrador)."""
    from servicios.entradas import leer_opcion, leer_texto
    while True:
        clave = leer_opcion("CONSULTA DE EXPEDIENTES", {
            "1": "Listar ordenado por CÓDIGO",
            "2": "Listar ordenado por FECHA",
            "3": "Listar ordenado por ESTADO",
            "4": "Listar ordenado por ÁREA",
            "5": "Buscar por código (búsqueda binaria)",
            "6": "Cantidad de expedientes por estado",
        })
        if clave is None:
            return
        if clave in ("1", "2", "3", "4"):
            criterio = {"1": "CODIGO", "2": "FECHA", "3": "ESTADO", "4": "AREA"}[clave]
            mostrar_tabla(listar_ordenado(criterio))
        elif clave == "5":
            fila = buscar_por_codigo_binaria(leer_texto("Código de expediente"))
            if fila is None:
                print("Expediente no encontrado.")
            else:
                mostrar_tabla([fila])
        else:
            estados, conteos = contar_por_estado()
            for i in range(len(estados)):
                print(f"{estados[i]:<12}: {conteos[i]}")

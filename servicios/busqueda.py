def buscar_lineal(lista, campo, valor):
    """Recorre la lista de diccionarios uno por uno.

    Devuelve la posición (índice) donde `lista[i][campo] == valor`, o -1.
    """
    for i in range(len(lista)):
        if lista[i][campo] == valor:
            return i
    return -1


def buscar_binaria(arreglo_ordenado, objetivo):
    """Búsqueda binaria sobre un arreglo de textos YA ORDENADO de menor a mayor.

    Cada vuelta descarta la mitad del arreglo. Devuelve el índice o -1.
    """
    inicio = 0
    fin = len(arreglo_ordenado) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if arreglo_ordenado[medio] == objetivo:
            return medio
        if arreglo_ordenado[medio] < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1

# Se grego
def buscar_expediente(expedientes: list, criterio: str) -> list:
    """
    Búsqueda avanzada de expedientes por código, DNI o nombre del ciudadano con orden lógico visible.
    """
    if not criterio:
        return expedientes
    
    criterio = criterio.lower()
    resultados = []
    for exp in expedientes:
        if (criterio in str(exp.get("codigo", "")).lower() or
            criterio in str(exp.get("dni", "")).lower() or
            criterio in str(exp.get("nombre", "")).lower()):
            resultados.append(exp)
            
    return resultados


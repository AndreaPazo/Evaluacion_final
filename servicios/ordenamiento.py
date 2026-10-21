# Función: algoritmos de ordenamiento escritos paso a paso.

def ordenar_burbuja_matriz(matriz, columna, descendente=False):
    """Ordena una matriz (lista de filas) por la `columna` indicada.
    Burbuja: compara filas vecinas y las intercambia si están desordenadas.
    """
    n = len(matriz)
    for pasada in range(n - 1):
        for i in range(n - 1 - pasada):
            a = matriz[i][columna]
            b = matriz[i + 1][columna]
            fuera_de_orden = a < b if descendente else a > b
            if fuera_de_orden:
                matriz[i], matriz[i + 1] = matriz[i + 1], matriz[i]
    return matriz

def ordenar_insercion_paralelos(claves, *paralelos, descendente=False):
    # Ordena `claves` por inserción y mueve igual los arreglos paralelos.
    # Arreglos paralelos: la posición i de cada arreglo describe el MISMO expediente,
    # por eso cuando se mueve una clave también se mueve su dato en los demás.
    
    for i in range(1, len(claves)):
        clave = claves[i]
        extras = [p[i] for p in paralelos]
        j = i - 1
        while j >= 0 and ((claves[j] < clave) if descendente else (claves[j] > clave)):
            claves[j + 1] = claves[j]
            for p in paralelos:
                p[j + 1] = p[j]
            j -= 1
        claves[j + 1] = clave
        for k in range(len(paralelos)):
            paralelos[k][j + 1] = extras[k]

def fecha_a_clave(fecha):
    # Convierte 'dd/mm/aaaa hh:mm' en 'aaaammddhhmm' para poder ordenar fechas como texto
    dia, mes, resto = fecha[0:2], fecha[3:5], fecha[6:]
    anio, hora = resto[0:4], resto[5:].replace(":", "")
    return anio + mes + dia + hora

def ordenar_expedientes(expedientes: list, criterio_orden: str = "fecha_reciente") -> list:
    # Ordenamiento lógico visible de expedientes:
    # - 'fecha_reciente': Orden descendente por fecha (más reciente primero).
    # - 'fecha_antigua': Orden ascendente por fecha.
    # - 'codigo': Orden alfabético por código de expediente.
    
    if criterio_orden == "fecha_reciente":
        return sorted(expedientes, key=lambda x: fecha_a_clave(x.get("fecha_registro", "")), reverse=True)
    elif criterio_orden == "fecha_antigua":
        return sorted(expedientes, key=lambda x: fecha_a_clave(x.get("fecha_registro", "")), reverse=False)
    elif criterio_orden == "codigo":
        return sorted(expedientes, key=lambda x: x.get("codigo", ""))
    return expedientes
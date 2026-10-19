import ast
import os
import pprint
import shutil

# Carpeta donde estan todos los archivos de datos (base_*.py).
CARPETA_DATA = os.path.dirname(os.path.abspath(__file__))

ENCABEZADO = (
    "# ARCHIVO DE DATOS GENERADO AUTOMÁTICAMENTE POR EL SISTEMA.\n"
    "# Puede leerlo, pero no lo edite a mano mientras el programa está en uso.\n\n"
)

class ArchivoDanado(Exception):
    """Se lanza cuando un archivo de datos existe pero no se puede leer."""

def cargar_lista(ruta, nombre_variable):
    """
    - Si el archivo NO existe, devuelve una lista vacía (primer uso).
    - Si el archivo existe pero está DAÑADO, lanza ArchivoDanado.
      Así el programa se detiene y NO sobrescribe los datos con una lista vacía.
    ast.literal_eval, solo acepta datos simples (listas, diccionarios, textos, 
    números) y nunca ejecuta código."""

    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            texto = archivo.read()
        marca = nombre_variable + " ="
        inicio = texto.index(marca) + len(marca)
        datos = ast.literal_eval(texto[inicio:].strip())
    except (ValueError, SyntaxError, OSError) as error:
        raise ArchivoDanado(
            f"El archivo {os.path.basename(ruta)} está dañado y no se puede leer ({error}).\n"
            f"Revíselo o restaure la copia {os.path.basename(ruta)}.bak"
        )
    if not isinstance(datos, list):
        raise ArchivoDanado(f"El archivo {os.path.basename(ruta)} no contiene una lista válida.")
    return datos

def guardar_lista(ruta, nombre_variable, lista):
    """Primero escribe en un archivo temporal y luego lo reemplaza, para no
    dejar el archivo a medias si ocurre un error mientras se guarda"""

    contenido = ENCABEZADO + nombre_variable + " = " + pprint.pformat(lista, width=100, sort_dicts=False) + "\n"
    ruta_temporal = ruta + ".tmp"
    with open(ruta_temporal, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    if os.path.exists(ruta):
        shutil.copy2(ruta, ruta + ".bak")   # copia de la versión anterior
    os.replace(ruta_temporal, ruta)

# Función: pedir datos por consola de forma segura (menús, textos, números).

import os
import sys
import re #Importación para las expresiones regulares
# Inserta de forma dinámica la ruta de la carpeta raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import msvcrt  # Importación de librería nativa para leer las teclas que se presiona (Windows)
import sys     # Importación de librería nativa para controlar la salida directa en la consola

from data.personas import validar_documento  # Importación de función modular de otro archivo

# Definición de una Tupla (Estructura de datos constante e inmutable del curso)
TIPOS_DOCUMENTO = ("DNI", "CE", "RUC")

def leer_opcion(titulo, opciones, cancelar=True):
    # Muestra un menú {clave: texto} y repite hasta elegir una clave válida.
    while True:  # Estructura de control: Bucle iterativo infinito para validación
        print(f"\n{titulo}")  # Función nativa print con formateo de cadena
        
        # Bucle FOR para recorrer los elementos del Diccionario (clave-valor)
        for clave, texto in opciones.items():  # Método .items() propio de los diccionarios
            print(f"  {clave}. {texto}")
            
        if cancelar:  # Estructura condicional simple (Booleano)
            print("  0. Cancelar")
            
        # Captura de datos por consola eliminando espacios en blanco extras con el método .strip()
        eleccion = input("Seleccione: ").strip()  
        
        if cancelar and eleccion == "0":  # Operador lógico 'and' para doble condición
            return None  # Retorno de valor nulo controlado
            
        if eleccion in opciones:  # Operador de pertenencia 'in' para buscar la clave en el diccionario
            return eleccion  # Retorna la opción válida elegida
            
        print("[ERROR] Opción no válida. Intente de nuevo.")

def pedir_opcion(mensaje, opciones_validas, cancelar=False):
    # Alias compatible con algunas versiones del módulo de registro
    return leer_opcion(mensaje, opciones_validas, cancelar)


def leer_texto(etiqueta, obligatorio=True):
    # Lee un texto y lo repite hasta que no esté vacío (si es obligatorio)
    while True: 
        valor = input(f"{etiqueta}: ").strip()  # Método de cadena .strip()
        
        # Operador lógico 'not' para evaluar la obligatoriedad del campo
        if valor or not obligatorio:  
            return valor
        print("[ERROR] Este campo es obligatorio.")

def leer_entero(etiqueta):
    # Pide un número entero y repite hasta que el usuario ingrese un valor válido
    while True:
        try:  # Bloque de control de excepciones (Manejo de errores visto en el curso)
            return int(input(f"{etiqueta}: ").strip())  # Función int() para conversión de tipos
        except ValueError:  # Captura el error específico si el usuario digita letras
            print("[ERROR] Debe ingresar un número entero.")

def pedir_contrasena(etiqueta="Contraseña"):
    # Pide una contraseña carácter por carácter mostrando asteriscos (*) en Windows.
    # Logica pura de cadenas y control de salida de flujos en consola.
    
    print(f"{etiqueta}: ", end="", flush=True)  # Parámetro end="" para evitar salto de línea automático
    contrasena = ""  # Inicialización de una variable de tipo Cadena (String vacía)
    
    while True:
        # Uso de la función nativa msvcrt.getch() para leer un carácter como tipo Byte
        caracter = msvcrt.getch()
        
        # Estructura condicional anidada para evaluar el comportamiento del teclado
        if caracter == b'\r':  # Evaluación del Byte correspondiente a la tecla ENTER
            print()  # Función print vacía para insertar un salto de línea estético
            break  # Sentencia de control de bucles: Rompe el ciclo While
            
        elif caracter == b'\x08':  # Evaluación del Byte correspondiente a la tecla RETROCESO (Borrar)
            if len(contrasena) > 0:  # Función nativa len() para counting de longitud de cadena
                # Aplicación de Slicing (Rebanado de cadenas): remueve el último carácter
                contrasena = contrasena[:-1]  
                
                # Método de escritura sys.stdout.write para mandar comandos ASCII directos a la consola
                sys.stdout.write('\b \b')  # Borra visualmente el último asterisco en pantalla
                sys.stdout.flush()  # Método para limpiar y refrescar el buffer de la terminal
                
        elif caracter == b'\t':  # Condicional para ignorar la tecla TABULACIÓN
            continue  # Sentencia de control: salta a la siguiente iteración del bucle
            
        else:
            try:
                # Método .decode() para convertir la lectura binaria (Byte) a texto regular (String UTF-8)
                letra = caracter.decode('utf-8')
                
                if len(contrasena) < 30:  # Condicional para limitar la longitud máxima de seguridad
                    contrasena += letra  # Operador de asignación compuesta para concatenar cadenas
                    sys.stdout.write('*')  # Imprime un único asterisco por cada carácter válido
                    sys.stdout.flush()
            except UnicodeDecodeError:  # Manejo de excepción si se presionan flechas o comandos del sistema
                pass  # Sentencia pass: Operación nula para ignorar el evento de error de forma segura
                
    return contrasena.strip()  # Retorna la cadena limpia construida paso a paso

def pedir_contrasena_registro(etiqueta="Contraseña (entre 6 y 10 caracteres)"):
    # Pide y valida en bucle que la contraseña de registro tenga entre 6 y 10 caracteres
    while True:
        clave = pedir_contrasena(etiqueta)  # Llamada modular a nuestra propia función de asteriscos
        
        # Estructura condicional con comparadores encadenados (Rango matemático regular)
        if 6 <= len(clave) <= 10:  
            return clave  # Retorna la clave definitiva si cumple la regla de negocio
            
        # Muestra un mensaje descriptivo inyectando la longitud del error detectado
        print(f"[ERROR] La contraseña debe tener entre 6 y 10 caracteres. Ingresó: {len(clave)}.")

def pedir_tipo_documento():
    # Muestra DNI/CE/RUC y devuelve el tipo elegido
    clave = leer_opcion(
        "Tipo de documento de identidad:",
        {"1": "DNI", "2": "CE", "3": "RUC"},
        cancelar=False,
    )
    # Uso de expresiones matemáticas aritméticas elementales para acceder a los índices de la Tupla
    return TIPOS_DOCUMENTO[int(clave) - 1]

def pedir_numero_documento(tipo, etiqueta="Número de documento"):
    # Repite hasta que el número cumpla el formato del tipo (DNI/CE/RUC)
    while True:
        numero = input(f"{etiqueta}: ").strip()
        if validar_documento(tipo, numero):  # Evaluación del valor de retorno booleano (True/False)
            return numero
        print(
            "[ERROR] Formato inválido. DNI: 8 dígitos | RUC: 11 dígitos | CE: 1 letra y 7 dígitos."
        )

def pedir_solo_letras(etiqueta):
    # Para nombres y apellidos: solo letras, espacios, guiones y apóstrofes
    while True:
        texto = input(f"{etiqueta}: ").strip()
        
        # Uso de la función nativa all() junto con el método de cadena .isalpha()
        # Verifica carácter por carácter mediante lógica booleana del curso
        if texto and all(c.isalpha() or c in (" ", "-", "'") for c in texto):
            return texto
        print("[ERROR] Ingrese un texto válido (solo letras y espacios).")

def pedir_folios(etiqueta="Cantidad de folios"):
    # Repite hasta que sea un entero mayor a 0 y lo devuelve como entero
    while True:
        valor = input(f"{etiqueta}: ").strip()
        
        # Método .isdigit() para validar que el texto contenga únicamente caracteres numéricos
        if valor.isdigit() and int(valor) >= 1:
            return int(valor)
        print("[ERROR] Ingrese un número entero mayor a 0.")

def pedir_nombre_usuario(etiqueta="Nombre de usuario"):
    # Pide un nombre de usuario básico asegurando que no contenga espacios
    while True:
        usuario = input(f"{etiqueta}: ").strip()
        if usuario != "" and " " not in usuario:
            return usuario
        print("[ERROR] El usuario no puede estar vacío ni contener espacios.")

def pedir_telefono(etiqueta="Teléfono"):
    # Pide un número telefónico celular válido (9 dígitos en Perú)
    while True:
        telefono = input(f"{etiqueta}: ").strip()
        if telefono.isdigit() and len(telefono) == 9 and telefono.startswith("9"):
            return telefono
        print("[ERROR] Teléfono inválido. Debe tener 9 dígitos y empezar con 9.")

def pedir_correo(etiqueta="Correo electrónico"):
    # Pide un correo electrónico validando que contenga al menos un caracter '@' y un '.'
    while True:
        correo = input(f"{etiqueta}: ").strip()
        if "@" in correo and "." in correo:
            return correo
        print("[ERROR] Formato de correo inválido. Debe incluir '@' y un dominio válido (ej. .com).")

def pedir_adjunto_pdf():
    # Pide el nombre de un archivo adjunto asegurando que termine en .pdf de manera correcta
    while True:
        archivo = input("Nombre del archivo adjunto (ejemplo.pdf): ").strip()
        # Validación de consistencia: No puede estar vacío y debe terminar en .pdf
        if archivo != "" and archivo.lower().endswith(".pdf"):
            return archivo
        print("[ERROR] Formato inválido. El archivo debe terminar obligatoria y únicamente en '.pdf'")

def validar_dni(dni: str) -> bool:
    # Valida que el DNI tenga exactamente 8 dígitos numéricos.
    return bool(re.match(r'^\d{8}$', str(dni)))

def validar_ruc(ruc: str) -> bool:
    # Valida que el RUC tenga exactamente 11 dígitos numéricos.
    return bool(re.match(r'^\d{11}$', str(ruc)))

def validar_archivo_pdf(nombre_archivo: str) -> bool:
    # Valida que el archivo adjunto termine estrictamente en .pdf
    if not nombre_archivo:
        return False
    return nombre_archivo.lower().endswith('.pdf')

def validar_entrada_instantanea(datos: dict) -> dict:
    errores = []
    
    dni = datos.get("dni", "")
    if dni and not validar_dni(dni):
        errores.append("El DNI debe contener exactamente 8 dígitos numéricos.")
    
    tipo_persona = datos.get("tipo_persona", "natural")
    if tipo_persona == "juridica":
        ruc = datos.get("ruc", "")
        if not validar_ruc(ruc):
            errores.append("El RUC debe contener exactamente 11 dígitos numéricos.")
            
    folios = datos.get("folios", 0)
    try:
        if int(folios) <= 0:
            errores.append("El número de folios debe ser mayor a 0.")
    except (ValueError, TypeError):
        errores.append("El número de folios debe ser un valor entero válido.")
        
    archivo = datos.get("archivo_pdf", "")
    if not validar_archivo_pdf(archivo):
        errores.append("El documento adjunto debe ser un archivo en formato .pdf válido.")
        
    if errores:
        return {"estado": "rechazado", "errores": errores}
    
    return {"estado": "aprobado", "mensaje": "Validación algorítmica instantánea exitosa."}
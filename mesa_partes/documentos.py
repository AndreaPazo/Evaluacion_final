# ============================================================
# Módulo: mesa_partes/documentos.py
# Responsable: Integrante 2
# Función: validar, registrar, consultar, derivar y anular documentos.
# Es el núcleo de Mesa de Partes: lo usan la recepción física y la virtual.
# ============================================================

from data.areas import determinar_area_por_tramite #from indica que busque en la carpeta data y en un archivo llamada areas.py
#luego usamos el import para pedir que solo se use la funcion llamada determinar_area_por_tramite
from data.expedientes import crear_expediente, buscar_expediente, actualizar_expediente
from data.personas import validar_documento
from data.tramites import CANALES, TRAMITES #lo mismo en el arhcivo tramites.py
#IMPORT CANALES, TRAMITES trae al archivo actual 2 VARIABLES CONSTANTES
from servicios.historial import registrar_historial
from servicios.notificaciones import notificar_registro, notificar_derivacion, notificar_anulacion

#Crea una lista con los nombres de todos los trámites válidos extrayéndolos del diccionario TRAMITES
TRAMITES_VALIDOS = [t["nombre"] for t in TRAMITES.values()]
#Define una tupla fija con los únicos dos tipos de firmas aceptadas en el sistema
FIRMAS_VALIDAS = ("MANUSCRITA", "DIGITAL")


# Define la función que recibe el tipo de documento (DNI, RUC, etc.) y su número
def validar_identificacion(tipo, numero):
    """Devuelve None si el documento es correcto, o el texto del error."""
    
    # Llama a otra función interna; si el documento NO es válido, entra al bloque IF
    if not validar_documento(tipo, numero):
        # Retorna el mensaje de error personalizado inyectando la variable 'tipo' con el f-string
        return f"El número de {tipo} no tiene un formato válido."
        
    # Si el formato fue correcto, la función no entra al IF y retorna None (sin error)
    return None



def validar_n_orden(n_orden):
    """Formato correcto: 0002999-2026- ENTIDAD (7 dígitos - 4 dígitos - siglas en mayúscula)."""
    # MÉTODO .strip(): Elimina espacios en blanco al inicio y al final.
    # MÉTODO .split("-"): Divide la cadena en una lista usando el guion como separador.
    partes = n_orden.strip().split("-")
    
    # FUNCIÓN len(): Cuenta los elementos de la lista. Si no son 3 partes, no es válido.
    if len(partes) != 3:
        return False
        
    # Desempaquetado de variables: Asigna cada elemento de la lista a una variable.
    numero, anio, siglas = partes
    
    # Operadores lógicos (and) y métodos de validación de cadenas:
    # MÉTODO .isdigit(): Retorna True si la cadena contiene solo números.
    # MÉTODO .isalpha(): Retorna True si la cadena contiene solo letras.
    # MÉTODO .isupper(): Retorna True si la cadena está completamente en mayúsculas.
    return (numero.isdigit() and len(numero) == 7 and anio.isdigit()
            and len(anio) == 4 and siglas.isalpha() and siglas.isupper())


def validar_documento_tramite(persona, canal, tramite, subtipo, asunto, folios, datos, adjunto):
    """Revisa todos los datos del trámite. Devuelve la lista de errores (vacía si está bien)."""
    # Inicializa una lista vacía para ir acumulando los mensajes de error encontrados.
    errores = []
    
    # Validación de existencia: Verifica si el objeto persona es nulo (no existe).
    if persona is None:
        return ["La persona no está registrada en la data maestra."]
        
    # Validación de diccionario: Accede a la clave "estado" para verificar que esté activo.
    if persona["estado"] != "ACTIVO":
        # MÉTODO .append(): Agrega un nuevo elemento al final de la lista de errores.
        errores.append("La persona se encuentra INACTIVA.")
        
    # Operador de pertenencia (not in): Verifica si el canal enviado no existe en los valores permitidos.
    if canal not in CANALES.values():
        errores.append("Canal de recepción no válido.")
        
    # Operador de pertenencia (not in): Comprueba si el trámite figura en la lista de trámites válidos.
    if tramite not in TRAMITES_VALIDOS:
        errores.append("Trámite no válido.")
        
    # Validación condicional compuesta: Si el trámite es de tipo "LICENCIA", evalúa su subtipo.
    if tramite == "LICENCIA" and subtipo not in ("CON GOCE", "SIN GOCE"):
        errores.append("La licencia requiere subtipo CON GOCE o SIN GOCE.")
        
    # MÉTODO .strip() aplicado a un string: Si la cadena queda vacía, significa que solo tenía espacios.
    if not asunto.strip():
        errores.append("El asunto es obligatorio.")
        
    # FUNCIÓN str() e int(): Convierte a texto para usar .isdigit() y luego a entero para comparar numéricamente.
    if not str(folios).isdigit() or int(folios) < 1:
        errores.append("El número de folios debe ser un entero mayor a 0.")

    # Bucle anidado: Recorre las configuraciones de trámites para buscar los campos obligatorios.
    for info in TRAMITES.values():
        if info["nombre"] == tramite:
            # Desempaquetado en bucle: Extrae la clave y la etiqueta de cada campo requerido.
            for clave, etiqueta in info["campos"]:
                # MÉTODO .get(): Busca la clave en el diccionario 'datos'. Si no existe, devuelve un texto vacío "".
                if not str(datos.get(clave, "")).strip():
                    # Formateo con F-STRING: Inyecta dinámicamente el nombre de la etiqueta en el mensaje.
                    errores.append(f"Falta el dato: {etiqueta}.")

    # Validación condicional de datos opcionales: Si existe la clave "n_orden", ejecuta la función externa de validación.
    if datos.get("n_orden") and not validar_n_orden(datos["n_orden"]):
        errores.append("El N° de orden/contrato no tiene el formato 0000000-AAAA-SIGLAS.")
        
    if datos.get("firma") and datos["firma"] not in FIRMAS_VALIDAS:
        errores.append("La firma debe ser MANUSCRITA o DIGITAL.")
        
    if canal == "VIRTUAL":
        # MÉTODO .lower(): Convierte a minúsculas.
        # MÉTODO .endswith(): Verifica si la extensión final coincide con la cadena especificada.
        if not adjunto or not adjunto.lower().endswith(".pdf"):
            errores.append("El documento adjunto debe ser un archivo .pdf.")
            
    return errores


def registrar_documento(persona, canal, tramite, subtipo, asunto, folios, datos,
                        usuario, casilla=None, adjunto=None):
    """Valida, crea el expediente, anota el historial y notifica.

    Devuelve (expediente, []) si todo sale bien, o (None, lista_de_errores).
    """
    # Invocación de función: Ejecuta la rutina de validación y almacena el resultado en 'errores'.
    errores = validar_documento_tramite(persona, canal, tramite, subtipo, asunto, folios, datos, adjunto)
    
    # Estructura de control: Si la lista de errores contiene elementos (es evaluada como True), detiene el proceso.
    if errores:
        return None, errores

    # Creación de diccionario: Instancia la estructura del expediente concatenando cadenas y llamando funciones externas.
    expediente = crear_expediente({
        "id_persona": persona["id_persona"],
        "tipo_identificacion": persona["tipo_documento"],
        "numero_identificacion": persona["numero_documento"],
        # Concatenación tradicional: Une cadenas usando el operador aritmético "+".
        "administrado": persona["nombres"] + " " + persona["apellidos"],
        "canal": canal,
        "casilla": casilla,
        "tramite": tramite,
        "subtipo": subtipo,
        "area": determinar_area_por_tramite(tramite), # Ejecuta función de asignación de área.
        "asunto": asunto.strip(),
        "folios": int(folios),
        "datos_adicionales": datos,
        "adjunto": adjunto,
        "registrado_por": usuario,
    })
    
    # Secuencia de ejecución: Llama a procedimientos de actualización, auditoría y alertas respectivamente.
    asignar_constancia(expediente)
    registrar_historial(expediente, "REGISTRO", f"Documento registrado. Canal: {canal}.", usuario)
    notificar_registro(expediente)
    
    # Retorno de Tupla: Devuelve una estructura con el expediente creado y una lista vacía de errores.
    return expediente, []


def asignar_constancia(exp):
    """Genera el código de constancia: EXP-2026-000001 -> CONST-2026-000001."""
    # Slicing / Rebanado de cadenas [4:]: Omite los primeros 4 caracteres de la cadena (el texto "EXP-").
    actualizar_expediente(exp["codigo"], codigo_constancia="CONST-" + exp["codigo"][4:])


def obtener_documento(codigo):
    """Devuelve el expediente (sin imprimir nada) o None."""
    # Retorno directo del resultado devuelto por otra función de búsqueda.
    return buscar_expediente(codigo)


def consultar_documento(codigo):
    """Muestra el detalle de un expediente. Devuelve el expediente o None."""
    exp = buscar_expediente(codigo)
    if exp is None:
        # FUNCIÓN print(): Envía un flujo de salida de texto de error hacia la consola del sistema.
        print("[ERROR] Expediente no encontrado.")
        return None
        
    # Multiplicación de caracteres: El operador "*" genera una línea repetida de guiones para diseño visual.
    print(f"\n{'=' * 20} DETALLE DEL EXPEDIENTE {'=' * 20}")
    print(f"Código    : {exp['codigo']} | Canal: {exp['canal']} | Estado: {exp['estado']}")
    print(f"Solicitante: {exp['administrado']} ({exp['tipo_identificacion']} {exp['numero_identificacion']})")
    print(f"Trámite   : {exp['tramite']} ({exp['subtipo'] or 'N/A'})")
    print(f"Área      : {exp['area']}")
    print(f"Asunto    : {exp['asunto']}")
    print(f"Folios    : {exp['folios']} | Adjunto: {exp['adjunto'] or 'NINGUNO'}")
    
    # Bucle diccionario .items(): Itera simultáneamente sobre las llaves y valores del sub-diccionario.
    for clave, valor in exp["datos_adicionales"].items():
        # Formateo de alineación (:<10): Alinea el texto de la clave a la izquierda rellenando 10 espacios vacíos.
        print(f"{clave:<10}: {valor}")
        
    if exp["anulado"]:
        print(f"ANULADO - Motivo: {exp['motivo_anulacion']}")
    print("=" * 64)
    return exp


def derivar_documento(codigo, usuario):
    """Derivación inicial: RECIBIDO -> DERIVADO al área del trámite. Devuelve (exp, error)."""
    exp = buscar_expediente(codigo)
    if exp is None:
        return None, "Expediente no encontrado."
    if exp["estado"] != "RECIBIDO":
        return None, f"Solo se deriva un expediente RECIBIDO (estado actual: {exp['estado']})."
        
    # Mutación de estado mediante función: Actualiza de forma persistente los atributos del registro.
    actualizar_expediente(codigo, estado="DERIVADO")
    registrar_historial(exp, "DERIVACION", f"Derivado al área de {exp['area']}.", usuario)
    notificar_derivacion(exp)
    return exp, None


def anular_documento(codigo, motivo, usuario):
    """Anula (NO elimina) un expediente RECIBIDO. Devuelve (exp, error)."""
    exp = buscar_expediente(codigo)
    if exp is None:
        return None, "Expediente no encontrado."
    if exp["anulado"]:
        return None, "El expediente ya se encuentra anulado."
    if exp["estado"] != "RECIBIDO":
        return None, f"Solo se anula un expediente RECIBIDO (estado actual: {exp['estado']})."
    if not motivo.strip():
        return None, "El motivo de anulación es obligatorio."
        
    # Envío de múltiples parámetros nombrados (keyword arguments) para modificar el estado lógico del registro.
    actualizar_expediente(codigo, estado="ANULADO", anulado=True, motivo_anulacion=motivo.strip())
    registrar_historial(exp, "ANULACION", f"Motivo: {motivo.strip()}", usuario)
    notificar_anulacion(exp)
    return exp, None

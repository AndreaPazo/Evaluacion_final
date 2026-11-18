# ============================================================
# Módulo: mesa_partes/documentos.py
# Responsable: Integrante 2
# Función: validar, registrar, consultar, derivar y anular documentos.
# Es el núcleo de Mesa de Partes: lo usan la recepción física y la virtual.
# ============================================================

from data.areas import determinar_area_por_tramite
from data.expedientes import crear_expediente, buscar_expediente, actualizar_expediente
from data.personas import validar_documento
from data.tramites import CANALES, TRAMITES
from servicios.historial import registrar_historial
from servicios.notificaciones import notificar_registro, notificar_derivacion, notificar_anulacion

TRAMITES_VALIDOS = [t["nombre"] for t in TRAMITES.values()]
FIRMAS_VALIDAS = ("MANUSCRITA", "DIGITAL")


def validar_identificacion(tipo, numero):
    """Devuelve None si el documento es correcto, o el texto del error."""
    if not validar_documento(tipo, numero):
        return f"El número de {tipo} no tiene un formato válido."
    return None


def validar_n_orden(n_orden):
    """Formato correcto: 0002999-2026- ENTIDAD (7 dígitos - 4 dígitos - siglas en mayúscula)."""
    partes = n_orden.strip().split("-")
    if len(partes) != 3:
        return False
    numero, anio, siglas = partes
    return (numero.isdigit() and len(numero) == 7 and anio.isdigit()
            and len(anio) == 4 and siglas.isalpha() and siglas.isupper())


def validar_documento_tramite(persona, canal, tramite, subtipo, asunto, folios, datos, adjunto):
    """Revisa todos los datos del trámite. Devuelve la lista de errores (vacía si está bien)."""
    errores = []
    if persona is None:
        return ["La persona no está registrada en la data maestra."]
    if persona["estado"] != "ACTIVO":
        errores.append("La persona se encuentra INACTIVA.")
    if canal not in CANALES.values():
        errores.append("Canal de recepción no válido.")
    if tramite not in TRAMITES_VALIDOS:
        errores.append("Trámite no válido.")
    if tramite == "LICENCIA" and subtipo not in ("CON GOCE", "SIN GOCE"):
        errores.append("La licencia requiere subtipo CON GOCE o SIN GOCE.")
    if not asunto.strip():
        errores.append("El asunto es obligatorio.")
    if not str(folios).isdigit() or int(folios) < 1:
        errores.append("El número de folios debe ser un entero mayor a 0.")

    for info in TRAMITES.values():
        if info["nombre"] == tramite:
            for clave, etiqueta in info["campos"]:
                if not str(datos.get(clave, "")).strip():
                    errores.append(f"Falta el dato: {etiqueta}.")

    if datos.get("n_orden") and not validar_n_orden(datos["n_orden"]):
        errores.append("El N° de orden/contrato no tiene el formato 0000000-AAAA-SIGLAS.")
    if datos.get("firma") and datos["firma"] not in FIRMAS_VALIDAS:
        errores.append("La firma debe ser MANUSCRITA o DIGITAL.")
    if canal == "VIRTUAL":
        if not adjunto or not adjunto.lower().endswith(".pdf"):
            errores.append("El documento adjunto debe ser un archivo .pdf.")
    return errores


def registrar_documento(persona, canal, tramite, subtipo, asunto, folios, datos,
                        usuario, casilla=None, adjunto=None):
    """Valida, crea el expediente, anota el historial y notifica.

    Devuelve (expediente, []) si todo sale bien, o (None, lista_de_errores).
    """
    errores = validar_documento_tramite(persona, canal, tramite, subtipo, asunto, folios, datos, adjunto)
    if errores:
        return None, errores

    expediente = crear_expediente({
        "id_persona": persona["id_persona"],
        "tipo_identificacion": persona["tipo_documento"],
        "numero_identificacion": persona["numero_documento"],
        "administrado": persona["nombres"] + " " + persona["apellidos"],
        "canal": canal,
        "casilla": casilla,
        "tramite": tramite,
        "subtipo": subtipo,
        "area": determinar_area_por_tramite(tramite),
        "asunto": asunto.strip(),
        "folios": int(folios),
        "datos_adicionales": datos,
        "adjunto": adjunto,
        "registrado_por": usuario,
    })
    asignar_constancia(expediente)
    registrar_historial(expediente, "REGISTRO", f"Documento registrado. Canal: {canal}.", usuario)
    notificar_registro(expediente)
    return expediente, []


def asignar_constancia(exp):
    """Genera el código de constancia: EXP-2026-000001 -> CONST-2026-000001."""
    actualizar_expediente(exp["codigo"], codigo_constancia="CONST-" + exp["codigo"][4:])


def obtener_documento(codigo):
    """Devuelve el expediente (sin imprimir nada) o None."""
    return buscar_expediente(codigo)


def consultar_documento(codigo):
    """Muestra el detalle de un expediente. Devuelve el expediente o None."""
    exp = buscar_expediente(codigo)
    if exp is None:
        print("[ERROR] Expediente no encontrado.")
        return None
    print(f"\n{'=' * 20} DETALLE DEL EXPEDIENTE {'=' * 20}")
    print(f"Código    : {exp['codigo']} | Canal: {exp['canal']} | Estado: {exp['estado']}")
    print(f"Solicitante: {exp['administrado']} ({exp['tipo_identificacion']} {exp['numero_identificacion']})")
    print(f"Trámite   : {exp['tramite']} ({exp['subtipo'] or 'N/A'})")
    print(f"Área      : {exp['area']}")
    print(f"Asunto    : {exp['asunto']}")
    print(f"Folios    : {exp['folios']} | Adjunto: {exp['adjunto'] or 'NINGUNO'}")
    for clave, valor in exp["datos_adicionales"].items():
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
    actualizar_expediente(codigo, estado="ANULADO", anulado=True, motivo_anulacion=motivo.strip())
    registrar_historial(exp, "ANULACION", f"Motivo: {motivo.strip()}", usuario)
    notificar_anulacion(exp)
    return exp, None

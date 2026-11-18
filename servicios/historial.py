# ============================================================
# Módulo: servicios/historial.py  (COMPARTIDO por los 4 integrantes)
# Función: registrar y mostrar los movimientos de un expediente.
# Formato de cada movimiento: {"fecha", "accion", "detalle", "usuario"}
# ============================================================

#importa los modulos necesarios para manejar el historial de los expedientes.
from data.expedientes import ahora, guardar_expedientes


# Funcion para registar historial de un expediente, tomando como parametros el expediente, 
# la accion realizada, el detalle de la accion y el usuario que realizo la accion.
def registrar_historial(exp, accion, detalle="", usuario=""):
    """Agrega un movimiento al historial del expediente y guarda los datos."""
    exp["historial"].append({
        "fecha": ahora(),
        "accion": accion,
        "detalle": detalle,
        "usuario": usuario,
    })
    guardar_expedientes()

#definicion de la funcion ver_historial, que toma como parametro un expediente y muestra en 
# pantalla todos los movimientos del expediente.
def ver_historial(exp):
    """Muestra en pantalla todos los movimientos de un expediente."""
    print(f"\nHISTORIAL - {exp['codigo']}")
    print("-" * 48)
    if not exp["historial"]:
        print("  Sin movimientos registrados.")
    for mov in exp["historial"]:
        print(mov["fecha"])
        detalle = f" | {mov['detalle']}" if mov["detalle"] else ""
        print(f"  {mov['accion']}{detalle}")
        if mov["usuario"]:
            print(f"  Usuario: {mov['usuario']}")
    print("-" * 48)

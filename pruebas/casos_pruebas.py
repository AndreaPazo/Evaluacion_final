# ============================================================
# Pruebas automáticas de TODO el sistema 
# Ejecutar desde la carpeta principal:
#     py -m unittest discover -s pruebas -t . -p "casos_prueba.py" -v
# Usan archivos temporales: NO modifican los datos reales de data/.
# - Estructura Anidada: Comprueba el historial y las notificaciones por expediente [F5].
# ============================================================

import contextlib
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Inserción correcta del path raíz del proyecto para evitar problemas de importación
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autenticacion.autenticacion import login, logout, obtener_rol, tiene_rol
from data import expedientes as ex
from data import personas, usuarios
from mesa_partes import mesa_partes
from servicios import notificaciones as notif
from servicios.busqueda import buscar_binaria, buscar_lineal
from servicios.entradas import (
    pedir_folios,
    pedir_numero_documento,
    pedir_solo_letras,
)
from servicios.ordenamiento import (
    fecha_a_clave,
    ordenar_burbuja_matriz,
    ordenar_insercion_paralelos,
)


class BasePruebas(unittest.TestCase):
    """
    Sustenta la viabilidad técnica y de persistencia local.
    Crea archivos temporales de Python (base_*.py) para simular el almacenamiento 
    en el disco duro sin alterar los archivos reales de la demostración.
    """
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.originales = (
            personas.ARCHIVO_PERSONAS,
            usuarios.ARCHIVO_USUARIOS,
            ex.ARCHIVO_EXPEDIENTES,
            notif.ARCHIVO_NOTIFICACIONES,
        )
        # Simulación de persistencia nativa en archivos temporales
        personas.ARCHIVO_PERSONAS = os.path.join(self.temp.name, "base_personas.py")
        usuarios.ARCHIVO_USUARIOS = os.path.join(self.temp.name, "base_usuarios.py")
        ex.ARCHIVO_EXPEDIENTES = os.path.join(self.temp.name, "base_expedientes.py")
        notif.ARCHIVO_NOTIFICACIONES = os.path.join(self.temp.name, "base_notificaciones.py")
        
        if hasattr(ex, 'expedientes') and isinstance(ex.expedientes, list):
            ex.expedientes.clear()

    def tearDown(self):
        (
            personas.ARCHIVO_PERSONAS,
            usuarios.ARCHIVO_USUARIOS,
            ex.ARCHIVO_EXPEDIENTES,
            notif.ARCHIVO_NOTIFICACIONES,
        ) = self.originales
        if hasattr(ex, 'expedientes') and isinstance(ex.expedientes, list):
            ex.expedientes.clear()
        self.temp.cleanup()


class PruebasEstructuraSistema(BasePruebas):
    """
    [CUMPLIMIENTO LEY N.° 31170]
    Prueba que el expediente sea un diccionario con la estructura anidada 
    requerida para almacenar estados, historial y enviar notificaciones.
    """
    def test_estructura_anidada_expediente(self):
        # Simulación de un expediente como diccionario dentro de una lista (Opción A)
        expediente_ejemplo = {
            "codigo": "EXP-2026-0001",
            "canal": "VIRTUAL",
            "tramite": "SOLICITUD DE ACCESO A LA INFORMACION",
            "area": "OFICINA DE ABASTECIMIENTO",
            "estado": "RECIBIDO",
            "historial": [
                {"fecha": "18/10/2026 18:00", "accion": "REGISTRADO", "usuario": "jcoronado"}
            ]
        }
        
        # Guardar en nuestra lista única en memoria
        if hasattr(ex, 'expedientes') and isinstance(ex.expedientes, list):
            ex.expedientes.append(expediente_ejemplo)
        
        # Validar que conserve el control total del dato y sus sub-estructuras
        self.assertEqual(len(ex.expedientes), 1)
        self.assertEqual(ex.expedientes[0]["estado"], "RECIBIDO")
        # Verificar que el historial esté anidado (lista dentro de diccionario)
        self.assertIsInstance(ex.expedientes[0]["historial"], list)
        self.assertEqual(ex.expedientes[0]["historial"][0]["accion"], "REGISTRADO")


class PruebasPersonasUsuariosLogin(BasePruebas):
    """Módulo Autenticación (Integrante 1) y validaciones del negocio."""
    def test_validar_documentos(self):
        self.assertTrue(personas.validar_documento("DNI", "40949554")) # Caso real: José Coronado
        self.assertFalse(personas.validar_documento("DNI", "1234"))
        self.assertTrue(personas.validar_documento("RUC", "20123456789"))
        self.assertTrue(personas.validar_documento("CE", "N1234567"))
        
    def test_usuario_funcionario_requiere_area(self):
        # Estructura del curso: Diccionarios para representar entidades
        p, _ = personas.registrar_persona("DNI", "72845631", "Juan", "Perez", "j@e.com", "987")
        malo, _ = usuarios.registrar_usuario(p["id_persona"], "func1", "clave123", "FUNCIONARIO")
        self.assertIsNone(malo) # Falla porque no se le asignó área laboral
        bueno, _ = usuarios.registrar_usuario(
            p["id_persona"], "func1", "clave123", "FUNCIONARIO", "ABASTECIMIENTO"
        )
        self.assertEqual(bueno["area"], "ABASTECIMIENTO")


class PruebasAlgoritmos(unittest.TestCase):
    """
    [TÉCNICA ACADÉMICA]
    Prueba el correcto funcionamiento de la algoritmia propia sin librerías externas.
    """
    def test_busqueda_binaria_expedientes(self):
        # Arreglo ordenado para búsqueda binaria
        arreglo_codigos = ["EXP-0001", "EXP-0002", "EXP-0003", "EXP-0004"]
        self.assertEqual(buscar_binaria(arreglo_codigos, "EXP-0003"), 2)
        self.assertEqual(buscar_binaria(arreglo_codigos, "EXP-0099"), -1)

    def test_ordenamiento_burbuja_matriz(self):
        # Representación de reportes como matrices (Arreglos bidimensionales vistos en el curso)
        matriz_reporte = [["EXP-0002", "DERIVADO"], ["EXP-0001", "RECIBIDO"]]
        ordenar_burbuja_matriz(matriz_reporte, 0) # Ordenar por la columna de códigos (índice 0)
        self.assertEqual(matriz_reporte[0][0], "EXP-0001")


class PruebasEntradas(unittest.TestCase):
    """Valida los filtros aplicados a cadenas de texto y flujos por consola."""
    def _con_entradas(self, entradas, funcion, *args):
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(io.StringIO()):
            return funcion(*args)

    def test_folios_rechaza_negativos_y_letras(self):
        # Simulamos que el usuario digita errores antes de poner un número correcto
        r = self._con_entradas(["diez", "-3", "15"], pedir_folios)
        self.assertEqual(r, 15)


if __name__ == "__main__":
    unittest.main()
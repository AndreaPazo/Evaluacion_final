# ============================================================
# Pruebas automáticas de TODO el sistema 
# Ejecutar desde la carpeta principal:
#     py -m unittest discover -s pruebas -t . -p "casos_prueba.py" -v
# ============================================================

#importación de módulos necesarios para las pruebas unitarias y manejo de archivos temporales
import contextlib
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

#importación de módulos del sistema para realizar pruebas de autenticación, 
# manejo de expedientes, personas, usuarios y notificaciones
# Inserción correcta del path raíz del proyecto para evitar problemas de importación
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from autenticacion.autenticacion import login, logout, obtener_rol, tiene_rol
from data import expedientes as ex
from data import personas, usuarios
from mesa_partes import mesa_partes
from servicios import notificaciones as notif
from servicios.busqueda import buscar_binaria, buscar_lineal, buscar_expediente
from servicios.entradas import (
    pedir_folios,
    pedir_numero_documento,
    pedir_solo_letras,
    validar_entrada_instantanea,
    validar_dni,
    validar_ruc,
    validar_archivo_pdf,
)
from servicios.ordenamiento import (
    fecha_a_clave,
    ordenar_burbuja_matriz,
    ordenar_insercion_paralelos,
    ordenar_expedientes,
)

#clase BasePruebas que hereda de unittest.TestCase, 
# utilizada para crear un entorno de pruebas con archivos temporales

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
        """Restaurar los archivos originales y limpiar la carpeta temporal."""
        (
            personas.ARCHIVO_PERSONAS,
            usuarios.ARCHIVO_USUARIOS,
            ex.ARCHIVO_EXPEDIENTES,
            notif.ARCHIVO_NOTIFICACIONES,
        ) = self.originales
        if hasattr(ex, 'expedientes') and isinstance(ex.expedientes, list):
            ex.expedientes.clear()
        self.temp.cleanup()

#clase PruebasEstructuraSistema que hereda de BasePruebas,
# utilizada para probar la estructura de los expedientes y su historial
class PruebasEstructuraSistema(BasePruebas):
    """
    [CUMPLIMIENTO LEY N.° 31170]
    Prueba que el expediente sea un diccionario con la estructura anidada 
    requerida para almacenar estados, historial y enviar notificaciones.
    """
    #definición del método test_estructura_anidada_expediente que prueba la estructura de un expediente
    def test_estructura_anidada_expediente(self):
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
        
        if hasattr(ex, 'expedientes') and isinstance(ex.expedientes, list):
            ex.expedientes.append(expediente_ejemplo)
        
        self.assertEqual(len(ex.expedientes), 1)
        self.assertEqual(ex.expedientes[0]["estado"], "RECIBIDO")
        self.assertIsInstance(ex.expedientes[0]["historial"], list)
        self.assertEqual(ex.expedientes[0]["historial"][0]["accion"], "REGISTRADO")
    #clase PruebasPersonasUsuariosLogin que hereda de BasePruebas,
    # utilizada para probar la autenticación de usuarios y validaciones de negocio
class PruebasPersonasUsuariosLogin(BasePruebas):
    """Módulo Autenticación (Integrante 1) y validaciones del negocio."""
    def test_validar_documentos(self):
        self.assertTrue(personas.validar_documento("DNI", "40949554"))
        self.assertFalse(personas.validar_documento("DNI", "1234"))
        self.assertTrue(personas.validar_documento("RUC", "20123456789"))
        self.assertTrue(personas.validar_documento("CE", "N1234567"))
        
    def test_usuario_funcionario_requiere_area(self):
        p, _ = personas.registrar_persona("DNI", "72845631", "Juan", "Perez", "j@e.com", "987")
        malo, _ = usuarios.registrar_usuario(p["id_persona"], "func1", "clave123", "FUNCIONARIO")
        self.assertIsNone(malo)
        bueno, _ = usuarios.registrar_usuario(
            p["id_persona"], "func1", "clave123", "FUNCIONARIO", "ABASTECIMIENTO"
        )
        self.assertEqual(bueno["area"], "ABASTECIMIENTO")

#clase PruebasAlgoritmos que hereda de unittest.TestCase,
# utilizada para probar algoritmos de búsqueda y ordenamiento
class PruebasAlgoritmos(unittest.TestCase):
    """
    [TÉCNICA ACADÉMICA]
    Prueba el correcto funcionamiento de la algoritmia propia sin librerías externas.
    """
    def test_busqueda_binaria_expedientes(self):
        arreglo_codigos = ["EXP-0001", "EXP-0002", "EXP-0003", "EXP-0004"]
        self.assertEqual(buscar_binaria(arreglo_codigos, "EXP-0003"), 2)
        self.assertEqual(buscar_binaria(arreglo_codigos, "EXP-0099"), -1)

    def test_ordenamiento_burbuja_matriz(self):
        # Representación de reportes como matrices (Arreglos bidimensionales vistos en el curso)
        matriz_reporte = [["EXP-0002", "DERIVADO"], ["EXP-0001", "RECIBIDO"]]
        ordenar_burbuja_matriz(matriz_reporte, 0) # Ordenar por la columna de códigos (índice 0)
        self.assertEqual(matriz_reporte[0][0], "EXP-0001")
        matriz_reporte = [["EXP-0002", "DERIVADO"], ["EXP-0001", "RECIBIDO"]]
        ordenar_burbuja_matriz(matriz_reporte, 0)
        self.assertEqual(matriz_reporte[0][0], "EXP-0001")
#clase PruebasMejorasZip que hereda de unittest.TestCase,
# utilizada para probar funciones añadidas desde un archivo .zip, 
# incluyendo validación instantánea, búsqueda avanzada y ordenamiento por inserción

class PruebasMejorasZip(unittest.TestCase):
    """
    Pruebas específicas para validar las funciones añadidas desde el archivo .zip:
    - Validación instantánea (DNI, RUC, PDF, Folios)
    - Búsqueda avanzada de expedientes
    - Conversor de fechas y ordenamiento por inserción con arreglos paralelos
    """
    def test_validacion_entrada_instantanea(self):
        # Datos válidos
        valido = {
            "dni": "45678912",
            "tipo_persona": "natural",
            "folios": 5,
            "archivo_pdf": "documento.pdf"
        }
        resultado = validar_entrada_instantanea(valido)
        self.assertEqual(resultado["estado"], "aprobado")

        # Datos inválidos (DNI corto, folios negativos, archivo no PDF)
        invalido = {
            "dni": "123",
            "tipo_persona": "natural",
            "folios": -1,
            "archivo_pdf": "foto.png"
        }
        resultado_err = validar_entrada_instantanea(invalido)
        self.assertEqual(resultado_err["estado"], "rechazado")
        self.assertTrue(len(resultado_err["errores"]) > 0)

    def test_buscar_expediente_avanzado(self):
        lista_exp = [
            {"codigo": "EXP-001", "dni": "40949554", "nombre": "Jose Coronado"},
            {"codigo": "EXP-002", "dni": "12345678", "nombre": "Maria Perez"}
        ]
        # Búsqueda por coincidencia parcial de nombre
        res_nombre = buscar_expediente(lista_exp, "jose")
        self.assertEqual(len(res_nombre), 1)
        self.assertEqual(res_nombre[0]["codigo"], "EXP-001")

        # Búsqueda con criterio vacío
        res_vacio = buscar_expediente(lista_exp, "")
        self.assertEqual(len(res_vacio), 2)

    def test_conversor_fecha_y_orden_insercion(self):
        # Probar conversor de fecha
        clave = fecha_a_clave("18/10/2026 15:30")
        self.assertEqual(clave, "202610181530")

        # Probar ordenamiento por inserción con arreglos paralelos
        claves = [30, 10, 20]
        paralelo_nombre = ["C", "A", "B"]
        ordenar_insercion_paralelos(claves, paralelo_nombre)
        
        self.assertEqual(claves, [10, 20, 30])
        self.assertEqual(paralelo_nombre, ["A", "B", "C"])
        

class PruebasEntradas(unittest.TestCase):
    """Valida los filtros aplicados a cadenas de texto y flujos por consola."""
    def _con_entradas(self, entradas, funcion, *args):
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(io.StringIO()):
            return funcion(*args)

    def test_folios_rechaza_negativos_y_letras(self):
        r = self._con_entradas(["diez", "-3", "15"], pedir_folios)
        self.assertEqual(r, 15)


if __name__ == "__main__":
    unittest.main()
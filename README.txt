========================================================================
   MESA DE PARTES FÍSICA Y VIRTUAL - PROTOTIPO PARA UNA ENTIDAD
========================================================================

REQUISITOS: Python 3.8 o superior. No hay que instalar nada. Sin base de datos SQL.

EJECUTAR (desde esta carpeta):     python main.py        (Windows: py main.py)
VERIFICAR QUE COMPILA TODO:        python -m compileall .
EJECUTAR PRUEBAS AUTOMÁTICAS:      py -m unittest discover -s pruebas -t . -p "casos_prueba.py" -v

ESTADO DEL AVANCE
  [LISTO]           Autenticación: login, logout, registro de ciudadano (Integrante 1 y 2)
  [LISTO]           Mesa de Partes: recepción física y virtual, 5 trámites, consulta,
                    derivación, anulación, reportes, notificaciones     (Integrante 2)
  [LISTO]           Ciudadano: casilla electrónica, nueva solicitud, mis expedientes,
                    seguimiento, notificaciones, constancias            (Integrante 4)
  [EN CONSTRUCCIÓN] Administrador (panel de personas, usuarios, roles y áreas)  (Integrante 1)
  [EN CONSTRUCCIÓN] Funcionario (bandeja, aceptar, observar, atender, archivar) (Integrante 3)
  [EN CONSTRUCCIÓN] Subsanación de observaciones por el ciudadano (depende de Funcionario)

USUARIOS DE EJEMPLO (datos en duro, solo para la demostración)
  mesa01       / mesa123    MESA_PARTES
  jcoronado    / clave123   CIUDADANO  (caso real: José Javier Coronado Ramos, DNI 40949554)
  jperez       / clave123   CIUDADANO  (Juan Pérez García, DNI 72845631)
  Persona 3 (María López, CE) está INACTIVA a propósito, para probar validaciones.
  
  Cuentas ya creadas para los módulos en construcción (al ingresar se muestra "módulo en construcción"):
  admin        / admin123   ADMINISTRADOR
  func_rrhh    / func123    FUNCIONARIO (RECURSOS HUMANOS)
  func_abast   / func123    FUNCIONARIO (ABASTECIMIENTO)

ESTRUCTURA DEL REPOSITORIO
main.py                          Integrador: login -> rol -> módulo del rol.
data/                            Datos en duro (listas/diccionarios guardados en archivos .py)
  almacen.py                     Lee/guarda listas en archivos base_*.py (con copia .bak)
  personas.py  usuarios.py       Personas (DNI/CE/RUC), usuarios, roles, contraseñas con hash
  areas.py  tramites.py          Áreas y los 5 trámites del MEF
  expedientes.py                 ÚNICA lista de expedientes (memoria + archivo)
  base_*.py                      Archivos de datos dinámica que escribe el sistema
autenticacion/                   login, logout, registro de ciudadano                 (Integrante 1)
mesa_partes/                     Recepción física y virtual, 5 trámites, anulación    (Integrante 2)
ciudadano/                       Casilla electrónica, solicitudes, seguimiento        (Integrante 4)
servicios/                       Compartido: entradas, historial, notificaciones,
                                 busqueda (lineal/binaria), ordenamiento (burbuja/inserción), reportes
pruebas/                         Suite automatizada de 27 casos de prueba unitarios
docs/                            Paquete exclusivo de documentación para auditoría de rúbrica
  ├── bizagi/                    Diagramas de flujo preliminares (.bpm y .png)
  └── pseint/                    Pseudocódigos oficiales (.psc)
       └── registro_expediente.psc  (Integrante 3)

CONTENIDOS DE LA ASIGNATURA EN EVIDENCIA
  Estructuras de control (if/while/for) .... todos los menús y validaciones interactivos
  Funciones y módulos ...................... cada carpeta es un paquete de código reutilizable
  Arreglos y matrices ...................... servicios/reportes.py (construir_matriz)
  Arreglos paralelos ....................... servicios/reportes.py (codigos, estados, areas, fechas...)
  Cadenas de caracteres .................... validar_n_orden, fecha_a_clave, formato_id, strip/upper/split
  Búsqueda ................................. servicios/busqueda.py (lineal y binaria)
  Ordenamiento ............................. servicios/ordenamiento.py (burbuja e inserción)
  Archivos / persistencia .................. data/almacen.py + data/base_*.py
  Booleanos ................................ validar_documento(), validar_n_orden(), anulado
  Manejo de errores (try/except) ........... data/almacen.py (ArchivoDanado) y main.py

FLUJO DEL EXPEDIENTE
  Implementado en este avance:
    RECIBIDO -> DERIVADO
    RECIBIDO -> ANULADO (el expediente NO se elimina; queda en el historial lógico)
  Pendiente (módulo Funcionario para fases de auditoría):
    DERIVADO -> EN_PROCESO -> OBSERVADO -> SUBSANADO -> ATENDIDO -> ARCHIVADO
  Cada cambio guarda el historial y envía una notificación a la casilla del ciudadano.

PROTECCIÓN DE DATOS
  Cada vez que se guarda un archivo base_*.py, la versión anterior queda como base_*.py.bak.
  Si un archivo de datos está dañado, el programa se detiene con un mensaje
  en lugar de sobrescribirlo. Para recuperarlo: copie base_X.py.bak sobre base_X.py.

REINICIAR DATOS (para repetir la demo desde cero)
  En data/base_expedientes.py deje solamente:    EXPEDIENTES = []
  En data/base_notificaciones.py deje solamente: NOTIFICACIONES = []

GIT CONTROL:
  Cada integrante trabaja su carpeta en una rama (feature/...) con commits pequeños
  y mensajes bajo el estándar corporativo (feat, docs, chore).
========================================================================

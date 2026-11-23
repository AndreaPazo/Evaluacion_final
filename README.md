# Mesa de Partes Física y Virtual — Backend (Python + SQL Server)

Prototipo de mesa de partes digital para una entidad pública (Ley N.° 31170).
Curso: Fundamentos de Programación (CIIN1205P) · Marco ágil: Scrum.

## Requisitos
- Python 3.8 o superior (Windows; el laboratorio usa Git Bash / VS Code).
- SQL Server (Express sirve) y **ODBC Driver 17 o 18 for SQL Server**.
- Librería: `pip install -r requirements.txt` (solo `pyodbc`).

## Puesta en marcha (3 pasos)
1. **Crear la base:** abrir `SQL/mesa_partes.sql` en SSMS y ejecutarlo completo.
   Crea la base `MesaPartes`, las 8 tablas y los datos iniciales. Si la base ya tiene tablas, el script se omite solo (no duplica datos).
2. **Conexión:** `data/conexion.py` es el único archivo de configuración.
   - Windows (laboratorio): no hay que cambiar nada; prueba `localhost\SQLEXPRESS`, `localhost` y `(localdb)\MSSQLLocalDB` con Autenticación de Windows.
   - Docker o usuario/clave de SQL Server: definir variables de entorno antes de ejecutar
     `MESAPARTES_USUARIO`, `MESAPARTES_CLAVE` y, si hace falta, `MESAPARTES_SERVIDOR` (por defecto `localhost,1433`).
     Ejemplo en Git Bash: `export MESAPARTES_USUARIO=sa MESAPARTES_CLAVE='SuClave'`
3. **Ejecutar:** `py main.py` (o `python main.py`).

Si SQL Server no responde, el programa muestra "No se pudo conectar a la base de datos" y se detiene sin error técnico.

## Pruebas automáticas
```
py -m unittest discover -s pruebas -t . -p "casos_pruebas.py" -v
```
Crean y usan su propia base `MesaPartes_Pruebas` (se borra y se recrea con el mismo script SQL). **Nunca tocan la base real.**
Cubren HU-01 a HU-08, HU-12, HU-13, HU-14, el flujo completo CP-08.5, la atomicidad estado + historial y los 5 trámites.
Verificar que todo compila: `py -m compileall .`

## Usuarios de demostración
| Usuario | Contraseña | Rol |
|---|---|---|
| mesa01 | mesa123 | MESA_PARTES |
| jcoronado | clave123 | CIUDADANO (DNI 40949554) |
| jperez | clave123 | CIUDADANO (DNI 72845631) |
| admin | admin123 | ADMINISTRADOR |
| func_rrhh | func123 | FUNCIONARIO · RECURSOS HUMANOS |
| func_abast | func123 | FUNCIONARIO · ABASTECIMIENTO |

`mlopez` (María López, CE A1234567) está INACTIVA a propósito para probar validaciones.
Cambiar estas contraseñas antes de usar el sistema con datos reales.

## Estructura
```
main.py                 login -> rol -> módulo del rol
SQL/mesa_partes.sql     8 tablas en 3FN + datos iniciales (idempotente)
SQL/limpiar_expedientes.sql   reinicia solo expedientes/historial/notificaciones (demo)
data/                   acceso a SQL Server: conexion, areas, tramites, personas, usuarios, expedientes
autenticacion/          login, logout, registro de ciudadano
mesa_partes/            recepción física y virtual, anulación, derivación
funcionario/            bandeja y reglas de estado (aceptar, derivar, observar, atender, archivar)
ciudadano/              casilla electrónica, solicitudes, seguimiento, subsanación
administrador/          personas, usuarios, roles y áreas
servicios/              entradas, historial, notificaciones, búsqueda, ordenamiento, reportes
pruebas/                suite automática y creación de la base de pruebas
pseint/                 pseudocódigo
```

## Flujo del expediente
```
RECIBIDO -> DERIVADO -> EN_PROCESO -> ATENDIDO -> ARCHIVADO
                         EN_PROCESO -> OBSERVADO -> SUBSANADO -> (observar de nuevo o atender)
RECIBIDO -> ANULADO      (no se elimina)
El funcionario puede derivar a otra área con motivo (queda DERIVADO).
```
Cada cambio guarda estado e historial **en una sola transacción** y notifica a la casilla del ciudadano.

## Protección de datos
- Restricciones `UNIQUE`, `CHECK` y llaves foráneas en la base: la data inválida o duplicada la rechaza SQL Server.
- Contraseñas guardadas con hash PBKDF2 con sal (nunca en texto claro).
- Consultas con parámetros `?` (sin concatenar texto: evita inyección SQL).
- Las pruebas usan otra base; el script de reinicio solo borra movimientos de la demo.

## Control de versiones
Ramas `feature/...` por integrante, commits pequeños con prefijo `feat`, `fix`, `test`, `docs`, `chore`.
Versión con archivos en duro respaldada en la etiqueta `v1-archivos`.

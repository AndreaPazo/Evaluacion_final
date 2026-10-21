// ESTRUCTURAS DE DATOS (todas de tipo Caracter, salvo cnt)
//   per[i, 1..8]   PERSONAS: 1 id_persona, 2 tipo_documento,
//                  3 numero_documento, 4 nombres, 5 apellidos,
//                  6 correo, 7 telefono, 8 estado
//   usu[i, 1..7]   USUARIOS: 1 id_usuario, 2 id_persona,
//                  3 nombre_usuario, 4 contrasena, 5 rol, 6 area, 7 estado
//   ex[i, 1..22]   EXPEDIENTES: 1 codigo, 2 id_persona,
//                  3 tipo_identificacion, 4 numero_identificacion,
//                  5 administrado, 6 canal, 7 casilla, 8 tramite,
//                  9 subtipo, 10 area, 11 asunto, 12 folios,
//                  13 area_laboro, 14 n_orden, 15 firma, 16 adjunto,
//                  17 registrado_por, 18 estado, 19 fecha_registro,
//                  20 motivo_anulacion, 21 anulado (SI/NO),
//                  22 codigo_constancia
//   his[i, 1..5]   HISTORIAL: 1 codigo_expediente, 2 fecha, 3 accion,
//                  4 detalle, 5 usuario
//   noti[i, 1..7]  NOTIFICACIONES: 1 id_notificacion, 2 id_persona,
//                  3 codigo_expediente, 4 tipo, 5 mensaje, 6 fecha,
//                  7 leida (SI/NO)
//   cnt[1..5]      Cantidad de filas usadas: 1 personas, 2 usuarios,
//                  3 expedientes, 4 historial, 5 notificaciones
//   ses[1..6]      SESIÓN: 1 id_usuario, 2 usuario, 3 rol,
//                  4 id_persona, 5 area, 6 nombre_completo
// ============================================================

// MÓDULO: main.py  (programa principal)
Algoritmo MesaDePartes
	Definir per, usu, ex, his, noti, ses Como Caracter;
	Definir cnt Como Entero;
	Dimension per[101, 9];		// Data maestra de Personas
	Dimension usu[101, 8];  	// Cuentas y credenciales de Usuarios
	Dimension ex[201, 23]; 	// Expedientes registrados
	Dimension his[1001, 6]; 	// Historial de trazabilidad
	Dimension noti[1001, 8];  	// Notificaciones y Casilla Electrónica
	Dimension cnt[6]; 			// Contadores de registros activos
	Dimension ses[7]; 			// Control de sesión activa

	// iniciar_sistema(): carga la data en duro y abre el menú principal
	CargarDatosIniciales(per, usu, cnt);
	LimpiarSesion(ses);
	Escribir "Sistema iniciado de manera correcta. Expedientes cargados: ", cnt[3];
	MenuPrincipal(ses, per, usu, ex, his, noti, cnt);
FinAlgoritmo

SubProceso MenuPrincipal(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	Definir opc Como Entero;
	Repetir
		Escribir "";
		Escribir LineaDe("=", 48);
		Escribir " MESA DE PARTES FÍSICA Y VIRTUAL - ENTIDAD";
		Escribir LineaDe("=", 48);
		Escribir "1. Iniciar sesión";
		Escribir "2. Registrarse como ciudadano";
		Escribir "0. Salir";
		opc <- LeerNumeroMenu("Seleccione una opción: ");
		Segun opc Hacer
			1:
				OpcionLogin(ses, per, usu, ex, his, noti, cnt);
			2:
				RegistroCiudadano(per, usu, cnt);
			0:
				Escribir "Programa finalizado. Los datos se mantienen solo mientras PSeInt está abierto.";
			De Otro Modo:
				Escribir "Opción incorrecta. Intente nuevamente.";
		FinSegun
	Hasta Que opc = 0
FinSubProceso

SubProceso OpcionLogin(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	// Inicia sesión, dirige al módulo del rol y cierra la sesión al volver
	Definir nombre, contrasena, mensaje, rol Como Caracter;
	Definir ok Como Logico;
	Escribir "";
	Escribir "--- INICIAR SESIÓN ---";
	Escribir "Usuario: " Sin Saltar;
	Leer nombre;
	contrasena <- PedirContrasena("Contraseña", "--- INICIAR SESIÓN ---", Recortar(nombre));
	mensaje <- "";
	ok <- IniciarSesion(per, usu, cnt, nombre, contrasena, ses, mensaje);
	Escribir mensaje;
	Si ok Entonces
		Escribir "";
		Escribir "Bienvenido/a: ", ses[6], " | Rol: ", ses[3];
		rol <- ses[3];
		// Equivale al diccionario MODULOS_POR_ROL
		Si rol = "MESA_PARTES" Entonces
			MenuMesaPartes(ses, per, usu, ex, his, noti, cnt);
		SiNo
			Si rol = "CIUDADANO" Entonces
				MenuCiudadano(ses, per, usu, ex, his, noti, cnt);
			SiNo
				Si rol = "ADMINISTRADOR" O rol = "FUNCIONARIO" Entonces
					Escribir "";
					Escribir "[AVISO] El módulo del rol ", rol, " todavía está en construcción para la entrega final.";
				SiNo
					Escribir "";
					Escribir "[ERROR] Rol no reconocido por el sistema de seguridad.";
				FinSi
			FinSi
		FinSi
		CerrarSesion(ses, mensaje);
		Escribir mensaje;
	FinSi
FinSubProceso

// DATOS EN DURO: data/base_personas.py y data/base_usuarios.py
SubProceso CargarDatosIniciales(per Por Referencia, usu Por Referencia, cnt Por Referencia)
	cnt[1] <- 0;
	cnt[2] <- 0;
	cnt[3] <- 0;
	cnt[4] <- 0;
	cnt[5] <- 0;
	AgregarPersonaBase(per, cnt, "1", "DNI", "40949554", "JOSE JAVIER", "CORONADO RAMOS", "josecoronadoramos@gmail.com", "985951485", "ACTIVO");
	AgregarPersonaBase(per, cnt, "2", "DNI", "72845631", "JUAN", "PEREZ GARCIA", "juan@gmail.com", "987654321", "ACTIVO");
	AgregarPersonaBase(per, cnt, "3", "CE", "123456789", "MARIA", "LOPEZ DIAZ", "maria@gmail.com", "999111222", "INACTIVO");
	AgregarPersonaBase(per, cnt, "4", "DNI", "10000001", "ADMIN", "SISTEMA", "admin@entidad.gob.pe", "900000001", "ACTIVO");
	AgregarPersonaBase(per, cnt, "5", "DNI", "10000002", "MESA", "PARTES UNO", "mesa@entidad.gob.pe", "900000002", "ACTIVO");
	AgregarPersonaBase(per, cnt, "6", "DNI", "10000003", "FUNCIONARIO", "RRHH", "rrhh@entidad.gob.pe", "900000003", "ACTIVO");
	AgregarPersonaBase(per, cnt, "7", "DNI", "10000004", "FUNCIONARIO", "ABASTECIMIENTO", "abast@entidad.gob.pe", "900000004", "ACTIVO");
	
	// data/base_usuarios.py (en Python la contraseña se guarda como hash;
	// aquí se guarda legible solo para la demostración)
	AgregarUsuarioBase(usu, cnt, "1", "1", "jcoronado", "clave123", "CIUDADANO", "", "ACTIVO");
	AgregarUsuarioBase(usu, cnt, "2", "2", "jperez", "clave123", "CIUDADANO", "", "ACTIVO");
	AgregarUsuarioBase(usu, cnt, "3", "3", "admin", "admin123", "ADMINISTRADOR", "", "ACTIVO");
	AgregarUsuarioBase(usu, cnt, "4", "4", "mesa01", "mesa123", "MESA_PARTES", "", "ACTIVO");
	AgregarUsuarioBase(usu, cnt, "5", "5", "func_rrhh", "func123", "FUNCIONARIO", "RECURSOS HUMANOS", "ACTIVO");
	AgregarUsuarioBase(usu, cnt, "6", "6", "func_abast", "func123", "FUNCIONARIO", "ABASTECIMIENTO", "ACTIVO");
	
FinSubProceso

SubProceso AgregarPersonaBase(per Por Referencia, cnt Por Referencia, idp, tipo, numDoc, nombres, apellidos, correo, telefono, estado)
	Definir i Como Entero;
	cnt[1] <- cnt[1] + 1;
	i <- cnt[1];
	per[i, 1] <- idp;
	per[i, 2] <- tipo;
	per[i, 3] <- numDoc;
	per[i, 4] <- nombres;
	per[i, 5] <- apellidos;
	per[i, 6] <- correo;
	per[i, 7] <- telefono;
	per[i, 8] <- estado;
FinSubProceso

SubProceso AgregarUsuarioBase(usu Por Referencia, cnt Por Referencia, idu, idp, nombreUsuario, contrasena, rol, area, estado)
	Definir i Como Entero;
	cnt[2] <- cnt[2] + 1;
	i <- cnt[2];
	usu[i, 1] <- idu;
	usu[i, 2] <- idp;
	usu[i, 3] <- nombreUsuario;
	usu[i, 4] <- contrasena;
	usu[i, 5] <- rol;
	usu[i, 6] <- area;
	usu[i, 7] <- estado;
FinSubProceso

// FUNCIONES DE APOYO PARA CADENAS (reemplazan a strip, isdigit,
// isalpha, endswith, split, zfill, "=" * n ... de Python)
Funcion r <- Trozo(s, pIni, pFin)
	// Igual que Subcadena, pero las posiciones SIEMPRE empiezan en 1,
	// funcione PSeInt en base 0 o en base 1 (depende del perfil).
	Definir r Como Caracter;
	Si Subcadena("AB", 1, 1) = "B" Entonces
		r <- Subcadena(s, pIni - 1, pFin - 1);
	SiNo
		r <- Subcadena(s, pIni, pFin);
	FinSi
FinFuncion

Funcion r <- LineaDe(c, n)
	// Equivale a  c * n  en Python. Ejemplo: LineaDe("=", 3) -> "==="
	Definir r Como Caracter;
	Definir i Como Entero;
	r <- "";
	Para i <- 1 Hasta n Con Paso 1 Hacer
		r <- Concatenar(r, c);
	FinPara
FinFuncion

Funcion r <- Recortar(s)
	// Equivale a  s.strip()  (quita espacios al inicio y al final)
	Definir r Como Caracter;
	Definir ini, ult Como Entero;
	Definir seguir Como Logico;
	ini <- 1;
	ult <- Longitud(s);
	seguir <- Verdadero;
	Mientras seguir Hacer
		Si ini > ult Entonces
			seguir <- Falso;
		SiNo
			Si Trozo(s, ini, ini) = " " Entonces
				ini <- ini + 1;
			SiNo
				seguir <- Falso;
			FinSi
		FinSi
	FinMientras
	seguir <- Verdadero;
	Mientras seguir Hacer
		Si ult < ini Entonces
			seguir <- Falso;
		SiNo
			Si Trozo(s, ult, ult) = " " Entonces
				ult <- ult - 1;
			SiNo
				seguir <- Falso;
			FinSi
		FinSi
	FinMientras
	Si ini > ult Entonces
		r <- "";
	SiNo
		r <- Trozo(s, ini, ult);
	FinSi
FinFuncion

Funcion r <- EsDigito(c)
	Definir r Como Logico;
	r <- (c >= "0") Y (c <= "9");
FinFuncion

Funcion r <- SoloDigitos(s)
	// Equivale a  s.isdigit()
	Definir r Como Logico;
	Definir i Como Entero;
	r <- Longitud(s) > 0;
	Para i <- 1 Hasta Longitud(s) Con Paso 1 Hacer
		Si No EsDigito(Trozo(s, i, i)) Entonces
			r <- Falso;
		FinSi
	FinPara
FinFuncion

Funcion r <- ContieneCaracter(s, c)
	// Equivale a  c in s
	Definir r Como Logico;
	r <- ContarCaracter(s, c) > 0;
FinFuncion

Funcion r <- ContarCaracter(s, c)
	// Equivale a  s.count(c)
	Definir r, i Como Entero;
	r <- 0;
	Para i <- 1 Hasta Longitud(s) Con Paso 1 Hacer
		Si Trozo(s, i, i) = c Entonces
			r <- r + 1;
		FinSi
	FinPara
FinFuncion

Funcion r <- EsLetra(c)
	// Equivale a  c.isalpha()  (incluye vocales con tilde y la ñ)
	Definir r Como Logico;
	Definir u Como Caracter;
	u <- Mayusculas(c);
	r <- ((u >= "A") Y (u <= "Z")) O ContieneCaracter("ÁÉÍÓÚÜÑáéíóúüñ", c);
FinFuncion

Funcion r <- SoloLetrasMayusculas(s)
	// Equivale a  s.isalpha() and s.isupper()
	Definir r Como Logico;
	Definir i Como Entero;
	Definir c Como Caracter;
	r <- Longitud(s) > 0;
	Para i <- 1 Hasta Longitud(s) Con Paso 1 Hacer
		c <- Trozo(s, i, i);
		Si No EsLetra(c) Entonces
			r <- Falso;
		SiNo
			Si c <> Mayusculas(c) Entonces
				r <- Falso;
			FinSi
		FinSi
	FinPara
FinFuncion

Funcion r <- TerminaEn(s, sufijo)
	// Equivale a  s.endswith(sufijo)
	Definir r Como Logico;
	Definir ls, lf Como Entero;
	ls <- Longitud(s);
	lf <- Longitud(sufijo);
	r <- Falso;
	Si ls >= lf Y lf > 0 Entonces
		r <- Trozo(s, ls - lf + 1, ls) = sufijo;
	FinSi
FinFuncion

Funcion r <- ContieneTexto(s, sub)
	// Equivale a  sub in s  (sub puede tener varios caracteres)
	Definir r Como Logico;
	Definir i, ls, lb Como Entero;
	ls <- Longitud(s);
	lb <- Longitud(sub);
	r <- lb = 0;
	i <- 1;
	Mientras No r Y i + lb - 1 <= ls Hacer
		Si Trozo(s, i, i + lb - 1) = sub Entonces
			r <- Verdadero;
		FinSi
		i <- i + 1;
	FinMientras
FinFuncion

Funcion r <- ContarItems(lista, sep)
	// Cantidad de partes de  lista.split(sep)
	Definir r Como Entero;
	r <- ContarCaracter(lista, sep) + 1;
FinFuncion

Funcion r <- ObtenerItem(lista, k, sep)
	// Equivale a  lista.split(sep)[k-1]
	Definir r, c Como Caracter;
	Definir i, actual Como Entero;
	r <- "";
	actual <- 1;
	Para i <- 1 Hasta Longitud(lista) Con Paso 1 Hacer
		c <- Trozo(lista, i, i);
		Si c = sep Entonces
			actual <- actual + 1;
		SiNo
			Si actual = k Entonces
				r <- Concatenar(r, c);
			FinSi
		FinSi
	FinPara
FinFuncion

Funcion r <- NumATexto(n)
	// Convierte un entero no negativo en texto. Ejemplo: 25 -> "25"
	Definir r Como Caracter;
	Definir m, d Como Entero;
	m <- trunc(n);
	Si m = 0 Entonces
		r <- "0";
	SiNo
		r <- "";
		Mientras m > 0 Hacer
			d <- m MOD 10;
			r <- Concatenar(Trozo("0123456789", d + 1, d + 1), r);
			m <- trunc(m / 10);
		FinMientras
	FinSi
FinFuncion

Funcion r <- Rellenar(n, ancho)
	// Equivale a  str(n).zfill(ancho). Ejemplo: Rellenar(1, 6) -> "000001"
	Definir r Como Caracter;
	r <- NumATexto(n);
	Mientras Longitud(r) < ancho Hacer
		r <- Concatenar("0", r);
	FinMientras
FinFuncion

Funcion r <- PadDer(s, ancho)
	// Equivale a  f"{s:<ancho}"  (completa con espacios a la derecha)
	Definir r Como Caracter;
	r <- s;
	Mientras Longitud(r) < ancho Hacer
		r <- Concatenar(r, " ");
	FinMientras
FinFuncion

Funcion r <- FormatoFechaHora(f, h)
	// Equivale a  ahora()  ->  dd/mm/aaaa hh:mm
	// Se llama con FormatoFechaHora(FechaActual(), HoraActual()):
	// FechaActual() devuelve AAAAMMDD y HoraActual() devuelve HHMMSS
	Definir r Como Caracter;
	r <- Concatenar(Concatenar(Rellenar(f MOD 100, 2), "/"), Concatenar(Concatenar(Rellenar(trunc(f / 100) MOD 100, 2), "/"), NumATexto(trunc(f / 10000))));
	r <- Concatenar(Concatenar(r, " "), Concatenar(Concatenar(Rellenar(trunc(h / 10000), 2), ":"), Rellenar(trunc(h / 100) MOD 100, 2)));
FinFuncion

// MÓDULO: servicios/entradas.py  (pedir datos por consola)
Funcion r <- LeerOpcion(titulo, lista, cancelar)
	// Muestra un menú con las opciones separadas por "|" y repite
	// hasta elegir una válida. Devuelve el número elegido (0 = cancelar).
	Definir r, n, i Como Entero;
	Definir eleccion Como Caracter;
	n <- ContarItems(lista, "|");
	Repetir
		Escribir "";
		Escribir titulo;
		Para i <- 1 Hasta n Con Paso 1 Hacer
			Escribir "  ", i, ". ", ObtenerItem(lista, i, "|");
		FinPara
		Si cancelar Entonces
			Escribir "  0. Cancelar";
		FinSi
		Escribir "Seleccione: " Sin Saltar;
		Leer eleccion;
		eleccion <- Recortar(eleccion);
		r <- -1;
		Si cancelar Y eleccion = "0" Entonces
			r <- 0;
		SiNo
			Para i <- 1 Hasta n Con Paso 1 Hacer
				Si eleccion = NumATexto(i) Entonces
					r <- i;
				FinSi
			FinPara
		FinSi
		Si r = -1 Entonces
			Escribir "[ERROR] Opción no válida. Intente de nuevo.";
		FinSi
	Hasta Que r <> -1
FinFuncion

Funcion r <- LeerNumeroMenu(mensaje)
	// Lee la opción de un menú principal. Devuelve -1 si no es un número.
	Definir r Como Entero;
	Definir eleccion Como Caracter;
	Escribir mensaje Sin Saltar;
	Leer eleccion;
	eleccion <- Recortar(eleccion);
	Si SoloDigitos(eleccion) Y Longitud(eleccion) <= 2 Entonces
		r <- trunc(ConvertirANumero(eleccion));
	SiNo
		r <- -1;
	FinSi
FinFuncion

Funcion r <- LeerTexto(etiqueta)
	// Lee un texto y lo repite hasta que no esté vacío
	Definir r Como Caracter;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer r;
		r <- Recortar(r);
		Si r = "" Entonces
			Escribir "[ERROR] Este campo es obligatorio.";
		FinSi
	Hasta Que r <> ""
FinFuncion

Funcion r <- LeerEntero(etiqueta)
	// Pide un número entero y repite hasta que sea válido
	Definir r Como Entero;
	Definir dato Como Caracter;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer dato;
		dato <- Recortar(dato);
		Si No SoloDigitos(dato) Entonces
			Escribir "[ERROR] Debe ingresar un número entero.";
		FinSi
	Hasta Que SoloDigitos(dato)
	r <- trunc(ConvertirANumero(dato));
FinFuncion

Funcion r <- PedirContrasena(etiqueta, titulo, usuario)
	Definir r Como Caracter;
	Escribir etiqueta, ": " Sin Saltar;
	Leer r;
	// En Python solo se aceptan hasta 30 caracteres al escribir la clave
	Si Longitud(r) > 30 Entonces
		r <- Trozo(r, 1, 30);
	FinSi
	r <- Recortar(r);
	OcultarContrasena(titulo, usuario, etiqueta, Longitud(r));
FinFuncion

SubProceso OcultarContrasena(titulo, usuario, etiqueta, largo)
	Limpiar Pantalla;
	Escribir titulo;
	Escribir "Usuario: ", usuario;
	Escribir etiqueta, ": ", LineaDe("*", largo);
FinSubProceso

Funcion r <- PedirContrasenaRegistro(etiqueta, usuario)
	// La contraseña de registro debe tener entre 6 y 10 caracteres
	Definir r Como Caracter;
	Definir valido Como Logico;
	Repetir
		r <- PedirContrasena(etiqueta, "--- REGISTRO DE CIUDADANO ---", usuario);
		valido <- (Longitud(r) >= 6) Y (Longitud(r) <= 10);
		Si No valido Entonces
			Escribir "[ERROR] La contraseña debe tener entre 6 y 10 caracteres. Ingresó: ", Longitud(r), ".";
		FinSi
	Hasta Que valido
FinFuncion

Funcion r <- PedirTipoDocumento(titulo)
	// Muestra DNI/CE/RUC y devuelve el tipo elegido
	Definir r Como Caracter;
	Definir k Como Entero;
	k <- LeerOpcion(titulo, "DNI|CE|RUC", Falso);
	r <- ObtenerItem("DNI|CE|RUC", k, "|");
FinFuncion

Funcion r <- PedirNumeroDocumento(tipo, etiqueta)
	// Repite hasta que el número cumpla el formato del tipo
	Definir r Como Caracter;
	Definir valido Como Logico;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer r;
		r <- Recortar(r);
		valido <- ValidarDocumento(tipo, r);
		Si No valido Entonces
			Escribir "[ERROR] Formato inválido. DNI: 8 dígitos | RUC: 11 dígitos | CE: 1 letra y 7 dígitos.";
		FinSi
	Hasta Que valido
FinFuncion

Funcion r <- PedirSoloLetras(etiqueta)
	// Para nombres y apellidos: solo letras, espacios, guiones y apóstrofes
	Definir r, c Como Caracter;
	Definir valido Como Logico;
	Definir i Como Entero;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer r;
		r <- Recortar(r);
		valido <- r <> "";
		Para i <- 1 Hasta Longitud(r) Con Paso 1 Hacer
			c <- Trozo(r, i, i);
			Si No (EsLetra(c) O c = " " O c = "-" O c = "'") Entonces
				valido <- Falso;
			FinSi
		FinPara
		Si No valido Entonces
			Escribir "[ERROR] Ingrese un texto válido (solo letras y espacios).";
		FinSi
	Hasta Que valido
FinFuncion

Funcion r <- PedirFolios(etiqueta)
	// Repite hasta que sea un entero mayor a 0
	Definir r Como Entero;
	Definir dato Como Caracter;
	Definir valido Como Logico;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer dato;
		dato <- Recortar(dato);
		valido <- Falso;
		Si SoloDigitos(dato) Entonces
			Si ConvertirANumero(dato) >= 1 Entonces
				valido <- Verdadero;
			FinSi
		FinSi
		Si No valido Entonces
			Escribir "[ERROR] Ingrese un número entero mayor a 0.";
		FinSi
	Hasta Que valido
	r <- trunc(ConvertirANumero(dato));
FinFuncion

Funcion r <- PedirNombreUsuario(etiqueta)
	// No puede estar vacío ni tener espacios
	Definir r Como Caracter;
	Definir valido Como Logico;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer r;
		r <- Recortar(r);
		valido <- (r <> "") Y (No ContieneCaracter(r, " "));
		Si No valido Entonces
			Escribir "[ERROR] El usuario no puede estar vacío ni contener espacios.";
		FinSi
	Hasta Que valido
FinFuncion

Funcion r <- PedirTelefono(etiqueta)
	// 9 dígitos y empieza con 9
	Definir r Como Caracter;
	Definir valido Como Logico;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer r;
		r <- Recortar(r);
		valido <- Falso;
		Si SoloDigitos(r) Y Longitud(r) = 9 Entonces
			Si Trozo(r, 1, 1) = "9" Entonces
				valido <- Verdadero;
			FinSi
		FinSi
		Si No valido Entonces
			Escribir "[ERROR] Teléfono inválido. Debe tener 9 dígitos y empezar con 9.";
		FinSi
	Hasta Que valido
FinFuncion

Funcion r <- PedirCorreo(etiqueta)
	// Debe contener '@' y '.'
	Definir r Como Caracter;
	Definir valido Como Logico;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer r;
		r <- Recortar(r);
		valido <- ContieneCaracter(r, "@") Y ContieneCaracter(r, ".");
		Si No valido Entonces
			Escribir "[ERROR] Formato de correo inválido. Debe incluir @ y un dominio válido (ej. .com).";
		FinSi
	Hasta Que valido
FinFuncion

Funcion r <- PedirAdjuntoPdf(etiqueta)
	// El nombre del archivo debe terminar en .pdf
	Definir r Como Caracter;
	Definir valido Como Logico;
	Repetir
		Escribir etiqueta, ": " Sin Saltar;
		Leer r;
		r <- Recortar(r);
		valido <- (r <> "") Y TerminaEn(Minusculas(r), ".pdf");
		Si No valido Entonces
			Escribir "[ERROR] Formato inválido. El archivo debe terminar obligatoria y únicamente en .pdf";
		FinSi
	Hasta Que valido
FinFuncion

// --- Agregado en el avance 20/10 (servicios/entradas.py) ---
Funcion r <- ValidarDni(dni)
	// Equivale a  re.match(r'^\d{8}$', dni) : exactamente 8 dígitos
	Definir r Como Logico;
	r <- SoloDigitos(dni) Y (Longitud(dni) = 8);
FinFuncion

Funcion r <- ValidarRuc(ruc)
	// Equivale a  re.match(r'^\d{11}$', ruc) : exactamente 11 dígitos
	Definir r Como Logico;
	r <- SoloDigitos(ruc) Y (Longitud(ruc) = 11);
FinFuncion

Funcion r <- ValidarArchivoPdf(nombreArchivo)
	// No puede estar vacío y debe terminar en .pdf
	Definir r Como Logico;
	r <- Falso;
	Si nombreArchivo <> "" Entonces
		r <- TerminaEn(Minusculas(nombreArchivo), ".pdf");
	FinSi
FinFuncion

Funcion n <- ValidarEntradaInstantanea(dni, ruc, tipoPersona, folios, archivoPdf, errores Por Referencia)
	// Validación algorítmica instantánea: DNI, RUC (persona jurídica),
	// folios y extensión .pdf. Guarda los errores en "errores" y
	// devuelve cuántos hay (0 = "aprobado", mayor a 0 = "rechazado").
	// El DNI solo se valida si se envía uno (con CE o RUC llega vacío).
	Definir n Como Entero;
	n <- 0;
	Si dni <> "" Entonces
		Si No ValidarDni(dni) Entonces
			n <- n + 1;
			errores[n] <- "El DNI debe contener exactamente 8 dígitos numéricos.";
		FinSi
	FinSi
	Si tipoPersona = "juridica" Entonces
		Si No ValidarRuc(ruc) Entonces
			n <- n + 1;
			errores[n] <- "El RUC debe contener exactamente 11 dígitos numéricos.";
		FinSi
	FinSi
	Si folios <= 0 Entonces
		n <- n + 1;
		errores[n] <- "El número de folios debe ser mayor a 0.";
	FinSi
	Si No ValidarArchivoPdf(archivoPdf) Entonces
		n <- n + 1;
		errores[n] <- "El documento adjunto debe ser un archivo en formato .pdf válido.";
	FinSi
FinFuncion

// MÓDULO: data/personas.py
Funcion r <- FormatoId(idTexto)
	// Ejemplo: "1" -> "000001"
	Definir r Como Caracter;
	r <- Rellenar(ConvertirANumero(idTexto), 6);
FinFuncion

Funcion r <- CodigoCasilla(idTexto)
	// Ejemplo: "1" -> "CE-000001"
	Definir r Como Caracter;
	r <- Concatenar("CE-", FormatoId(idTexto));
FinFuncion

Funcion r <- ValidarDocumento(tipo, numDoc)
	// DNI: 8 dígitos | RUC: 11 dígitos | CE: 1 letra y 7 dígitos
	Definir r Como Logico;
	Definir t, n Como Caracter;
	t <- Mayusculas(Recortar(tipo));
	n <- Recortar(numDoc);
	r <- Falso;
	Si t = "DNI" Entonces
		r <- SoloDigitos(n) Y (Longitud(n) = 8);
	FinSi
	Si t = "RUC" Entonces
		r <- SoloDigitos(n) Y (Longitud(n) = 11);
	FinSi
	Si t = "CE" Entonces
		Si Longitud(n) = 8 Entonces
			r <- EsLetra(Trozo(n, 1, 1)) Y SoloDigitos(Trozo(n, 2, 8));
		FinSi
	FinSi
FinFuncion

Funcion r <- CorreoValido(correo)
	// Formato básico: algo@dominio.ext
	Definir r Como Logico;
	Definir usuarioC, dominio Como Caracter;
	r <- Falso;
	Si ContarCaracter(correo, "@") = 1 Y No ContieneCaracter(correo, " ") Entonces
		usuarioC <- ObtenerItem(correo, 1, "@");
		dominio <- ObtenerItem(correo, 2, "@");
		Si usuarioC <> "" Y ContieneCaracter(dominio, ".") Entonces
			Si Trozo(dominio, 1, 1) <> "." Y Trozo(dominio, Longitud(dominio), Longitud(dominio)) <> "." Entonces
				r <- Verdadero;
			FinSi
		FinSi
	FinSi
FinFuncion

Funcion pos <- BuscarPersona(per Por Referencia, cnt Por Referencia, idPersona)
	// Busca por ID interno. Devuelve la fila o 0
	Definir pos, i Como Entero;
	pos <- 0;
	Para i <- 1 Hasta cnt[1] Con Paso 1 Hacer
		Si per[i, 1] = idPersona Entonces
			pos <- i;
		FinSi
	FinPara
FinFuncion

Funcion pos <- BuscarPersonaPorDocumento(per Por Referencia, cnt Por Referencia, tipo, numDoc)
	// Busca por tipo y número de documento. Devuelve la fila o 0
	Definir pos, i Como Entero;
	Definir t, n Como Caracter;
	t <- Mayusculas(Recortar(tipo));
	n <- Mayusculas(Recortar(numDoc));
	pos <- 0;
	Para i <- 1 Hasta cnt[1] Con Paso 1 Hacer
		Si per[i, 2] = t Y Mayusculas(per[i, 3]) = n Entonces
			pos <- i;
		FinSi
	FinPara
FinFuncion

Funcion pos <- RegistrarPersona(per Por Referencia, cnt Por Referencia, tipo, numDoc, nombres, apellidos, correo, telefono, mensaje Por Referencia)
	// Valida y registra una persona. Devuelve la fila nueva o 0 si hay error
	Definir pos, i, nuevoId Como Entero;
	Definir t, n, nom, ape, cor, tel Como Caracter;
	t <- Mayusculas(Recortar(tipo));
	n <- Mayusculas(Recortar(numDoc));
	nom <- Recortar(nombres);
	ape <- Recortar(apellidos);
	cor <- Recortar(correo);
	tel <- Recortar(telefono);
	pos <- 0;
	mensaje <- "";
	
	Si No ValidarDocumento(t, n) Entonces
		mensaje <- "Documento inválido. DNI: 8 dígitos; RUC: 11 dígitos; CE: 1 letra y 7 dígitos.";
	FinSi
	Si mensaje = "" Entonces
		Si BuscarPersonaPorDocumento(per, cnt, t, n) > 0 Entonces
			mensaje <- "Ya existe una persona con ese tipo y número de documento.";
		FinSi
	FinSi
	Si mensaje = "" Entonces
		Si nom = "" O ape = "" Entonces
			mensaje <- "Los nombres y apellidos son obligatorios.";
		FinSi
	FinSi
	Si mensaje = "" Entonces
		Si No CorreoValido(cor) Entonces
			mensaje <- "Ingrese un correo válido (ejemplo: nombre@dominio.com).";
		FinSi
	FinSi
	Si mensaje = "" Entonces
		Si tel = "" Entonces
			mensaje <- "El teléfono es obligatorio.";
		FinSi
	FinSi
	
	Si mensaje = "" Entonces
		// El ID se genera solo: el mayor ID existente + 1
		nuevoId <- 0;
		Para i <- 1 Hasta cnt[1] Con Paso 1 Hacer
			Si ConvertirANumero(per[i, 1]) > nuevoId Entonces
				nuevoId <- ConvertirANumero(per[i, 1]);
			FinSi
		FinPara
		nuevoId <- nuevoId + 1;
		cnt[1] <- cnt[1] + 1;
		pos <- cnt[1];
		per[pos, 1] <- NumATexto(nuevoId);
		per[pos, 2] <- t;
		per[pos, 3] <- n;
		per[pos, 4] <- nom;
		per[pos, 5] <- ape;
		per[pos, 6] <- cor;
		per[pos, 7] <- tel;
		per[pos, 8] <- "ACTIVO";
		mensaje <- "Persona registrada correctamente.";
	FinSi
FinFuncion

// MÓDULO: data/usuarios.py
Funcion r <- RolValido(rol)
	Definir r Como Logico;
	r <- rol = "ADMINISTRADOR" O rol = "MESA_PARTES" O rol = "FUNCIONARIO" O rol = "CIUDADANO";
FinFuncion

Funcion pos <- BuscarUsuario(usu Por Referencia, cnt Por Referencia, nombreUsuario)
	// Busca por nombre de usuario sin distinguir mayúsculas. Devuelve la fila o 0
	Definir pos, i Como Entero;
	Definir buscado Como Caracter;
	buscado <- Minusculas(Recortar(nombreUsuario));
	pos <- 0;
	Para i <- 1 Hasta cnt[2] Con Paso 1 Hacer
		Si Minusculas(usu[i, 3]) = buscado Entonces
			pos <- i;
		FinSi
	FinPara
FinFuncion

Funcion pos <- BuscarUsuarioPorPersona(usu Por Referencia, cnt Por Referencia, idPersona)
	// Busca la cuenta vinculada a un ID de persona. Devuelve la fila o 0
	Definir pos, i Como Entero;
	pos <- 0;
	Para i <- 1 Hasta cnt[2] Con Paso 1 Hacer
		Si usu[i, 2] = idPersona Entonces
			pos <- i;
		FinSi
	FinPara
FinFuncion

Funcion pos <- RegistrarUsuario(per Por Referencia, usu Por Referencia, cnt Por Referencia, idPersona, nombreUsuario, contrasena, rol, area, mensaje Por Referencia)
	// Crea una cuenta para una persona ya registrada. Devuelve la fila o 0
	Definir pos, i, nuevoId Como Entero;
	Definir nom, rolU, areaU Como Caracter;
	nom <- Recortar(nombreUsuario);
	rolU <- Mayusculas(Recortar(rol));
	areaU <- Mayusculas(Recortar(area));
	pos <- 0;
	mensaje <- "";
	
	Si BuscarPersona(per, cnt, idPersona) = 0 Entonces
		mensaje <- "La persona no existe. Regístrela primero.";
	FinSi
	Si mensaje = "" Entonces
		Si nom = "" O ContieneCaracter(nom, " ") Entonces
			mensaje <- "El nombre de usuario es obligatorio y no puede tener espacios.";
		FinSi
	FinSi
	Si mensaje = "" Entonces
		Si Longitud(contrasena) < 6 Entonces
			mensaje <- "La contraseña debe tener al menos 6 caracteres.";
		FinSi
	FinSi
	Si mensaje = "" Entonces
		Si No RolValido(rolU) Entonces
			mensaje <- "Rol no válido. Roles: ADMINISTRADOR, MESA_PARTES, FUNCIONARIO, CIUDADANO.";
		FinSi
	FinSi
	Si mensaje = "" Entonces
		Si rolU = "FUNCIONARIO" Y No AreaValida(areaU) Entonces
			mensaje <- Concatenar(Concatenar("El FUNCIONARIO necesita un área válida: ", ListaAreas(", ")), ".");
		FinSi
	FinSi
	Si rolU <> "FUNCIONARIO" Entonces
		areaU <- "";
	FinSi
	Si mensaje = "" Entonces
		Si BuscarUsuario(usu, cnt, nom) > 0 Entonces
			mensaje <- "Ese nombre de usuario ya está registrado.";
		FinSi
	FinSi
	Si mensaje = "" Entonces
		Si BuscarUsuarioPorPersona(usu, cnt, idPersona) > 0 Entonces
			mensaje <- "Esta persona ya tiene una cuenta de usuario.";
		FinSi
	FinSi
	
	Si mensaje = "" Entonces
		nuevoId <- 0;
		Para i <- 1 Hasta cnt[2] Con Paso 1 Hacer
			Si ConvertirANumero(usu[i, 1]) > nuevoId Entonces
				nuevoId <- ConvertirANumero(usu[i, 1]);
			FinSi
		FinPara
		nuevoId <- nuevoId + 1;
		cnt[2] <- cnt[2] + 1;
		pos <- cnt[2];
		usu[pos, 1] <- NumATexto(nuevoId);
		usu[pos, 2] <- idPersona;
		usu[pos, 3] <- nom;
		usu[pos, 4] <- contrasena;
		usu[pos, 5] <- rolU;
		usu[pos, 6] <- areaU;
		usu[pos, 7] <- "ACTIVO";
		mensaje <- "Usuario creado correctamente.";
	FinSi
FinFuncion

Funcion pos <- ValidarCredenciales(usu Por Referencia, cnt Por Referencia, nombreUsuario, contrasena)
	// Devuelve la fila si usuario y contraseña son correctos y la cuenta está ACTIVA
	Definir pos, i Como Entero;
	pos <- 0;
	i <- BuscarUsuario(usu, cnt, nombreUsuario);
	Si i > 0 Entonces
		Si usu[i, 7] = "ACTIVO" Y usu[i, 4] = contrasena Entonces
			pos <- i;
		FinSi
	FinSi
FinFuncion

// MÓDULO: data/areas.py y data/tramites.py
Funcion r <- ListaAreas(sep)
	Definir r Como Caracter;
	r <- Concatenar(Concatenar(Concatenar("RECURSOS HUMANOS", sep), Concatenar("ABASTECIMIENTO", sep)), Concatenar(Concatenar(Concatenar("SERVICIOS AL USUARIO", sep), Concatenar("PRESUPUESTO PUBLICO", sep)), "FINANZAS"));
FinFuncion

Funcion r <- AreaValida(area)
	Definir r Como Logico;
	Definir i Como Entero;
	r <- Falso;
	Para i <- 1 Hasta 5 Con Paso 1 Hacer
		Si ObtenerItem(ListaAreas("|"), i, "|") = Mayusculas(Recortar(area)) Entonces
			r <- Verdadero;
		FinSi
	FinPara
FinFuncion

Funcion r <- DeterminarAreaPorTramite(tramite)
	// Equivale al diccionario AREAS_POR_TRAMITE
	Definir r Como Caracter;
	r <- "RECURSOS HUMANOS";
	Si tramite = "SOLICITUD DE ORDEN DE SERVICIOS" Entonces
		r <- "ABASTECIMIENTO";
	FinSi
FinFuncion

Funcion r <- ListaTramites(sep)
	// Los 5 trámites (claves 1 a 5), separados por "sep"
	Definir r Como Caracter;
	r <- Concatenar(Concatenar(Concatenar("LICENCIA", sep), Concatenar("DESCANSO MEDICO", sep)), Concatenar(Concatenar("CONSTANCIA DE TRABAJO", sep), Concatenar(Concatenar("SOLICITUD DE ORDEN DE SERVICIOS", sep), "REPROGRAMACION DE VACACIONES")));
FinFuncion

Funcion r <- TramitePideCampos(clave)
	// Los trámites 3 y 4 piden CAMPOS_CONSTANCIA (área donde laboró, N° de orden y firma)
	Definir r Como Logico;
	r <- clave = 3 O clave = 4;
FinFuncion

// MÓDULO: autenticacion/autenticacion.py
SubProceso LimpiarSesion(ses Por Referencia)
	Definir i Como Entero;
	Para i <- 1 Hasta 6 Con Paso 1 Hacer
		ses[i] <- "";
	FinPara
FinSubProceso

Funcion ok <- IniciarSesion(per Por Referencia, usu Por Referencia, cnt Por Referencia, nombreUsuario, contrasena, ses Por Referencia, mensaje Por Referencia)
	// login(): valida usuario y contraseña y llena la sesión
	Definir ok Como Logico;
	Definir iu, ip Como Entero;
	ok <- Falso;
	iu <- ValidarCredenciales(usu, cnt, nombreUsuario, contrasena);
	Si iu = 0 Entonces
		mensaje <- "Acceso denegado: usuario, contraseña o estado incorrecto.";
	SiNo
		ip <- BuscarPersona(per, cnt, usu[iu, 2]);
		Si ip = 0 Entonces
			mensaje <- "Acceso denegado: la persona no existe o está inactiva.";
		SiNo
			Si per[ip, 8] <> "ACTIVO" Entonces
				mensaje <- "Acceso denegado: la persona no existe o está inactiva.";
			SiNo
				ses[1] <- usu[iu, 1];
				ses[2] <- usu[iu, 3];
				ses[3] <- usu[iu, 5];
				ses[4] <- per[ip, 1];
				ses[5] <- usu[iu, 6];
				ses[6] <- Concatenar(Concatenar(per[ip, 4], " "), per[ip, 5]);
				ok <- Verdadero;
				mensaje <- "Inicio de sesión correcto.";
			FinSi
		FinSi
	FinSi
FinFuncion

SubProceso CerrarSesion(ses Por Referencia, mensaje Por Referencia)
	// logout()
	Si ses[1] = "" Entonces
		mensaje <- "No hay una sesión activa.";
	SiNo
		mensaje <- Concatenar(Concatenar("Sesión cerrada para ", ses[2]), ".");
		LimpiarSesion(ses);
	FinSi
FinSubProceso

// MÓDULO: autenticacion/registro.py
Funcion pos <- PedirDatosPersona(per Por Referencia, cnt Por Referencia, tipo, numDoc)
	// Pide los datos y registra una persona. Si tipo y numDoc vienen
	// vacíos se piden; si ya se conocen (recepción física) no se repiten.
	Definir pos Como Entero;
	Definir t, n, nombres, apellidos, correo, telefono, mensaje Como Caracter;
	Si tipo = "" O numDoc = "" Entonces
		t <- PedirTipoDocumento("Tipo de documento de identidad:");
		n <- PedirNumeroDocumento(t, "Número de documento");
	SiNo
		t <- tipo;
		n <- numDoc;
		Escribir "Documento: ", t, " ", n;
	FinSi
	nombres <- PedirSoloLetras("Nombres");
	apellidos <- PedirSoloLetras("Apellidos");
	correo <- PedirCorreo("Correo electrónico");
	telefono <- PedirTelefono("Teléfono");
	mensaje <- "";
	pos <- RegistrarPersona(per, cnt, t, n, nombres, apellidos, correo, telefono, mensaje);
	Escribir mensaje;
	Si pos > 0 Entonces
		Escribir "ID_PERSONA: ", FormatoId(per[pos, 1]);
	FinSi
FinFuncion

Funcion r <- PedirUsuarioDisponible(usu Por Referencia, cnt Por Referencia)
	// Pide el nombre de usuario y lo repite mientras ya esté en uso
	Definir r Como Caracter;
	Definir disponible Como Logico;
	Repetir
		r <- PedirNombreUsuario("Nombre de usuario");
		disponible <- BuscarUsuario(usu, cnt, r) = 0;
		Si No disponible Entonces
			Escribir "[ERROR] Ese nombre de usuario ya está en uso. Ingrese otro usuario.";
		FinSi
	Hasta Que disponible
FinFuncion

Funcion pos <- CrearUsuarioPara(per Por Referencia, usu Por Referencia, cnt Por Referencia, iPer, rolFijo)
	// Pide usuario, contraseña y rol, y crea la cuenta de la persona
	Definir pos Como Entero;
	Definir nombreUsuario, contrasena, rol, area, mensaje Como Caracter;
	nombreUsuario <- PedirUsuarioDisponible(usu, cnt);
	contrasena <- PedirContrasenaRegistro("Contraseña (entre 6 y 10 caracteres)", nombreUsuario);
	area <- "";
	Si rolFijo <> "" Entonces
		rol <- rolFijo;
	SiNo
		Escribir "Roles disponibles: ADMINISTRADOR, MESA_PARTES, FUNCIONARIO, CIUDADANO";
		Escribir "Rol: " Sin Saltar;
		Leer rol;
		rol <- Mayusculas(Recortar(rol));
		Si rol = "FUNCIONARIO" Entonces
			Escribir "Áreas disponibles: ", ListaAreas(", ");
			Escribir "Área del funcionario: " Sin Saltar;
			Leer area;
		FinSi
	FinSi
	mensaje <- "";
	pos <- RegistrarUsuario(per, usu, cnt, per[iPer, 1], nombreUsuario, contrasena, rol, area, mensaje);
	Escribir mensaje;
	Si pos > 0 Entonces
		Escribir "ID_USUARIO: ", FormatoId(usu[pos, 1]);
	FinSi
FinFuncion

SubProceso RegistroCiudadano(per Por Referencia, usu Por Referencia, cnt Por Referencia)
	// Auto-registro: crea la persona y su cuenta con rol CIUDADANO
	Definir iPer, iUsu Como Entero;
	Escribir "";
	Escribir "--- REGISTRO DE CIUDADANO ---";
	iPer <- PedirDatosPersona(per, cnt, "", "");
	Si iPer > 0 Entonces
		iUsu <- CrearUsuarioPara(per, usu, cnt, iPer, "CIUDADANO");
		Si iUsu = 0 Entonces
			Escribir "[ERROR] No se pudo crear la cuenta. Intente registrarse nuevamente.";
		FinSi
	FinSi
FinSubProceso


// ============================================================
// MÓDULO: servicios/busqueda.py
// ============================================================
Funcion pos <- BuscarLineal(mat Por Referencia, n, columna, buscado)
	// Recorre las filas una por una. Devuelve la fila donde
	// mat[fila, columna] = buscado, o 0 si no está.
	Definir pos, i Como Entero;
	pos <- 0;
	i <- 1;
	Mientras i <= n Y pos = 0 Hacer
		Si mat[i, columna] = buscado Entonces
			pos <- i;
		FinSi
		i <- i + 1;
	FinMientras
FinFuncion

Funcion pos <- BuscarBinaria(arreglo Por Referencia, n, objetivo)
	// Búsqueda binaria sobre un arreglo de textos YA ORDENADO de menor a mayor.
	// Cada vuelta descarta la mitad del arreglo. Devuelve la posición o 0.
	Definir pos, ini, ult, medio Como Entero;
	ini <- 1;
	ult <- n;
	pos <- 0;
	Mientras ini <= ult Y pos = 0 Hacer
		medio <- trunc((ini + ult) / 2);
		Si arreglo[medio] = objetivo Entonces
			pos <- medio;
		SiNo
			Si arreglo[medio] < objetivo Entonces
				ini <- medio + 1;
			SiNo
				ult <- medio - 1;
			FinSi
		FinSi
	FinMientras
FinFuncion

// --- Agregado en el avance 20/10 (servicios/busqueda.py) ---
Funcion n <- BuscarExpedienteAvanzado(ex Por Referencia, cnt Por Referencia, criterio, resultados Por Referencia)
	// Búsqueda por código, DNI o nombre del ciudadano (sin distinguir
	// mayúsculas y aceptando coincidencias parciales). Guarda en
	// "resultados" las filas encontradas y devuelve cuántas son.
	// Si el criterio está vacío devuelve todos los expedientes.
	// Claves "codigo", "numero_identificacion" y "administrado" de Python
	// = columnas 1, 4 y 5 de la matriz ex.
	Definir n, i Como Entero;
	Definir c Como Caracter;
	c <- Minusculas(criterio);
	n <- 0;
	Para i <- 1 Hasta cnt[3] Con Paso 1 Hacer
		Si c = "" Entonces
			n <- n + 1;
			resultados[n] <- i;
		SiNo
			Si ContieneTexto(Minusculas(ex[i, 1]), c) O ContieneTexto(Minusculas(ex[i, 4]), c) O ContieneTexto(Minusculas(ex[i, 5]), c) Entonces
				n <- n + 1;
				resultados[n] <- i;
			FinSi
		FinSi
	FinPara
FinFuncion

// MÓDULO: servicios/ordenamiento.py
SubProceso OrdenarBurbujaMatriz(mat Por Referencia, n, columna, ncols, descendente)
	// Burbuja: compara filas vecinas y las intercambia si están desordenadas
	Definir pasada, i, j Como Entero;
	Definir a, b, aux Como Caracter;
	Definir fueraDeOrden Como Logico;
	Para pasada <- 1 Hasta n - 1 Con Paso 1 Hacer
		Para i <- 1 Hasta n - pasada Con Paso 1 Hacer
			a <- mat[i, columna];
			b <- mat[i + 1, columna];
			Si descendente Entonces
				fueraDeOrden <- a < b;
			SiNo
				fueraDeOrden <- a > b;
			FinSi
			Si fueraDeOrden Entonces
				Para j <- 1 Hasta ncols Con Paso 1 Hacer
					aux <- mat[i, j];
					mat[i, j] <- mat[i + 1, j];
					mat[i + 1, j] <- aux;
				FinPara
			FinSi
		FinPara
	FinPara
FinSubProceso

SubProceso OrdenarInsercionParalelos(claves Por Referencia, p1 Por Referencia, p2 Por Referencia, p3 Por Referencia, p4 Por Referencia, n, descendente)
	// Ordena "claves" por inserción y mueve igual los 4 arreglos paralelos
	// (la posición i de cada arreglo describe el MISMO expediente)
	Definir i, j Como Entero;
	Definir clave, x1, x2, x3, x4 Como Caracter;
	Definir seguir, mover Como Logico;
	Para i <- 2 Hasta n Con Paso 1 Hacer
		clave <- claves[i];
		x1 <- p1[i];
		x2 <- p2[i];
		x3 <- p3[i];
		x4 <- p4[i];
		j <- i - 1;
		seguir <- Verdadero;
		Mientras seguir Hacer
			Si j < 1 Entonces
				seguir <- Falso;
			SiNo
				Si descendente Entonces
					mover <- claves[j] < clave;
				SiNo
					mover <- claves[j] > clave;
				FinSi
				Si mover Entonces
					claves[j + 1] <- claves[j];
					p1[j + 1] <- p1[j];
					p2[j + 1] <- p2[j];
					p3[j + 1] <- p3[j];
					p4[j + 1] <- p4[j];
					j <- j - 1;
				SiNo
					seguir <- Falso;
				FinSi
			FinSi
		FinMientras
		claves[j + 1] <- clave;
		p1[j + 1] <- x1;
		p2[j + 1] <- x2;
		p3[j + 1] <- x3;
		p4[j + 1] <- x4;
	FinPara
FinSubProceso

Funcion r <- FechaAClave(fecha)
	// 'dd/mm/aaaa hh:mm' -> 'aaaammddhhmm' para poder ordenar fechas como texto
	Definir r Como Caracter;
	r <- Concatenar(Concatenar(Trozo(fecha, 7, 10), Trozo(fecha, 4, 5)), Concatenar(Concatenar(Trozo(fecha, 1, 2), Trozo(fecha, 12, 13)), Trozo(fecha, 15, 16)));
FinFuncion

// --- Agregado en el avance 20/10 (servicios/ordenamiento.py) ---
Funcion n <- OrdenarExpedientes(ex Por Referencia, cnt Por Referencia, criterioOrden, indices Por Referencia)
	// Guarda en "indices" las filas de ex en el orden pedido y devuelve cuántas son:
	//   "fecha_reciente": por fecha, la más reciente primero
	//   "fecha_antigua" : por fecha, la más antigua primero
	//   "codigo"        : por código de expediente (alfabético)
	//   otro criterio   : en el orden en que se registraron
	// Usa inserción (estable, igual que sorted() de Python).
	// La fecha se compara con FechaAClave(fecha_registro), columna 19,
	// igual que fecha_a_clave(x["fecha_registro"]) en Python.
	Definir n, i, j, idx Como Entero;
	Definir claves Como Caracter;
	Definir clave Como Caracter;
	Definir descendente, ordenar, seguir, mover Como Logico;
	Dimension claves[201];
	n <- cnt[3];
	ordenar <- Verdadero;
	descendente <- Falso;
	Para i <- 1 Hasta n Con Paso 1 Hacer
		indices[i] <- i;
		Si criterioOrden = "codigo" Entonces
			claves[i] <- ex[i, 1];
		SiNo
			claves[i] <- FechaAClave(ex[i, 19]);
		FinSi
	FinPara
	Si criterioOrden = "fecha_reciente" Entonces
		descendente <- Verdadero;
	SiNo
		Si criterioOrden <> "fecha_antigua" Y criterioOrden <> "codigo" Entonces
			ordenar <- Falso;
		FinSi
	FinSi
	Si ordenar Entonces
		Para i <- 2 Hasta n Con Paso 1 Hacer
			clave <- claves[i];
			idx <- indices[i];
			j <- i - 1;
			seguir <- Verdadero;
			Mientras seguir Hacer
				Si j < 1 Entonces
					seguir <- Falso;
				SiNo
					Si descendente Entonces
						mover <- claves[j] < clave;
					SiNo
						mover <- claves[j] > clave;
					FinSi
					Si mover Entonces
						claves[j + 1] <- claves[j];
						indices[j + 1] <- indices[j];
						j <- j - 1;
					SiNo
						seguir <- Falso;
					FinSi
				FinSi
			FinMientras
			claves[j + 1] <- clave;
			indices[j + 1] <- idx;
		FinPara
	FinSi
FinFuncion

// MÓDULO: data/expedientes.py
Funcion pos <- BuscarExpediente(ex Por Referencia, cnt Por Referencia, codigo)
	// Búsqueda LINEAL por código. Devuelve la fila o 0
	Definir pos Como Entero;
	pos <- BuscarLineal(ex, cnt[3], 1, Mayusculas(Recortar(codigo)));
FinFuncion

Funcion pos <- CrearExpediente(ex Por Referencia, cnt Por Referencia, per Por Referencia, iPer, canal, casilla, tramite, subtipo, asunto, folios, datos Por Referencia, adjunto, usuario)
	// Asigna el código EXP-AAAA-NNNNNN y completa los campos base
	Definir pos Como Entero;
	cnt[3] <- cnt[3] + 1;
	pos <- cnt[3];
	// Nunca se borran expedientes, así el correlativo no se repite
	ex[pos, 1] <- Concatenar(Concatenar("EXP-", NumATexto(trunc(FechaActual() / 10000))), Concatenar("-", Rellenar(pos, 6)));
	ex[pos, 2] <- per[iPer, 1];
	ex[pos, 3] <- per[iPer, 2];
	ex[pos, 4] <- per[iPer, 3];
	ex[pos, 5] <- Concatenar(Concatenar(per[iPer, 4], " "), per[iPer, 5]);
	ex[pos, 6] <- canal;
	ex[pos, 7] <- casilla;
	ex[pos, 8] <- tramite;
	ex[pos, 9] <- subtipo;
	ex[pos, 10] <- DeterminarAreaPorTramite(tramite);
	ex[pos, 11] <- Recortar(asunto);
	ex[pos, 12] <- NumATexto(folios);
	ex[pos, 13] <- datos[1];
	ex[pos, 14] <- datos[2];
	ex[pos, 15] <- datos[3];
	ex[pos, 16] <- adjunto;
	ex[pos, 17] <- usuario;
	ex[pos, 18] <- "RECIBIDO";
	ex[pos, 19] <- FormatoFechaHora(FechaActual(), HoraActual());
	ex[pos, 20] <- "";
	ex[pos, 21] <- "NO";
	ex[pos, 22] <- "";
FinFuncion

// MÓDULO: servicios/historial.py
SubProceso RegistrarHistorial(his Por Referencia, cnt Por Referencia, codigoExp, accion, detalle, usuario)
	// Agrega un movimiento al historial del expediente
	Definir i Como Entero;
	cnt[4] <- cnt[4] + 1;
	i <- cnt[4];
	his[i, 1] <- codigoExp;
	his[i, 2] <- FormatoFechaHora(FechaActual(), HoraActual());
	his[i, 3] <- accion;
	his[i, 4] <- detalle;
	his[i, 5] <- usuario;
FinSubProceso

SubProceso VerHistorial(his Por Referencia, cnt Por Referencia, codigoExp)
	// Muestra todos los movimientos de un expediente
	Definir i, total Como Entero;
	Escribir "";
	Escribir "HISTORIAL - ", codigoExp;
	Escribir LineaDe("-", 48);
	total <- 0;
	Para i <- 1 Hasta cnt[4] Con Paso 1 Hacer
		Si his[i, 1] = codigoExp Entonces
			total <- total + 1;
			Escribir his[i, 2];
			Si his[i, 4] <> "" Entonces
				Escribir "  ", his[i, 3], " | ", his[i, 4];
			SiNo
				Escribir "  ", his[i, 3];
			FinSi
			Si his[i, 5] <> "" Entonces
				Escribir "  Usuario: ", his[i, 5];
			FinSi
		FinSi
	FinPara
	Si total = 0 Entonces
		Escribir "  Sin movimientos registrados.";
	FinSi
	Escribir LineaDe("-", 48);
FinSubProceso

// MÓDULO: servicios/notificaciones.py
SubProceso EnviarNotificacion(noti Por Referencia, cnt Por Referencia, idPersona, mensaje, codigoExp, tipo)
	// Guarda una notificación nueva (sin leer) y simula el envío
	Definir i Como Entero;
	cnt[5] <- cnt[5] + 1;
	i <- cnt[5];
	noti[i, 1] <- NumATexto(i);
	noti[i, 2] <- idPersona;
	noti[i, 3] <- codigoExp;
	noti[i, 4] <- tipo;
	noti[i, 5] <- mensaje;
	noti[i, 6] <- FormatoFechaHora(FechaActual(), HoraActual());
	noti[i, 7] <- "NO";
	Escribir "  [OK] NOTIFICACIÓN ENVIADA a la casilla ", CodigoCasilla(idPersona), " (N.º ", noti[i, 1], ", ", tipo, ")";
FinSubProceso

SubProceso NotificarRegistro(ex Por Referencia, noti Por Referencia, cnt Por Referencia, iExp)
	EnviarNotificacion(noti, cnt, ex[iExp, 2], Concatenar(Concatenar(Concatenar("Su solicitud de ", ex[iExp, 8]), " fue recibida. Se generó el expediente "), Concatenar(ex[iExp, 1], ".")), ex[iExp, 1], "REGISTRO");
FinSubProceso

SubProceso NotificarDerivacion(ex Por Referencia, noti Por Referencia, cnt Por Referencia, iExp)
	EnviarNotificacion(noti, cnt, ex[iExp, 2], Concatenar(Concatenar(Concatenar("Su expediente ", ex[iExp, 1]), " fue derivado a "), Concatenar(ex[iExp, 10], ".")), ex[iExp, 1], "DERIVACION");
FinSubProceso

SubProceso NotificarAnulacion(ex Por Referencia, noti Por Referencia, cnt Por Referencia, iExp)
	EnviarNotificacion(noti, cnt, ex[iExp, 2], Concatenar(Concatenar(Concatenar("Su expediente ", ex[iExp, 1]), " fue ANULADO. Motivo: "), Concatenar(ex[iExp, 20], ".")), ex[iExp, 1], "ANULACION");
FinSubProceso

Funcion r <- ContarNoLeidas(noti Por Referencia, cnt Por Referencia, idPersona)
	Definir r, i Como Entero;
	r <- 0;
	Para i <- 1 Hasta cnt[5] Con Paso 1 Hacer
		Si noti[i, 2] = idPersona Y noti[i, 7] = "NO" Entonces
			r <- r + 1;
		FinSi
	FinPara
FinFuncion

Funcion ok <- MarcarLeida(noti Por Referencia, cnt Por Referencia, idNotificacion, idPersona)
	// Marca como leída una notificación de esa persona. Verdadero si la encontró
	Definir ok Como Logico;
	Definir i Como Entero;
	ok <- Falso;
	Para i <- 1 Hasta cnt[5] Con Paso 1 Hacer
		Si noti[i, 1] = idNotificacion Y noti[i, 2] = idPersona Entonces
			noti[i, 7] <- "SI";
			ok <- Verdadero;
		FinSi
	FinPara
FinFuncion

SubProceso ListarTodasNotificaciones(noti Por Referencia, cnt Por Referencia)
	// Opción 6 de Mesa de Partes: todas las notificaciones del sistema
	Definir i Como Entero;
	Definir estado Como Caracter;
	Si cnt[5] = 0 Entonces
		Escribir "No hay notificaciones en el sistema.";
	FinSi
	Para i <- 1 Hasta cnt[5] Con Paso 1 Hacer
		Si noti[i, 7] = "SI" Entonces
			estado <- "LEÍDA";
		SiNo
			estado <- "NUEVA";
		FinSi
		Escribir "[", estado, "] ", noti[i, 6], " | ", noti[i, 4], " | ", noti[i, 3], " (persona ", noti[i, 2], ")";
		Escribir "   ", noti[i, 5];
	FinPara
FinSubProceso

// MÓDULO: ciudadano/casilla.py
SubProceso VerCasilla(per Por Referencia, noti Por Referencia, cnt Por Referencia, idPersona)
	// Encabezado de la casilla con las notificaciones nuevas
	Definir ip Como Entero;
	ip <- BuscarPersona(per, cnt, idPersona);
	Si ip = 0 Entonces
		Escribir "No se encontró la persona asociada a la casilla.";
	SiNo
		Escribir "";
		Escribir LineaDe("=", 34);
		Escribir "       CASILLA ELECTRÓNICA";
		Escribir LineaDe("=", 34);
		Escribir "Ciudadano: ", per[ip, 4], " ", per[ip, 5];
		Escribir "Casilla  : ", CodigoCasilla(idPersona);
		Escribir "Notificaciones nuevas: ", ContarNoLeidas(noti, cnt, idPersona);
	FinSi
FinSubProceso

Funcion total <- ListarMensajes(noti Por Referencia, cnt Por Referencia, idPersona)
	// Muestra las notificaciones de la casilla. Devuelve la cantidad
	Definir total, i Como Entero;
	Definir marca Como Caracter;
	total <- 0;
	Para i <- 1 Hasta cnt[5] Con Paso 1 Hacer
		Si noti[i, 2] = idPersona Entonces
			total <- total + 1;
			Si noti[i, 7] = "SI" Entonces
				marca <- "[LEÍDA]";
			SiNo
				marca <- "[NUEVA]";
			FinSi
			Escribir "[", noti[i, 1], "] ", noti[i, 6], " | ", marca, " | ", noti[i, 4];
			Escribir "     ", noti[i, 5];
		FinSi
	FinPara
	Si total = 0 Entonces
		Escribir "No tiene mensajes en su casilla.";
	FinSi
FinFuncion

SubProceso MenuMensajes(noti Por Referencia, cnt Por Referencia, idPersona)
	// Lista las notificaciones y permite marcar una como leída
	Definir numeroNoti Como Entero;
	Si ListarMensajes(noti, cnt, idPersona) > 0 Entonces
		numeroNoti <- LeerEntero("Número de notificación para marcarla como leída (0 para volver)");
		Si numeroNoti <> 0 Entonces
			Si MarcarLeida(noti, cnt, NumATexto(numeroNoti), idPersona) Entonces
				Escribir "Notificación marcada como leída.";
			SiNo
				Escribir "No se encontró esa notificación en su casilla.";
			FinSi
		FinSi
	FinSi
FinSubProceso

// MÓDULO: mesa_partes/utilidades.py
Funcion clave <- SeleccionarTramite(tramite Por Referencia, subtipo Por Referencia)
	// Devuelve la clave del trámite (1 a 5) o 0 si cancela
	Definir clave, sub Como Entero;
	tramite <- "";
	subtipo <- "";
	clave <- LeerOpcion("Tipo de trámite:", ListaTramites("|"), Verdadero);
	Si clave > 0 Entonces
		tramite <- ObtenerItem(ListaTramites("|"), clave, "|");
		Si clave = 1 Entonces
			// Solo LICENCIA tiene subtipos
			sub <- LeerOpcion("Tipo de licencia:", "CON GOCE|SIN GOCE", Verdadero);
			Si sub = 0 Entonces
				clave <- 0;
				tramite <- "";
			SiNo
				subtipo <- ObtenerItem("CON GOCE|SIN GOCE", sub, "|");
			FinSi
		FinSi
	FinSi
FinFuncion

Funcion r <- ValidarNOrden(nOrden)
	// Formato correcto: 0002999-2026-ENTIDAD (7 dígitos - 4 dígitos - siglas en mayúscula)
	Definir r Como Logico;
	Definir s, numeroO, anio, siglas Como Caracter;
	s <- Recortar(nOrden);
	r <- Falso;
	Si ContarItems(s, "-") = 3 Entonces
		numeroO <- ObtenerItem(s, 1, "-");
		anio <- ObtenerItem(s, 2, "-");
		siglas <- ObtenerItem(s, 3, "-");
		r <- SoloDigitos(numeroO) Y (Longitud(numeroO) = 7) Y SoloDigitos(anio) Y (Longitud(anio) = 4) Y SoloLetrasMayusculas(siglas);
	FinSi
FinFuncion

Funcion r <- PedirNOrden(etiqueta)
	// Repite hasta que el N° de orden tenga el formato correcto
	Definir r Como Caracter;
	Definir valido Como Logico;
	Repetir
		r <- Mayusculas(LeerTexto(etiqueta));
		valido <- ValidarNOrden(r);
		Si No valido Entonces
			Escribir "[ERROR] Formato incorrecto. Debe ser 7 dígitos-año-siglas (ejemplo: 0002999-2026-ENTIDAD).";
		FinSi
	Hasta Que valido
FinFuncion

SubProceso PedirDatosAdicionales(clave, datos Por Referencia)
	// datos[1] = area_laboro, datos[2] = n_orden, datos[3] = firma
	Definir eleccion Como Entero;
	datos[1] <- "";
	datos[2] <- "";
	datos[3] <- "";
	Si TramitePideCampos(clave) Entonces
		datos[1] <- Mayusculas(LeerTexto("Área/Dirección donde laboró"));
		datos[2] <- PedirNOrden("N° Orden de Servicio/Contrato (ej. 0002999-2026-ENTIDAD)");
		eleccion <- LeerOpcion("Tipo de firma:", "MANUSCRITA|DIGITAL", Falso);
		Si eleccion = 1 Entonces
			datos[3] <- "MANUSCRITA";
		SiNo
			datos[3] <- "DIGITAL";
		FinSi
	FinSi
FinSubProceso

// MÓDULO: mesa_partes/documentos.py  (núcleo de Mesa de Partes)
Funcion n <- ValidarDocumentoTramite(per Por Referencia, iPer, canal, clave, tramite, subtipo, asunto, folios, datos Por Referencia, adjunto, errores Por Referencia)
	// Revisa todos los datos del trámite. Guarda los errores en el
	// arreglo "errores" y devuelve cuántos hay (0 = todo correcto).
	Definir n Como Entero;
	n <- 0;
	Si iPer = 0 Entonces
		n <- 1;
		errores[1] <- "La persona no está registrada en la data maestra.";
	SiNo
		Si per[iPer, 8] <> "ACTIVO" Entonces
			n <- n + 1;
			errores[n] <- "La persona se encuentra INACTIVA.";
		FinSi
		Si canal <> "FISICO" Y canal <> "VIRTUAL" Entonces
			n <- n + 1;
			errores[n] <- "Canal de recepción no válido.";
		FinSi
		Si clave < 1 O clave > 5 Entonces
			n <- n + 1;
			errores[n] <- "Trámite no válido.";
		FinSi
		Si tramite = "LICENCIA" Y subtipo <> "CON GOCE" Y subtipo <> "SIN GOCE" Entonces
			n <- n + 1;
			errores[n] <- "La licencia requiere subtipo CON GOCE o SIN GOCE.";
		FinSi
		Si Recortar(asunto) = "" Entonces
			n <- n + 1;
			errores[n] <- "El asunto es obligatorio.";
		FinSi
		Si folios < 1 Entonces
			n <- n + 1;
			errores[n] <- "El número de folios debe ser un entero mayor a 0.";
		FinSi
		Si TramitePideCampos(clave) Entonces
			Si datos[1] = "" Entonces
				n <- n + 1;
				errores[n] <- "Falta el dato: Área/Dirección donde laboró.";
			FinSi
			Si datos[2] = "" Entonces
				n <- n + 1;
				errores[n] <- "Falta el dato: N° Orden de Servicio/Contrato.";
			FinSi
			Si datos[3] = "" Entonces
				n <- n + 1;
				errores[n] <- "Falta el dato: Firma.";
			FinSi
		FinSi
		Si datos[2] <> "" Entonces
			Si No ValidarNOrden(datos[2]) Entonces
				n <- n + 1;
				errores[n] <- "El N° de orden/contrato no tiene el formato 0000000-AAAA-SIGLAS.";
			FinSi
		FinSi
		Si datos[3] <> "" Y datos[3] <> "MANUSCRITA" Y datos[3] <> "DIGITAL" Entonces
			n <- n + 1;
			errores[n] <- "La firma debe ser MANUSCRITA o DIGITAL.";
		FinSi
		Si canal = "VIRTUAL" Entonces
			Si No TerminaEn(Minusculas(adjunto), ".pdf") Entonces
				n <- n + 1;
				errores[n] <- "El documento adjunto debe ser un archivo .pdf.";
			FinSi
		FinSi
	FinSi
FinFuncion

Funcion pos <- RegistrarDocumento(per Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia, iPer, canal, clave, tramite, subtipo, asunto, folios, datos Por Referencia, usuario, casilla, adjunto, errores Por Referencia, nErrores Por Referencia)
	// Valida, crea el expediente, anota el historial y notifica.
	// Devuelve la fila del expediente, o 0 si hubo errores.
	Definir pos Como Entero;
	pos <- 0;
	nErrores <- ValidarDocumentoTramite(per, iPer, canal, clave, tramite, subtipo, asunto, folios, datos, adjunto, errores);
	Si nErrores = 0 Entonces
		pos <- CrearExpediente(ex, cnt, per, iPer, canal, casilla, tramite, subtipo, asunto, folios, datos, adjunto, usuario);
		AsignarConstancia(ex, pos);
		RegistrarHistorial(his, cnt, ex[pos, 1], "REGISTRO", Concatenar(Concatenar("Documento registrado. Canal: ", canal), "."), usuario);
		NotificarRegistro(ex, noti, cnt, pos);
	FinSi
FinFuncion

SubProceso AsignarConstancia(ex Por Referencia, iExp)
	// EXP-2026-000001 -> CONST-2026-000001
	ex[iExp, 22] <- Concatenar("CONST-", Trozo(ex[iExp, 1], 5, Longitud(ex[iExp, 1])));
FinSubProceso

Funcion pos <- ConsultarDocumento(ex Por Referencia, cnt Por Referencia, codigo)
	// Muestra el detalle de un expediente. Devuelve la fila o 0
	Definir pos Como Entero;
	Definir subt, adj Como Caracter;
	pos <- BuscarExpediente(ex, cnt, codigo);
	Si pos = 0 Entonces
		Escribir "[ERROR] Expediente no encontrado.";
	SiNo
		subt <- ex[pos, 9];
		Si subt = "" Entonces
			subt <- "N/A";
		FinSi
		adj <- ex[pos, 16];
		Si adj = "" Entonces
			adj <- "NINGUNO";
		FinSi
		Escribir "";
		Escribir LineaDe("=", 20), " DETALLE DEL EXPEDIENTE ", LineaDe("=", 20);
		Escribir "Código    : ", ex[pos, 1], " | Canal: ", ex[pos, 6], " | Estado: ", ex[pos, 18];
		Escribir "Solicitante: ", ex[pos, 5], " (", ex[pos, 3], " ", ex[pos, 4], ")";
		Escribir "Trámite   : ", ex[pos, 8], " (", subt, ")";
		Escribir "Área      : ", ex[pos, 10];
		Escribir "Asunto    : ", ex[pos, 11];
		Escribir "Folios    : ", ex[pos, 12], " | Adjunto: ", adj;
		Si ex[pos, 13] <> "" Entonces
			Escribir PadDer("area_laboro", 10), ": ", ex[pos, 13];
			Escribir PadDer("n_orden", 10), ": ", ex[pos, 14];
			Escribir PadDer("firma", 10), ": ", ex[pos, 15];
		FinSi
		Si ex[pos, 21] = "SI" Entonces
			Escribir "ANULADO - Motivo: ", ex[pos, 20];
		FinSi
		Escribir LineaDe("=", 64);
	FinSi
FinFuncion

Funcion pos <- DerivarDocumento(ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia, codigo, usuario, mensajeError Por Referencia)
	// Derivación inicial: RECIBIDO -> DERIVADO al área del trámite
	Definir pos Como Entero;
	mensajeError <- "";
	pos <- BuscarExpediente(ex, cnt, codigo);
	Si pos = 0 Entonces
		mensajeError <- "Expediente no encontrado.";
	SiNo
		Si ex[pos, 18] <> "RECIBIDO" Entonces
			mensajeError <- Concatenar(Concatenar("Solo se deriva un expediente RECIBIDO (estado actual: ", ex[pos, 18]), ").");
			pos <- 0;
		SiNo
			ex[pos, 18] <- "DERIVADO";
			RegistrarHistorial(his, cnt, ex[pos, 1], "DERIVACION", Concatenar(Concatenar("Derivado al área de ", ex[pos, 10]), "."), usuario);
			NotificarDerivacion(ex, noti, cnt, pos);
		FinSi
	FinSi
FinFuncion

Funcion pos <- AnularDocumento(ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia, codigo, motivo, usuario, mensajeError Por Referencia)
	// Anula (NO elimina) un expediente RECIBIDO
	Definir pos Como Entero;
	mensajeError <- "";
	pos <- BuscarExpediente(ex, cnt, codigo);
	Si pos = 0 Entonces
		mensajeError <- "Expediente no encontrado.";
	SiNo
		Si ex[pos, 21] = "SI" Entonces
			mensajeError <- "El expediente ya se encuentra anulado.";
		SiNo
			Si ex[pos, 18] <> "RECIBIDO" Entonces
				mensajeError <- Concatenar(Concatenar("Solo se anula un expediente RECIBIDO (estado actual: ", ex[pos, 18]), ").");
			SiNo
				Si Recortar(motivo) = "" Entonces
					mensajeError <- "El motivo de anulación es obligatorio.";
				FinSi
			FinSi
		FinSi
		Si mensajeError <> "" Entonces
			pos <- 0;
		SiNo
			ex[pos, 18] <- "ANULADO";
			ex[pos, 21] <- "SI";
			ex[pos, 20] <- Recortar(motivo);
			RegistrarHistorial(his, cnt, ex[pos, 1], "ANULACION", Concatenar("Motivo: ", Recortar(motivo)), usuario);
			NotificarAnulacion(ex, noti, cnt, pos);
		FinSi
	FinSi
FinFuncion

// MÓDULO: mesa_partes/recepcion_fisica.py
SubProceso GenerarConstanciaFisica(ex Por Referencia, iExp)
	// Cargo de recepción que se entrega al ciudadano
	Escribir "";
	Escribir LineaDe("=", 40);
	Escribir " CARGO DE RECEPCIÓN - MESA DE PARTES FÍSICA";
	Escribir LineaDe("=", 40);
	Escribir "Constancia : ", ex[iExp, 22];
	Escribir "Expediente : ", ex[iExp, 1];
	Escribir "Solicitante: ", ex[iExp, 5];
	Escribir "Trámite    : ", ex[iExp, 8], "  | Folios: ", ex[iExp, 12];
	Escribir "Fecha      : ", ex[iExp, 19];
	Escribir LineaDe("=", 40);
FinSubProceso

SubProceso RegistrarDocumentoFisico(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	Definir tipoDoc, numDoc, tramite, subtipo, asunto Como Caracter;
	Definir dniV, rucV, tipoPersona Como Caracter;
	Definir datos, errores, erroresVal Como Caracter;
	Definir iPer, clave, folios, iExp, nErrores, nVal, k, respuesta Como Entero;
	Definir continuar Como Logico;
	Dimension datos[4];
	Dimension errores[21];
	Dimension erroresVal[5];
	
	Escribir "";
	Escribir "--- INGRESO CANAL FÍSICO ---";
	tipoDoc <- PedirTipoDocumento("Tipo de documento de identidad:");
	numDoc <- PedirNumeroDocumento(tipoDoc, "Número de documento");
	iPer <- BuscarPersonaPorDocumento(per, cnt, tipoDoc, numDoc);
	continuar <- Verdadero;
	
	Si iPer = 0 Entonces
		Escribir "La persona no está registrada en la data maestra.";
		respuesta <- LeerOpcion("¿Desea registrarla ahora?", "Sí|No", Falso);
		Si respuesta = 2 Entonces
			continuar <- Falso;
		SiNo
			iPer <- PedirDatosPersona(per, cnt, tipoDoc, numDoc);
			Si iPer = 0 Entonces
				continuar <- Falso;
			FinSi
		FinSi
	FinSi
	
	Si continuar Entonces
		tramite <- "";
		subtipo <- "";
		clave <- SeleccionarTramite(tramite, subtipo);
		Si clave > 0 Entonces
			asunto <- LeerTexto("Asunto del trámite");
			folios <- PedirFolios("Cantidad de folios");
			PedirDatosAdicionales(clave, datos);
			
			// Agregado en el avance 20/10: validación instantánea
			// (equivale al diccionario datos_validacion de Python)
			dniV <- "";
			rucV <- "";
			tipoPersona <- "natural";
			Si tipoDoc = "DNI" Entonces
				dniV <- numDoc;
			FinSi
			Si tipoDoc = "RUC" Entonces
				rucV <- numDoc;
				tipoPersona <- "juridica";
			FinSi
			// En el canal físico el PDF se simula con "documento_fisico.pdf"
			nVal <- ValidarEntradaInstantanea(dniV, rucV, tipoPersona, folios, "documento_fisico.pdf", erroresVal);
			Si nVal > 0 Entonces
				Escribir "";
				Escribir "[ERROR] Validación instantánea fallida:";
				Para k <- 1 Hasta nVal Con Paso 1 Hacer
					Escribir "- ", erroresVal[k];
				FinPara
			SiNo
				nErrores <- 0;
				iExp <- RegistrarDocumento(per, ex, his, noti, cnt, iPer, "FISICO", clave, tramite, subtipo, asunto, folios, datos, ses[2], "", "", errores, nErrores);
				Si nErrores > 0 Entonces
					Escribir "";
					Escribir "[ERROR] No se pudo registrar el documento:";
					Para k <- 1 Hasta nErrores Con Paso 1 Hacer
						Escribir "- ", errores[k];
					FinPara
				SiNo
					Escribir "";
					Escribir "[OK] Expediente físico creado: ", ex[iExp, 1], " | Estado: ", ex[iExp, 18];
					GenerarConstanciaFisica(ex, iExp);
				FinSi
			FinSi
		FinSi
	FinSi
FinSubProceso

// MÓDULO: mesa_partes/recepcion_virtual.py
Funcion r <- ValidarCasilla(per Por Referencia, usu Por Referencia, cnt Por Referencia, iPer)
	// La casilla existe solo si la persona tiene cuenta de usuario.
	// Devuelve el código de casilla o "" si no tiene.
	Definir r Como Caracter;
	r <- "";
	Si iPer > 0 Entonces
		Si BuscarUsuarioPorPersona(usu, cnt, per[iPer, 1]) > 0 Entonces
			r <- CodigoCasilla(per[iPer, 1]);
		FinSi
	FinSi
FinFuncion

SubProceso GenerarConstanciaVirtual(ex Por Referencia, iExp)
	Escribir "";
	Escribir LineaDe("=", 40);
	Escribir " SOLICITUD REGISTRADA - CASILLA ELECTRÓNICA";
	Escribir LineaDe("=", 40);
	Escribir "Constancia : ", ex[iExp, 22];
	Escribir "Expediente : ", ex[iExp, 1];
	Escribir "Casilla    : ", ex[iExp, 7];
	Escribir "Trámite    : ", ex[iExp, 8];
	Escribir "Estado     : ", ex[iExp, 18];
	Escribir LineaDe("=", 40);
FinSubProceso

SubProceso CapturarYRegistrar(per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia, iPer, usuario)
	// Pide los datos del trámite virtual y registra el expediente
	Definir casilla, tramite, subtipo, asunto, adjunto Como Caracter;
	Definir datos, errores Como Caracter;
	Definir clave, folios, iExp, nErrores, k, confirmar Como Entero;
	Dimension datos[4];
	Dimension errores[21];
	
	casilla <- ValidarCasilla(per, usu, cnt, iPer);
	Si casilla = "" Entonces
		Escribir "[ERROR] La persona no tiene casilla electrónica (necesita una cuenta de usuario).";
	SiNo
		tramite <- "";
		subtipo <- "";
		clave <- SeleccionarTramite(tramite, subtipo);
		Si clave > 0 Entonces
			asunto <- LeerTexto("Asunto digital");
			folios <- PedirFolios("Cantidad de folios digitales");
			PedirDatosAdicionales(clave, datos);
			adjunto <- PedirAdjuntoPdf("Nombre del archivo adjunto (ejemplo.pdf)");
			confirmar <- LeerOpcion("¿Confirmar envío?", "Sí|No", Falso);
			Si confirmar = 2 Entonces
				Escribir "Envío cancelado.";
			SiNo
				nErrores <- 0;
				iExp <- RegistrarDocumento(per, ex, his, noti, cnt, iPer, "VIRTUAL", clave, tramite, subtipo, asunto, folios, datos, usuario, casilla, adjunto, errores, nErrores);
				Si nErrores > 0 Entonces
					Escribir "";
					Escribir "[ERROR] No se pudo registrar el trámite virtual:";
					Para k <- 1 Hasta nErrores Con Paso 1 Hacer
						Escribir "- ", errores[k];
					FinPara
				SiNo
					GenerarConstanciaVirtual(ex, iExp);
				FinSi
			FinSi
		FinSi
	FinSi
FinSubProceso

SubProceso RegistrarDocumentoVirtual(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	// Mesa de Partes registra un documento virtual con el documento del ciudadano
	Definir tipoDoc, numDoc Como Caracter;
	Definir iPer Como Entero;
	Escribir "";
	Escribir "--- INGRESO CANAL VIRTUAL ---";
	tipoDoc <- PedirTipoDocumento("Tipo de documento de identidad:");
	numDoc <- PedirNumeroDocumento(tipoDoc, "Número de documento del ciudadano");
	iPer <- BuscarPersonaPorDocumento(per, cnt, tipoDoc, numDoc);
	Si iPer = 0 Entonces
		Escribir "[ERROR] La persona no está registrada.";
	SiNo
		CapturarYRegistrar(per, usu, ex, his, noti, cnt, iPer, ses[2]);
	FinSi
FinSubProceso

SubProceso EnviarSolicitudVirtual(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	// El propio ciudadano envía su solicitud desde su casilla
	Definir iPer Como Entero;
	iPer <- BuscarPersona(per, cnt, ses[4]);
	Escribir "";
	Escribir "--- ENVÍO DE SOLICITUD (CASILLA ELECTRÓNICA) ---";
	CapturarYRegistrar(per, usu, ex, his, noti, cnt, iPer, ses[2]);
FinSubProceso

// ============================================================
// MÓDULO: servicios/reportes.py
// (arreglos paralelos, matriz, burbuja, inserción y búsqueda binaria)
// ============================================================
Funcion n <- ConstruirArreglosParalelos(ex Por Referencia, cnt Por Referencia, codigos Por Referencia, estados Por Referencia, areas Por Referencia, fechas Por Referencia, tramites Por Referencia)
	// Misma posición = mismo expediente
	Definir n, i Como Entero;
	n <- cnt[3];
	Para i <- 1 Hasta n Con Paso 1 Hacer
		codigos[i] <- ex[i, 1];
		estados[i] <- ex[i, 18];
		areas[i] <- ex[i, 10];
		fechas[i] <- ex[i, 19];
		tramites[i] <- ex[i, 8];
	FinPara
FinFuncion

Funcion n <- ConstruirMatriz(ex Por Referencia, cnt Por Referencia, mat Por Referencia)
	// Cada fila es [codigo, estado, area, fecha, tramite, clave_fecha]
	Definir n, i Como Entero;
	Definir codigos, estados, areas, fechas, tramites Como Caracter;
	Dimension codigos[201];
	Dimension estados[201];
	Dimension areas[201];
	Dimension fechas[201];
	Dimension tramites[201];
	n <- ConstruirArreglosParalelos(ex, cnt, codigos, estados, areas, fechas, tramites);
	Para i <- 1 Hasta n Con Paso 1 Hacer
		mat[i, 1] <- codigos[i];
		mat[i, 2] <- estados[i];
		mat[i, 3] <- areas[i];
		mat[i, 4] <- fechas[i];
		mat[i, 5] <- tramites[i];
		mat[i, 6] <- FechaAClave(fechas[i]);
	FinPara
FinFuncion

Funcion n <- ListarOrdenado(ex Por Referencia, cnt Por Referencia, criterio, mat Por Referencia)
	// criterio: CODIGO, FECHA, ESTADO o AREA. Devuelve la cantidad de filas
	Definir n, columna Como Entero;
	n <- ConstruirMatriz(ex, cnt, mat);
	columna <- 1;
	Si criterio = "ESTADO" Entonces
		columna <- 2;
	FinSi
	Si criterio = "AREA" Entonces
		columna <- 3;
	FinSi
	Si criterio = "FECHA" Entonces
		// Se ordena por la columna 6 (clave de fecha ordenable)
		columna <- 6;
	FinSi
	OrdenarBurbujaMatriz(mat, n, columna, 6, Falso);
FinFuncion

SubProceso MostrarEncabezadoTabla(ancho)
	Escribir PadDer("CÓDIGO", 17), PadDer("ESTADO", 12), PadDer("ÁREA", 22), PadDer("FECHA", 18), "TRÁMITE";
	Escribir LineaDe("-", ancho);
FinSubProceso

SubProceso MostrarFila(c1, c2, c3, c4, c5)
	Escribir PadDer(c1, 17), PadDer(c2, 12), PadDer(c3, 22), PadDer(c4, 18), c5;
FinSubProceso

SubProceso MostrarTabla(mat Por Referencia, n)
	Definir i Como Entero;
	Si n = 0 Entonces
		Escribir "No hay expedientes registrados.";
	SiNo
		MostrarEncabezadoTabla(95);
		Para i <- 1 Hasta n Con Paso 1 Hacer
			MostrarFila(mat[i, 1], mat[i, 2], mat[i, 3], mat[i, 4], mat[i, 5]);
		FinPara
	FinSi
FinSubProceso

SubProceso BuscarPorCodigoBinaria(ex Por Referencia, cnt Por Referencia, codigo)
	// Ordena los códigos (inserción) y los busca con búsqueda binaria
	Definir n, pos Como Entero;
	Definir codigos, estados, areas, fechas, tramites Como Caracter;
	Dimension codigos[201];
	Dimension estados[201];
	Dimension areas[201];
	Dimension fechas[201];
	Dimension tramites[201];
	n <- ConstruirArreglosParalelos(ex, cnt, codigos, estados, areas, fechas, tramites);
	OrdenarInsercionParalelos(codigos, estados, areas, fechas, tramites, n, Falso);
	pos <- BuscarBinaria(codigos, n, Mayusculas(Recortar(codigo)));
	Si pos = 0 Entonces
		Escribir "Expediente no encontrado.";
	SiNo
		MostrarEncabezadoTabla(95);
		MostrarFila(codigos[pos], estados[pos], areas[pos], fechas[pos], tramites[pos]);
	FinSi
FinSubProceso

SubProceso ContarPorEstado(ex Por Referencia, cnt Por Referencia)
	// Dos arreglos paralelos: nombres de ESTADOS y sus conteos
	Definir estadosLista Como Caracter;
	Definir conteos, i, j Como Entero;
	Dimension conteos[9];
	estadosLista <- "RECIBIDO|DERIVADO|EN_PROCESO|OBSERVADO|SUBSANADO|ATENDIDO|ARCHIVADO|ANULADO";
	Para j <- 1 Hasta 8 Con Paso 1 Hacer
		conteos[j] <- 0;
	FinPara
	Para i <- 1 Hasta cnt[3] Con Paso 1 Hacer
		Para j <- 1 Hasta 8 Con Paso 1 Hacer
			Si ex[i, 18] = ObtenerItem(estadosLista, j, "|") Entonces
				conteos[j] <- conteos[j] + 1;
			FinSi
		FinPara
	FinPara
	Para j <- 1 Hasta 8 Con Paso 1 Hacer
		Escribir PadDer(ObtenerItem(estadosLista, j, "|"), 12), ": ", conteos[j];
	FinPara
FinSubProceso

SubProceso MenuReporte(ex Por Referencia, cnt Por Referencia)
	// Consulta: ordenar, buscar por código y estadísticas
	Definir mat Como Caracter;
	Definir k, n Como Entero;
	Dimension mat[201, 7];
	Repetir
		k <- LeerOpcion("CONSULTA DE EXPEDIENTES", "Listar ordenado por CÓDIGO|Listar ordenado por FECHA|Listar ordenado por ESTADO|Listar ordenado por ÁREA|Buscar por código (búsqueda binaria)|Cantidad de expedientes por estado", Verdadero);
		Segun k Hacer
			1:
				n <- ListarOrdenado(ex, cnt, "CODIGO", mat);
				MostrarTabla(mat, n);
			2:
				n <- ListarOrdenado(ex, cnt, "FECHA", mat);
				MostrarTabla(mat, n);
			3:
				n <- ListarOrdenado(ex, cnt, "ESTADO", mat);
				MostrarTabla(mat, n);
			4:
				n <- ListarOrdenado(ex, cnt, "AREA", mat);
				MostrarTabla(mat, n);
			5:
				BuscarPorCodigoBinaria(ex, cnt, LeerTexto("Código de expediente"));
			6:
				ContarPorEstado(ex, cnt);
		FinSegun
	Hasta Que k = 0
FinSubProceso

// MÓDULO: mesa_partes/mesa_partes.py  (menú del rol MESA_PARTES)
SubProceso RegistrarDocumentoCanal(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	// Pregunta por qué canal llegó el documento y llama a la recepción
	Definir canal Como Entero;
	canal <- LeerOpcion("CANAL DE RECEPCIÓN", "MESA DE PARTES EXTERNA - FÍSICO|MESA DE PARTES VIRTUAL - CASILLA ELECTRÓNICA", Verdadero);
	Si canal = 1 Entonces
		RegistrarDocumentoFisico(ses, per, usu, ex, his, noti, cnt);
	FinSi
	Si canal = 2 Entonces
		RegistrarDocumentoVirtual(ses, per, usu, ex, his, noti, cnt);
	FinSi
FinSubProceso

SubProceso OpcionAnular(ses Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	Definir codigo, motivo, mensajeError Como Caracter;
	Definir pos, respuesta Como Entero;
	codigo <- LeerTexto("Código de expediente");
	pos <- ConsultarDocumento(ex, cnt, codigo);
	Si pos > 0 Entonces
		respuesta <- LeerOpcion("¿Desea ANULAR el documento?", "Sí|No", Falso);
		Si respuesta = 1 Entonces
			motivo <- LeerTexto("Ingrese motivo de anulación");
			mensajeError <- "";
			pos <- AnularDocumento(ex, his, noti, cnt, codigo, motivo, ses[2], mensajeError);
			Si mensajeError <> "" Entonces
				Escribir "[ERROR] ", mensajeError;
			SiNo
				Escribir "";
				Escribir "[OK] DOCUMENTO ANULADO | ", ex[pos, 1], " | Motivo: ", ex[pos, 20];
				Escribir "  [OK] Se registró la anulación en el historial (el expediente NO se elimina).";
			FinSi
		FinSi
	FinSi
FinSubProceso

SubProceso OpcionDerivar(ses Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	Definir codigo, mensajeError Como Caracter;
	Definir pos Como Entero;
	codigo <- LeerTexto("Código de expediente");
	mensajeError <- "";
	pos <- DerivarDocumento(ex, his, noti, cnt, codigo, ses[2], mensajeError);
	Si mensajeError <> "" Entonces
		Escribir "[ERROR] ", mensajeError;
	SiNo
		Escribir "[OK] Expediente ", ex[pos, 1], " derivado a ", ex[pos, 10], ". Estado: ", ex[pos, 18];
	FinSi
FinSubProceso

SubProceso MenuMesaPartes(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	// Punto de entrada del rol MESA_PARTES
	Definir opc, pos Como Entero;
	Repetir
		Escribir "";
		Escribir LineaDe("=", 40);
		Escribir "MESA DE PARTES  -  Usuario: ", ses[2];
		Escribir LineaDe("=", 40);
		Escribir "1. Registrar documento";
		Escribir "2. Consultar documento";
		Escribir "3. Derivar documento";
		Escribir "4. Anular documento";
		Escribir "5. Consultar expedientes (ordenar / buscar)";
		Escribir "6. Notificaciones";
		Escribir "0. Cerrar sesión";
		opc <- LeerNumeroMenu("Seleccione: ");
		Segun opc Hacer
			1:
				RegistrarDocumentoCanal(ses, per, usu, ex, his, noti, cnt);
			2:
				pos <- ConsultarDocumento(ex, cnt, LeerTexto("Código de expediente"));
			3:
				OpcionDerivar(ses, ex, his, noti, cnt);
			4:
				OpcionAnular(ses, ex, his, noti, cnt);
			5:
				MenuReporte(ex, cnt);
			6:
				ListarTodasNotificaciones(noti, cnt);
			0:
				Escribir "Saliendo de Mesa de Partes...";
			De Otro Modo:
				Escribir "[ERROR] Opción no válida.";
		FinSegun
	Hasta Que opc = 0
FinSubProceso

// MÓDULO: ciudadano/ciudadano.py  (menú del rol CIUDADANO)
SubProceso VerPerfil(ses Por Referencia, per Por Referencia, cnt Por Referencia)
	Definir ip Como Entero;
	ip <- BuscarPersona(per, cnt, ses[4]);
	Si ip = 0 Entonces
		Escribir "No se encontraron los datos del ciudadano.";
	SiNo
		Escribir "";
		Escribir "--- MI PERFIL ---";
		Escribir "ID_PERSONA: ", FormatoId(per[ip, 1]);
		Escribir "Documento : ", per[ip, 2], " ", per[ip, 3];
		Escribir "Nombres   : ", per[ip, 4];
		Escribir "Apellidos : ", per[ip, 5];
		Escribir "Correo    : ", per[ip, 6];
		Escribir "Teléfono  : ", per[ip, 7];
	FinSi
FinSubProceso

SubProceso ConsultarMisExpedientes(ses Por Referencia, ex Por Referencia, cnt Por Referencia)
	// Lista los expedientes del ciudadano
	Definir i, total Como Entero;
	total <- 0;
	Para i <- 1 Hasta cnt[3] Con Paso 1 Hacer
		Si ex[i, 2] = ses[4] Entonces
			total <- total + 1;
			Si total = 1 Entonces
				Escribir "";
				Escribir "--- MIS EXPEDIENTES ---";
			FinSi
			Escribir ex[i, 1], " | ", PadDer(ex[i, 8], 32), " | ", ex[i, 18];
		FinSi
	FinPara
	Si total = 0 Entonces
		Escribir "No tiene expedientes registrados.";
	FinSi
FinSubProceso

Funcion pos <- ExpedientePropio(ses Por Referencia, ex Por Referencia, cnt Por Referencia)
	// Pide un código y devuelve la fila solo si pertenece al ciudadano
	Definir pos Como Entero;
	pos <- BuscarExpediente(ex, cnt, LeerTexto("Código de expediente"));
	Si pos > 0 Entonces
		Si ex[pos, 2] <> ses[4] Entonces
			pos <- 0;
		FinSi
	FinSi
	Si pos = 0 Entonces
		Escribir "No se encontró el expediente o no pertenece a su cuenta.";
	FinSi
FinFuncion

SubProceso ConsultarEstado(ses Por Referencia, ex Por Referencia, his Por Referencia, cnt Por Referencia)
	// Seguimiento de un expediente propio
	Definir pos Como Entero;
	pos <- ExpedientePropio(ses, ex, cnt);
	Si pos > 0 Entonces
		Escribir "";
		Escribir "--- SEGUIMIENTO DEL EXPEDIENTE ---";
		Escribir "Código     : ", ex[pos, 1];
		Escribir "Trámite    : ", ex[pos, 8];
		Escribir "Estado     : ", ex[pos, 18];
		Escribir "Área       : ", ex[pos, 10];
		Escribir "Canal      : ", ex[pos, 6];
		Escribir "Observación: Sin observaciones";
		VerHistorial(his, cnt, ex[pos, 1]);
	FinSi
FinSubProceso

SubProceso VerConstancias(ses Por Referencia, ex Por Referencia, cnt Por Referencia)
	// Lista las constancias generadas en los expedientes del ciudadano
	Definir i, total Como Entero;
	total <- 0;
	Para i <- 1 Hasta cnt[3] Con Paso 1 Hacer
		Si ex[i, 2] = ses[4] Y ex[i, 22] <> "" Entonces
			total <- total + 1;
			Si total = 1 Entonces
				Escribir "";
				Escribir "--- CONSTANCIAS ---";
			FinSi
			Escribir ex[i, 22], "  (expediente ", ex[i, 1], ", ", ex[i, 19], ")";
		FinSi
	FinPara
	Si total = 0 Entonces
		Escribir "No hay constancias disponibles.";
	FinSi
FinSubProceso

SubProceso MenuCiudadano(ses Por Referencia, per Por Referencia, usu Por Referencia, ex Por Referencia, his Por Referencia, noti Por Referencia, cnt Por Referencia)
	Definir opc Como Entero;
	Repetir
		VerCasilla(per, noti, cnt, ses[4]);
		Escribir "";
		Escribir "1. Ver mi perfil";
		Escribir "2. Nueva solicitud";
		Escribir "3. Mis expedientes";
		Escribir "4. Consultar estado / seguimiento";
		// Escribir "5. Subsanar observación";   (en construcción, depende del módulo Funcionario)
		Escribir "6. Notificaciones";
		Escribir "7. Constancias";
		Escribir "0. Cerrar sesión";
		opc <- LeerNumeroMenu("Seleccione una opción: ");
		Segun opc Hacer
			1:
				VerPerfil(ses, per, cnt);
			2:
				EnviarSolicitudVirtual(ses, per, usu, ex, his, noti, cnt);
			3:
				ConsultarMisExpedientes(ses, ex, cnt);
			4:
				ConsultarEstado(ses, ex, his, cnt);
			// 5: Subsanar(ses, ex, his, noti, cnt);   (en construcción)
			6:
				MenuMensajes(noti, cnt, ses[4]);
			7:
				VerConstancias(ses, ex, cnt);
			0:
				Escribir "Sesión del ciudadano finalizada.";
			De Otro Modo:
				Escribir "Opción no válida.";
		FinSegun
	Hasta Que opc = 0
FinSubProceso

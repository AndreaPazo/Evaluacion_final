-- ============================================================
-- Base de datos: Mesa de Partes (modelo en 3FN)
-- ============================================================
CREATE DATABASE MesaPartes;
GO
USE MesaPartes;
GO

-- ===================== TABLAS ======================

-- >>> INTEGRANTE 3: tabla Area
CREATE TABLE dbo.Area (
    IdArea  INT IDENTITY(1,1) NOT NULL,
    Nombre  NVARCHAR(60)      NOT NULL,
    CONSTRAINT PK_Area PRIMARY KEY (IdArea),
    CONSTRAINT UQ_Area_Nombre UNIQUE (Nombre)
);
-- <<< FIN INTEGRANTE 3 (Area)

-- >>> INTEGRANTE 2: tablas Tramite y SubtipoTramite
CREATE TABLE dbo.Tramite (
    IdTramite INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(80) NOT NULL UNIQUE,
    IdArea INT NOT NULL,
    PideDatosAdicionales BIT NOT NULL DEFAULT 0,
    CONSTRAINT FK_Tramite_Area FOREIGN KEY (IdArea) REFERENCES dbo.Area(IdArea) 
);

CREATE TABLE dbo.SubtipoTramite (
    IdTramite INT NOT NULL,
    IdSubtipo INT NOT NULL,
    Nombre NVARCHAR(40) NOT NULL,
    CONSTRAINT PK_SubtipoTramite PRIMARY KEY (IdTramite, IdSubtipo),
    CONSTRAINT FK_SubtipoTramite_Tramite FOREIGN KEY (IdTramite) REFERENCES dbo.Tramite(IdTramite)
);
-- <<< FIN INTEGRANTE 2

-- >>> INTEGRANTE 3: tablas Persona y Usuario
CREATE TABLE dbo.Persona (
    IdPersona        INT IDENTITY(1,1) NOT NULL,
    TipoDocumento    VARCHAR(3)    NOT NULL,
    NumeroDocumento  VARCHAR(11)   NOT NULL,
    Nombres          NVARCHAR(80)  NOT NULL,
    Apellidos        NVARCHAR(80)  NOT NULL,
    Correo           NVARCHAR(100) NOT NULL,
    Telefono         CHAR(9)       NOT NULL,
    Estado           VARCHAR(8)    NOT NULL DEFAULT 'ACTIVO',
    CONSTRAINT PK_Persona PRIMARY KEY (IdPersona),
    CONSTRAINT UQ_Persona_Documento UNIQUE (TipoDocumento, NumeroDocumento),
    CONSTRAINT CK_Persona_TipoDocumento CHECK (TipoDocumento IN ('DNI', 'CE', 'RUC')),
    CONSTRAINT CK_Persona_Telefono CHECK (Telefono LIKE '9[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    CONSTRAINT CK_Persona_Estado CHECK (Estado IN ('ACTIVO', 'INACTIVO'))
);

CREATE TABLE dbo.Usuario (
    IdUsuario       INT IDENTITY(1,1) NOT NULL,
    IdPersona       INT          NOT NULL,
    NombreUsuario   NVARCHAR(30) NOT NULL,
    ContrasenaHash  VARCHAR(200) NOT NULL,
    Rol             VARCHAR(15)  NOT NULL,
    IdArea          INT          NULL,
    Estado          VARCHAR(8)   NOT NULL DEFAULT 'ACTIVO',
    CONSTRAINT PK_Usuario PRIMARY KEY (IdUsuario),
    CONSTRAINT UQ_Usuario_Persona UNIQUE (IdPersona),
    CONSTRAINT UQ_Usuario_Nombre UNIQUE (NombreUsuario),
    CONSTRAINT FK_Usuario_Persona FOREIGN KEY (IdPersona) REFERENCES dbo.Persona (IdPersona),
    CONSTRAINT FK_Usuario_Area FOREIGN KEY (IdArea) REFERENCES dbo.Area (IdArea),
    CONSTRAINT CK_Usuario_Rol CHECK (Rol IN ('ADMINISTRADOR', 'MESA_PARTES', 'FUNCIONARIO', 'CIUDADANO')),
    CONSTRAINT CK_Usuario_Area CHECK ((Rol = 'FUNCIONARIO' AND IdArea IS NOT NULL)
                                   OR (Rol <> 'FUNCIONARIO' AND IdArea IS NULL)),
    CONSTRAINT CK_Usuario_Estado CHECK (Estado IN ('ACTIVO', 'INACTIVO'))
);
-- <<< FIN INTEGRANTE 3

-- >>> INTEGRANTE 3: tabla Expediente
CREATE TABLE dbo.Expediente (
    IdExpediente       INT IDENTITY(1,1) NOT NULL,
    Codigo             VARCHAR(20)     NOT NULL,          -- EXP-2026-000001
    CodigoConstancia   VARCHAR(30)     NULL,              -- CONST-2026-000001
    IdPersona          INT             NOT NULL,          -- solicitante
    IdTramite          INT             NOT NULL,
    IdSubtipo          INT             NULL,              -- solo LICENCIA tiene subtipos
    IdArea             INT             NOT NULL,          -- área donde está AHORA
    IdUsuarioRegistro  INT             NOT NULL,          -- quién lo registró
    Canal              VARCHAR(7)      NOT NULL,
    Asunto             NVARCHAR(500)   NOT NULL,
    Folios             INT             NULL,
    Adjunto            NVARCHAR(150)   NULL,              -- nombre del PDF (virtual)
    Estado             VARCHAR(10)     NOT NULL DEFAULT 'RECIBIDO',
    FechaRegistro      DATETIME        NOT NULL DEFAULT GETDATE(),
    MotivoAnulacion    NVARCHAR(500)   NULL,
    Observacion        NVARCHAR(1000)  NULL,
    Subsanacion        NVARCHAR(1000)  NULL,
    Respuesta          NVARCHAR(1000)  NULL,
    FechaCierre        DATETIME        NULL,              -- se llena al archivar
    AreaLaboro         NVARCHAR(100)   NULL,              -- datos adicionales
    NumeroOrden        VARCHAR(30)     NULL,
    TipoFirma          VARCHAR(10)     NULL,
    CONSTRAINT PK_Expediente PRIMARY KEY (IdExpediente),
    CONSTRAINT UQ_Expediente_Codigo UNIQUE (Codigo),
    CONSTRAINT FK_Expediente_Persona FOREIGN KEY (IdPersona) REFERENCES dbo.Persona (IdPersona),
    CONSTRAINT FK_Expediente_Tramite FOREIGN KEY (IdTramite) REFERENCES dbo.Tramite (IdTramite),
    CONSTRAINT FK_Expediente_Subtipo FOREIGN KEY (IdTramite, IdSubtipo)
        REFERENCES dbo.SubtipoTramite (IdTramite, IdSubtipo),
    CONSTRAINT FK_Expediente_Area FOREIGN KEY (IdArea) REFERENCES dbo.Area (IdArea),
    CONSTRAINT FK_Expediente_Usuario FOREIGN KEY (IdUsuarioRegistro) REFERENCES dbo.Usuario (IdUsuario),
    CONSTRAINT CK_Expediente_Canal CHECK (Canal IN ('FISICO', 'VIRTUAL')),
    CONSTRAINT CK_Expediente_Estado CHECK (Estado IN ('RECIBIDO', 'DERIVADO', 'EN_PROCESO', 'OBSERVADO',
                                                      'SUBSANADO', 'ATENDIDO', 'ARCHIVADO', 'ANULADO')),
    CONSTRAINT CK_Expediente_Folios CHECK (Folios IS NULL OR Folios > 0),
    CONSTRAINT CK_Expediente_Firma CHECK (TipoFirma IS NULL OR TipoFirma IN ('MANUSCRITA', 'DIGITAL')),
    CONSTRAINT CK_Expediente_Anulacion CHECK (Estado <> 'ANULADO' OR MotivoAnulacion IS NOT NULL)
);

-- La constancia no se repite (se permiten varias vacías mientras se asigna)
CREATE UNIQUE INDEX UX_Expediente_Constancia
    ON dbo.Expediente (CodigoConstancia) WHERE CodigoConstancia IS NOT NULL;

-- Acelera la bandeja del funcionario (busca por área y estado)
CREATE INDEX IX_Expediente_Area_Estado ON dbo.Expediente (IdArea, Estado);
-- <<< FIN INTEGRANTE 3 (Expediente)

-- >>> INTEGRANTE 4: tablas HistorialExpediente y Notificacion
-- <<< FIN INTEGRANTE 4

CREATE TABLE dbo.HistorialExpediente (
    IdHistorial   INT IDENTITY(1,1) NOT NULL,
    IdExpediente  INT               NOT NULL,
    Fecha         DATETIME          NOT NULL DEFAULT GETDATE(),
    Accion        NVARCHAR(30)      NOT NULL,
    Detalle       NVARCHAR(500)     NULL,
    IdUsuario     INT               NULL,
    CONSTRAINT PK_HistorialExpediente PRIMARY KEY (IdHistorial),
    CONSTRAINT FK_HistorialExpediente_Expediente FOREIGN KEY (IdExpediente)
        REFERENCES dbo.Expediente (IdExpediente),
    CONSTRAINT FK_HistorialExpediente_Usuario FOREIGN KEY (IdUsuario)
        REFERENCES dbo.Usuario (IdUsuario),
    CONSTRAINT CK_HistorialExpediente_Accion CHECK (Accion IN (
        'REGISTRADO', 'DERIVADO', 'EN_PROCESO', 'OBSERVADO',
        'SUBSANADO', 'ATENDIDO', 'ARCHIVADO', 'ANULADO'
    ))
);

CREATE INDEX IX_HistorialExpediente_Expediente_Fecha
    ON dbo.HistorialExpediente (IdExpediente, Fecha DESC);

CREATE TABLE dbo.Notificacion (
    IdNotificacion INT IDENTITY(1,1) NOT NULL,
    IdPersona      INT               NOT NULL,
    IdExpediente   INT               NULL,
    Tipo           VARCHAR(20)       NOT NULL,
    Mensaje        NVARCHAR(500)     NOT NULL,
    Fecha          DATETIME          NOT NULL DEFAULT GETDATE(),
    Leida          BIT               NOT NULL DEFAULT 0,
    CONSTRAINT PK_Notificacion PRIMARY KEY (IdNotificacion),
    CONSTRAINT FK_Notificacion_Persona FOREIGN KEY (IdPersona)
        REFERENCES dbo.Persona (IdPersona),
    CONSTRAINT FK_Notificacion_Expediente FOREIGN KEY (IdExpediente)
        REFERENCES dbo.Expediente (IdExpediente),
    CONSTRAINT CK_Notificacion_Tipo CHECK (Tipo IN (
        'REGISTRO', 'DERIVACION', 'OBSERVACION', 'SUBSANACION', 'ATENCION', 'ARCHIVO', 'ANULACION', 'GENERAL'
    ))
);

CREATE INDEX IX_Notificacion_Persona_Leida_Fecha
    ON dbo.Notificacion (IdPersona, Leida, Fecha DESC);
-- <<< FIN INTEGRANTE 4


-- ================= DATOS INICIALES =================

-- >>> INTEGRANTE 3: las 5 áreas
SET IDENTITY_INSERT dbo.Area ON;
INSERT INTO dbo.Area (IdArea, Nombre) VALUES
 (1, 'RECURSOS HUMANOS'),
 (2, 'ABASTECIMIENTO'),
 (3, 'SERVICIOS AL USUARIO'),
 (4, 'PRESUPUESTO PUBLICO'),
 (5, 'FINANZAS');
SET IDENTITY_INSERT dbo.Area OFF;
-- <<< FIN INTEGRANTE 3

-- >>> INTEGRANTE 2: trámites y subtipos
INSERT INTO dbo.Tramite (Nombre, IdArea, PideDatosAdicionales) VALUES
    (N'LICENCIA', 1, 0),
    (N'DESCANSO MEDICO', 1, 0),
    (N'CONSTANCIA DE TRABAJO', 1, 1),
    (N'SOLICITUD DE ORDEN DE SERVICIOS', 2, 1),
    (N'REPROGRAMACION DE VACACIONES', 1, 0);

INSERT INTO dbo.SubtipoTramite (IdTramite, IdSubtipo, Nombre) VALUES
    (1, 1, N'CON GOCE'),
    (1, 2, N'SIN GOCE');
-- <<< FIN INTEGRANTE 2

-- >>> INTEGRANTE 3: personas y cuentas de usuario
SET IDENTITY_INSERT dbo.Persona ON;
INSERT INTO dbo.Persona (IdPersona, TipoDocumento, NumeroDocumento, Nombres, Apellidos, Correo, Telefono, Estado) VALUES
 (1, 'DNI', '40949554', 'JOSE JAVIER', 'CORONADO RAMOS', 'josecoronadoramos@gmail.com', '985951485', 'ACTIVO'),
 (2, 'DNI', '72845631', 'JUAN', 'PEREZ GARCIA', 'juan@gmail.com', '987654321', 'ACTIVO'),
 (3, 'CE', 'A1234567', 'MARIA', 'LOPEZ DIAZ', 'maria@gmail.com', '999111222', 'INACTIVO'),
 (4, 'DNI', '10000001', 'ADMIN', 'SISTEMA', 'admin@entidad.gob.pe', '900000001', 'ACTIVO'),
 (5, 'DNI', '10000002', 'MESA', 'PARTES UNO', 'mesa@entidad.gob.pe', '900000002', 'ACTIVO'),
 (6, 'DNI', '10000003', 'FUNCIONARIO', 'RRHH', 'rrhh@entidad.gob.pe', '900000003', 'ACTIVO'),
 (7, 'DNI', '10000004', 'FUNCIONARIO', 'ABASTECIMIENTO', 'abast@entidad.gob.pe', '900000004', 'ACTIVO'),
 (8, 'DNI', '85758790', 'FUNCIONARIO', 'SERVICIOS', 'servicios@entidad.gob.pe', '900000123', 'ACTIVO'),
 (9, 'DNI', '85967411', 'FUNCIONARIO', 'PRESUPUESTO', 'presupuesto@entidad.gob.pe', '987589123', 'ACTIVO'),
 (10, 'DNI', '78965489', 'FUNCIONARIO', 'FINANZAS', 'finanzas@entidad.gob.pe', '985745125', 'ACTIVO');
SET IDENTITY_INSERT dbo.Persona OFF;

SET IDENTITY_INSERT dbo.Usuario ON;
-- Cuentas sin área (ciudadanos, administrador y Mesa de Partes)
INSERT INTO dbo.Usuario (IdUsuario, IdPersona, NombreUsuario, ContrasenaHash, Rol, IdArea, Estado) VALUES
 (1, 1, 'jcoronado', '8b92d999ed8639675a8f4220caacb563$87e7698f8341ea6085d1ec5a98261638613852083de6574f1e94d392e51804e4', 'CIUDADANO', NULL, 'ACTIVO'),
 (2, 2, 'jperez', 'ea3ad4505267176920847905ec63583e$42ade2d1515c3dbb8cdda8f86be1a9f0a12cc183b28d2fea1dc778e144c47f79', 'CIUDADANO', NULL, 'ACTIVO'),
 (3, 3, 'mlopez', '87fe34a2dd6ba53b4541b5e692cfc9a7$a3436944fc8ced2ba026a5e04c0e6d308f07f594971469d68fda1221f0708e86', 'CIUDADANO', NULL, 'ACTIVO'),
 (4, 4, 'admin', 'f1c12dd780eeceef4c21e3a89cf76cc3$aa483aab922d3a561f848750947020c010ff5b155859a74a5e50d5d4c35196d8', 'ADMINISTRADOR', NULL, 'ACTIVO'),
 (5, 5, 'mesa01', 'd796cb6f6e1fe9a545d51d9d30529aad$4ffb48cf160b853a11cafc5fddb7a5924dadbeb175b107e85bf39324e2bea74e', 'MESA_PARTES', NULL, 'ACTIVO');

-- Funcionarios: el IdArea se toma de la tabla Area según su nombre
INSERT INTO dbo.Usuario (IdUsuario, IdPersona, NombreUsuario, ContrasenaHash, Rol, IdArea, Estado)
SELECT v.IdUsuario, v.IdPersona, v.NombreUsuario, v.ContrasenaHash, 'FUNCIONARIO', a.IdArea, 'ACTIVO'
FROM (VALUES
 (6, 6, 'func_rrhh', '78bedc9f54c0e5f691caadcdf4e3a552$a9b4fc33b115d3fd8e9ec4272ac22dc7c0ca14cf6ff9500198a0d8e83893de8f', 'RECURSOS HUMANOS'),
 (7, 7, 'func_abast', 'b2c130512c585f004179e04c38e4aae8$d1d95df9750308f2f04a3d24b054f18a72f90fa96376165fc632e35b7077c00e', 'ABASTECIMIENTO'),
 (8, 8, 'func_servicios', '6bad7b45a9949b6f57f3c66e4d810b8e$a242d7fd9a552075b484b2a0d33ac5ca09196a99e9a7a1e0f709316e05c798a7', 'SERVICIOS AL USUARIO'),
 (9, 9, 'func_presupuesto', 'bf404fde5ff6ad832b9862542f214c6a$cf2bf3475802a48f42b53b7481d3a22578dd55a40a302e8b03423d556b119f56', 'PRESUPUESTO PUBLICO'),
 (10, 10, 'func_finanzas', '3135d23f3745c835a0dcaa1c05b00466$ce9e69abae272d6dc80bfd2bdc0c0f645e8e750e8f64d529ae76fbe46eeba198', 'FINANZAS')
) AS v (IdUsuario, IdPersona, NombreUsuario, ContrasenaHash, NombreArea)
JOIN dbo.Area a ON a.Nombre = v.NombreArea;
SET IDENTITY_INSERT dbo.Usuario OFF;
-- <<< FIN INTEGRANTE 3

-- (Expedientes, historial y notificaciones empiezan vacíos)
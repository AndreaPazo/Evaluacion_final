-- ============================================================
-- Base de datos: Mesa de Partes (modelo en 3FN)
-- ============================================================
CREATE DATABASE MesaPartes;
GO
USE MesaPartes;
GO

-- ===================== TABLAS ======================

-- >>> INTEGRANTE 1: tabla Area
-- <<< FIN INTEGRANTE 1 (Area)

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
-- <<< FIN INTEGRANTE 3

-- >>> INTEGRANTE 1: tabla Expediente
-- <<< FIN INTEGRANTE 1 (Expediente)

-- >>> INTEGRANTE 4: tablas HistorialExpediente y Notificacion
-- <<< FIN INTEGRANTE 4

-- ================= DATOS INICIALES =================

-- >>> INTEGRANTE 1: las 5 áreas
-- <<< FIN INTEGRANTE 1

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
-- <<< FIN INTEGRANTE 3

-- (Expedientes, historial y notificaciones empiezan vacíos)
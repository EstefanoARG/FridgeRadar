-- =========================================================
-- BASE DE DATOS: FRIDGERADAR
-- Motor: MySQL 8+
-- Versión: 2.0 (Producción-Ready)
-- =========================================================

DROP DATABASE IF EXISTS fridgeradar_db;

CREATE DATABASE fridgeradar_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fridgeradar_db;

-- Activar scheduler para eventos automáticos
SET GLOBAL event_scheduler = ON;

-- =========================================================
-- 1. USUARIOS
-- =========================================================

CREATE TABLE usuario (
    id_usuario       INT AUTO_INCREMENT PRIMARY KEY,
    nombres          VARCHAR(100) NOT NULL,
    apellidos        VARCHAR(100),
    correo           VARCHAR(150) NOT NULL UNIQUE,
    password_hash    VARCHAR(255) NOT NULL,
    fecha_registro   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso    TIMESTAMP    NULL,
    estado           ENUM('activo','suspendido','eliminado') DEFAULT 'activo'
);

-- =========================================================
-- 2. HOGARES / GRUPOS
-- =========================================================

CREATE TABLE hogar (
    id_hogar          INT AUTO_INCREMENT PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL,
    codigo_invitacion VARCHAR(20)  UNIQUE,
    fecha_creacion    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuario_hogar (
    id_usuario_hogar INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario       INT  NOT NULL,
    id_hogar         INT  NOT NULL,
    rol              ENUM('owner','admin','miembro') DEFAULT 'miembro',
    fecha_union      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE,
    FOREIGN KEY (id_hogar)   REFERENCES hogar(id_hogar)
        ON DELETE CASCADE,

    UNIQUE KEY uq_usuario_hogar (id_usuario, id_hogar)
);

-- =========================================================
-- 3. ZONAS DE ALMACENAMIENTO
-- FIX: ahora pertenecen a un hogar específico
-- =========================================================

CREATE TABLE zona (
    id_zona          INT AUTO_INCREMENT PRIMARY KEY,
    id_hogar         INT  NOT NULL,                  -- ← FIX: era global
    nombre           VARCHAR(50) NOT NULL,
    tipo             ENUM(
                         'refrigerador',
                         'congelador',
                         'alacena',
                         'cajon',
                         'puerta_refri'
                     ) NOT NULL,
    icono            VARCHAR(100),
    temperatura_min  DECIMAL(4,1),
    temperatura_max  DECIMAL(4,1),

    FOREIGN KEY (id_hogar) REFERENCES hogar(id_hogar)
        ON DELETE CASCADE
);

-- =========================================================
-- 4. ESTANTES VISUALES
-- =========================================================

CREATE TABLE estante (
    id_estante         INT AUTO_INCREMENT PRIMARY KEY,
    id_zona            INT         NOT NULL,
    nombre             VARCHAR(50) NOT NULL,
    posicion_vertical  INT         NOT NULL,
    color_ui           VARCHAR(20),

    FOREIGN KEY (id_zona) REFERENCES zona(id_zona)
        ON DELETE CASCADE
);

-- =========================================================
-- 5. CATEGORÍAS DE PRODUCTOS
-- =========================================================

CREATE TABLE categoria_producto (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL UNIQUE,
    icono        VARCHAR(100),
    color        VARCHAR(20)
);

-- =========================================================
-- 6. PRODUCTOS BASE (catálogo global)
-- =========================================================

CREATE TABLE producto (
    id_producto                INT AUTO_INCREMENT PRIMARY KEY,
    nombre                     VARCHAR(150) NOT NULL,
    descripcion                TEXT,
    id_categoria               INT,
    codigo_barras              VARCHAR(50),             -- ← NUEVO: scanner futuro
    unidad_medida              ENUM(
                                   'unidad',
                                   'kg',
                                   'g',
                                   'litro',
                                   'ml',
                                   'paquete',
                                   'lata',
                                   'botella',
                                   'taza',
                                   'cucharada'
                               ) DEFAULT 'unidad',
    perecible                  BOOLEAN DEFAULT TRUE,
    dias_promedio_vencimiento  INT,
    imagen                     VARCHAR(255),

    FOREIGN KEY (id_categoria) REFERENCES categoria_producto(id_categoria)
);

-- =========================================================
-- 7. INVENTARIO REAL DEL USUARIO
-- FIX: agrega id_usuario_agrego para trazabilidad
-- =========================================================

CREATE TABLE inventario (
    id_inventario      INT AUTO_INCREMENT PRIMARY KEY,
    id_hogar           INT  NOT NULL,
    id_producto        INT  NOT NULL,
    id_estante         INT  NOT NULL,
    id_usuario_agrego  INT  NOT NULL,                   -- ← FIX: quién lo metió
    cantidad           DECIMAL(10,2) NOT NULL DEFAULT 1,
    fecha_compra       DATE,
    fecha_vencimiento  DATE,
    abierto            BOOLEAN DEFAULT FALSE,
    observaciones      TEXT,
    estado_caducidad   ENUM(
                           'verde',
                           'amarillo',
                           'rojo',
                           'vencido'
                       ) DEFAULT 'verde',
    fecha_registro     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_hogar)          REFERENCES hogar(id_hogar),
    FOREIGN KEY (id_producto)       REFERENCES producto(id_producto),
    FOREIGN KEY (id_estante)        REFERENCES estante(id_estante),
    FOREIGN KEY (id_usuario_agrego) REFERENCES usuario(id_usuario)
);

-- =========================================================
-- 8. HISTORIAL DE MOVIMIENTOS
-- FIX: registra qué usuario ejecutó cada acción
-- =========================================================

CREATE TABLE movimiento_inventario (
    id_movimiento    INT AUTO_INCREMENT PRIMARY KEY,
    id_inventario    INT  NOT NULL,
    id_usuario       INT  NOT NULL,                     -- ← FIX: quién lo hizo
    tipo_movimiento  ENUM(
                         'agregado',
                         'movido',
                         'consumido',
                         'eliminado',
                         'vencido'
                     ) NOT NULL,
    cantidad         DECIMAL(10,2),
    descripcion      TEXT,
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_inventario) REFERENCES inventario(id_inventario),
    FOREIGN KEY (id_usuario)    REFERENCES usuario(id_usuario)
);

-- =========================================================
-- 9. RECETAS
-- FIX: id_usuario_creador para separar recetas sistema vs. usuario
-- =========================================================

CREATE TABLE receta (
    id_receta           INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario_creador  INT  NULL,                      -- ← NUEVO: NULL = sistema
    nombre              VARCHAR(150) NOT NULL,
    descripcion         TEXT,
    instrucciones       LONGTEXT,
    tiempo_preparacion  INT,
    dificultad          ENUM('facil','media','dificil') DEFAULT 'facil',
    porciones           INT,
    imagen              VARCHAR(255),
    calorias            INT,
    es_publica          BOOLEAN   DEFAULT TRUE,
    fecha_creacion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario_creador) REFERENCES usuario(id_usuario)
        ON DELETE SET NULL
);

-- =========================================================
-- 10. TAGS / ETIQUETAS DE RECETAS
-- NUEVO: vegetariano, sin gluten, etc.
-- =========================================================

CREATE TABLE tag_receta (
    id_tag   INT AUTO_INCREMENT PRIMARY KEY,
    nombre   VARCHAR(50) NOT NULL UNIQUE,
    color    VARCHAR(20)
);

CREATE TABLE receta_tag (
    id_receta_tag INT AUTO_INCREMENT PRIMARY KEY,
    id_receta     INT NOT NULL,
    id_tag        INT NOT NULL,

    FOREIGN KEY (id_receta) REFERENCES receta(id_receta) ON DELETE CASCADE,
    FOREIGN KEY (id_tag)    REFERENCES tag_receta(id_tag),

    UNIQUE KEY uq_receta_tag (id_receta, id_tag)
);

-- =========================================================
-- 11. INGREDIENTES DE RECETAS
-- FIX: agrega unidad_medida y nota por ingrediente
-- =========================================================

CREATE TABLE receta_ingrediente (
    id_receta_ingrediente INT AUTO_INCREMENT PRIMARY KEY,
    id_receta             INT  NOT NULL,
    id_producto           INT  NOT NULL,
    cantidad              DECIMAL(10,2),
    unidad_medida         ENUM(                         -- ← FIX: era implícito
                              'unidad',
                              'kg',
                              'g',
                              'litro',
                              'ml',
                              'taza',
                              'cucharada',
                              'pizca'
                          ) DEFAULT 'unidad',
    obligatorio           BOOLEAN DEFAULT TRUE,
    nota                  VARCHAR(200),                 -- ej: "picado fino"

    FOREIGN KEY (id_receta)   REFERENCES receta(id_receta)   ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- =========================================================
-- 12. RECETAS FAVORITAS
-- =========================================================

CREATE TABLE receta_favorita (
    id_receta_favorita INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario         INT NOT NULL,
    id_receta          INT NOT NULL,
    fecha_guardado     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_receta)  REFERENCES receta(id_receta)   ON DELETE CASCADE,

    UNIQUE KEY uq_favorita (id_usuario, id_receta)
);

-- =========================================================
-- 13. ALERTAS
-- FIX: link directo al inventario afectado
-- =========================================================

CREATE TABLE alerta (
    id_alerta      INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario     INT  NOT NULL,
    id_inventario  INT  NULL,                           -- ← FIX: producto específico
    titulo         VARCHAR(150) NOT NULL,
    mensaje        TEXT         NOT NULL,
    tipo           ENUM(
                       'vencimiento',
                       'desperdicio',
                       'receta',
                       'stock_bajo'
                   ) NOT NULL,
    leida          BOOLEAN   DEFAULT FALSE,
    fecha_alerta   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario)    REFERENCES usuario(id_usuario)       ON DELETE CASCADE,
    FOREIGN KEY (id_inventario) REFERENCES inventario(id_inventario) ON DELETE SET NULL
);

-- =========================================================
-- 14. HISTORIAL DE DESPERDICIO
-- =========================================================

CREATE TABLE desperdicio (
    id_desperdicio     INT AUTO_INCREMENT PRIMARY KEY,
    id_inventario      INT  NOT NULL,
    cantidad           DECIMAL(10,2),
    motivo             ENUM('vencido','mal_estado','olvido','otro'),
    comentario         TEXT,
    fecha_desperdicio  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_inventario) REFERENCES inventario(id_inventario)
);

-- =========================================================
-- 15. LISTA DE COMPRAS
-- FIX: agrega prioridad en detalle
-- =========================================================

CREATE TABLE lista_compra (
    id_lista        INT AUTO_INCREMENT PRIMARY KEY,
    id_hogar        INT         NOT NULL,
    nombre          VARCHAR(100),
    estado          ENUM('activa','completada') DEFAULT 'activa',
    fecha_creacion  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_hogar) REFERENCES hogar(id_hogar) ON DELETE CASCADE
);

CREATE TABLE lista_compra_detalle (
    id_detalle   INT AUTO_INCREMENT PRIMARY KEY,
    id_lista     INT  NOT NULL,
    id_producto  INT  NOT NULL,
    cantidad     DECIMAL(10,2),
    unidad       VARCHAR(30),
    prioridad    ENUM('alta','media','baja') DEFAULT 'media', -- ← NUEVO
    comprado     BOOLEAN DEFAULT FALSE,
    nota         VARCHAR(200),

    FOREIGN KEY (id_lista)    REFERENCES lista_compra(id_lista)    ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- =========================================================
-- 16. SUGERENCIAS "TENGO HAMBRE"
-- FIX: agrega id_hogar para multi-hogar
-- =========================================================

CREATE TABLE sugerencia_receta (
    id_sugerencia            INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario               INT  NOT NULL,
    id_hogar                 INT  NOT NULL,             -- ← FIX
    id_receta                INT  NOT NULL,
    porcentaje_coincidencia  DECIMAL(5,2),
    usa_productos_criticos   BOOLEAN   DEFAULT FALSE,
    fecha_sugerencia         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_hogar)   REFERENCES hogar(id_hogar),
    FOREIGN KEY (id_receta)  REFERENCES receta(id_receta)
);

-- =========================================================
-- ÍNDICES DE OPTIMIZACIÓN
-- =========================================================

CREATE INDEX idx_inventario_vencimiento   ON inventario(fecha_vencimiento);
CREATE INDEX idx_inventario_estado        ON inventario(estado_caducidad);
CREATE INDEX idx_inventario_hogar         ON inventario(id_hogar);
CREATE INDEX idx_producto_nombre          ON producto(nombre);
CREATE INDEX idx_producto_codigo_barras   ON producto(codigo_barras);
CREATE INDEX idx_alerta_usuario           ON alerta(id_usuario);
CREATE INDEX idx_alerta_leida             ON alerta(leida);
CREATE INDEX idx_receta_nombre            ON receta(nombre);
CREATE INDEX idx_movimiento_inventario    ON movimiento_inventario(id_inventario);
CREATE INDEX idx_zona_hogar               ON zona(id_hogar);

-- =========================================================
-- TRIGGER 1: Semáforo en INSERT
-- =========================================================

DELIMITER $$

CREATE TRIGGER trg_semaforo_insert
BEFORE INSERT ON inventario
FOR EACH ROW
BEGIN
    DECLARE dias INT;
    SET dias = DATEDIFF(NEW.fecha_vencimiento, CURDATE());

    SET NEW.estado_caducidad = CASE
        WHEN dias > 7            THEN 'verde'
        WHEN dias BETWEEN 3 AND 7 THEN 'amarillo'
        WHEN dias BETWEEN 0 AND 2 THEN 'rojo'
        ELSE                         'vencido'
    END;
END$$

-- =========================================================
-- TRIGGER 2: Semáforo en UPDATE
-- FIX: el original no cubría actualizaciones
-- =========================================================

CREATE TRIGGER trg_semaforo_update
BEFORE UPDATE ON inventario
FOR EACH ROW
BEGIN
    DECLARE dias INT;

    IF NEW.fecha_vencimiento IS NOT NULL THEN
        SET dias = DATEDIFF(NEW.fecha_vencimiento, CURDATE());

        SET NEW.estado_caducidad = CASE
            WHEN dias > 7             THEN 'verde'
            WHEN dias BETWEEN 3 AND 7 THEN 'amarillo'
            WHEN dias BETWEEN 0 AND 2 THEN 'rojo'
            ELSE                          'vencido'
        END;
    END IF;
END$$

-- =========================================================
-- TRIGGER 3: Log automático al consumir / eliminar
-- =========================================================

CREATE TRIGGER trg_log_movimiento
AFTER UPDATE ON inventario
FOR EACH ROW
BEGIN
    IF NEW.cantidad < OLD.cantidad THEN
        INSERT INTO movimiento_inventario
            (id_inventario, id_usuario, tipo_movimiento, cantidad, descripcion)
        VALUES
            (NEW.id_inventario,
             NEW.id_usuario_agrego,
             'consumido',
             OLD.cantidad - NEW.cantidad,
             'Reducción detectada automáticamente');
    END IF;
END$$

DELIMITER ;

-- =========================================================
-- EVENT: Recalculo diario del semáforo
-- FIX: el trigger original nunca actualizaba con el paso del tiempo
-- =========================================================

CREATE EVENT evt_actualizar_semaforo
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
    UPDATE inventario
    SET estado_caducidad = CASE
        WHEN DATEDIFF(fecha_vencimiento, CURDATE()) > 7            THEN 'verde'
        WHEN DATEDIFF(fecha_vencimiento, CURDATE()) BETWEEN 3 AND 7 THEN 'amarillo'
        WHEN DATEDIFF(fecha_vencimiento, CURDATE()) BETWEEN 0 AND 2 THEN 'rojo'
        ELSE                                                             'vencido'
    END
    WHERE fecha_vencimiento IS NOT NULL;

-- =========================================================
-- EVENT: Alertas automáticas de vencimiento
-- Corre cada mañana a las 8:00 AM
-- =========================================================

DELIMITER $$

CREATE EVENT evt_generar_alertas_vencimiento
ON SCHEDULE EVERY 1 DAY
STARTS (TIMESTAMP(CURRENT_DATE) + INTERVAL 8 HOUR)
DO
BEGIN
    -- Alerta para productos en rojo (0-2 días)
    INSERT INTO alerta (id_usuario, id_inventario, titulo, mensaje, tipo)
    SELECT
        uh.id_usuario,
        i.id_inventario,
        CONCAT('⛔ Vence hoy o mañana: ', p.nombre),
        CONCAT(p.nombre, ' vence el ', DATE_FORMAT(i.fecha_vencimiento, '%d/%m/%Y'), '. ¡Úsalo ya!'),
        'vencimiento'
    FROM inventario i
    JOIN producto p         ON i.id_producto = p.id_producto
    JOIN usuario_hogar uh   ON i.id_hogar    = uh.id_hogar
    WHERE i.estado_caducidad = 'rojo'
      AND NOT EXISTS (
          SELECT 1 FROM alerta a
          WHERE a.id_inventario = i.id_inventario
            AND a.tipo          = 'vencimiento'
            AND DATE(a.fecha_alerta) = CURDATE()
      );

    -- Alerta para productos en amarillo (3-7 días)
    INSERT INTO alerta (id_usuario, id_inventario, titulo, mensaje, tipo)
    SELECT
        uh.id_usuario,
        i.id_inventario,
        CONCAT('⚠️ Próximo a vencer: ', p.nombre),
        CONCAT(p.nombre, ' vence en ', DATEDIFF(i.fecha_vencimiento, CURDATE()), ' días.'),
        'vencimiento'
    FROM inventario i
    JOIN producto p         ON i.id_producto = p.id_producto
    JOIN usuario_hogar uh   ON i.id_hogar    = uh.id_hogar
    WHERE i.estado_caducidad = 'amarillo'
      AND NOT EXISTS (
          SELECT 1 FROM alerta a
          WHERE a.id_inventario = i.id_inventario
            AND a.tipo          = 'vencimiento'
            AND DATE(a.fecha_alerta) = CURDATE()
      );
END$$

DELIMITER ;

-- =========================================================
-- VIEWS ÚTILES PARA EL BACKEND
-- =========================================================

-- Vista: Inventario completo con semáforo y zona
CREATE VIEW v_inventario_completo AS
SELECT
    i.id_inventario,
    i.id_hogar,
    p.nombre                                          AS producto,
    p.imagen,
    cat.nombre                                        AS categoria,
    z.nombre                                          AS zona,
    z.tipo                                            AS tipo_zona,
    e.nombre                                          AS estante,
    i.cantidad,
    p.unidad_medida,
    i.fecha_vencimiento,
    DATEDIFF(i.fecha_vencimiento, CURDATE())          AS dias_restantes,
    i.estado_caducidad,
    i.abierto,
    i.fecha_registro
FROM inventario i
JOIN producto          p   ON i.id_producto  = p.id_producto
JOIN estante           e   ON i.id_estante   = e.id_estante
JOIN zona              z   ON e.id_zona      = z.id_zona
LEFT JOIN categoria_producto cat ON p.id_categoria = cat.id_categoria
ORDER BY i.fecha_vencimiento ASC;

-- Vista: Recetas posibles con ingredientes actuales (lógica "Tengo Hambre")
CREATE VIEW v_recetas_posibles AS
SELECT
    r.id_receta,
    r.nombre                                                    AS receta,
    r.tiempo_preparacion,
    r.dificultad,
    r.imagen,
    COUNT(ri.id_receta_ingrediente)                            AS total_ingredientes,
    SUM(CASE WHEN i.id_inventario IS NOT NULL THEN 1 ELSE 0 END) AS ingredientes_disponibles,
    ROUND(
        SUM(CASE WHEN i.id_inventario IS NOT NULL THEN 1 ELSE 0 END)
        / COUNT(ri.id_receta_ingrediente) * 100, 1
    )                                                          AS porcentaje_match,
    MAX(CASE WHEN i.estado_caducidad IN ('amarillo','rojo') THEN 1 ELSE 0 END)
                                                               AS usa_criticos
FROM receta r
JOIN receta_ingrediente ri ON r.id_receta   = ri.id_receta
LEFT JOIN inventario i     ON ri.id_producto = i.id_producto
                          AND i.cantidad > 0
WHERE ri.obligatorio = TRUE
GROUP BY r.id_receta, r.nombre, r.tiempo_preparacion, r.dificultad, r.imagen;

-- Vista: Desperdicio por hogar (métricas ecológicas)
CREATE VIEW v_desperdicio_por_hogar AS
SELECT
    h.id_hogar,
    h.nombre                          AS hogar,
    p.nombre                          AS producto,
    SUM(d.cantidad)                   AS total_desperdiciado,
    p.unidad_medida,
    d.motivo,
    COUNT(*)                          AS veces,
    DATE_FORMAT(MIN(d.fecha_desperdicio), '%Y-%m') AS primer_mes,
    DATE_FORMAT(MAX(d.fecha_desperdicio), '%Y-%m') AS ultimo_mes
FROM desperdicio d
JOIN inventario i ON d.id_inventario = i.id_inventario
JOIN producto   p ON i.id_producto   = p.id_producto
JOIN hogar      h ON i.id_hogar      = h.id_hogar
GROUP BY h.id_hogar, h.nombre, p.nombre, p.unidad_medida, d.motivo;

-- =========================================================
-- STORED PROCEDURE: "Tengo Hambre"
-- Devuelve recetas filtrando por hogar y priorizando críticos
-- =========================================================

DELIMITER $$

CREATE PROCEDURE sp_tengo_hambre(
    IN  p_id_hogar      INT,
    IN  solo_criticos   BOOLEAN,     -- TRUE = solo usa amarillo/rojo
    IN  limite          INT          -- cuántas recetas devolver
)
BEGIN
    SELECT
        r.id_receta,
        r.nombre,
        r.descripcion,
        r.tiempo_preparacion,
        r.dificultad,
        r.porciones,
        r.imagen,
        r.calorias,
        ROUND(
            SUM(CASE WHEN i.id_inventario IS NOT NULL THEN 1 ELSE 0 END)
            / COUNT(ri.id_receta_ingrediente) * 100, 1
        )  AS porcentaje_match,
        MAX(CASE WHEN i.estado_caducidad IN ('amarillo','rojo') THEN 1 ELSE 0 END)
           AS usa_criticos
    FROM receta r
    JOIN receta_ingrediente ri  ON r.id_receta    = ri.id_receta
    LEFT JOIN inventario i      ON ri.id_producto  = i.id_producto
                               AND i.id_hogar      = p_id_hogar
                               AND i.cantidad      > 0
                               AND (solo_criticos = FALSE
                                    OR i.estado_caducidad IN ('amarillo','rojo'))
    WHERE ri.obligatorio = TRUE
    GROUP BY
        r.id_receta, r.nombre, r.descripcion,
        r.tiempo_preparacion, r.dificultad,
        r.porciones, r.imagen, r.calorias
    HAVING
        -- Al menos 70% de ingredientes disponibles
        ROUND(
            SUM(CASE WHEN i.id_inventario IS NOT NULL THEN 1 ELSE 0 END)
            / COUNT(ri.id_receta_ingrediente) * 100, 1
        ) >= 70
    ORDER BY
        usa_criticos DESC,
        porcentaje_match DESC
    LIMIT limite;
END$$

-- =========================================================
-- STORED PROCEDURE: Agregar producto al inventario
-- Registra movimiento automáticamente
-- =========================================================

CREATE PROCEDURE sp_agregar_inventario(
    IN p_id_hogar          INT,
    IN p_id_producto       INT,
    IN p_id_estante        INT,
    IN p_id_usuario        INT,
    IN p_cantidad          DECIMAL(10,2),
    IN p_fecha_compra      DATE,
    IN p_fecha_vencimiento DATE,
    IN p_observaciones     TEXT
)
BEGIN
    DECLARE nuevo_id INT;

    INSERT INTO inventario (
        id_hogar, id_producto, id_estante, id_usuario_agrego,
        cantidad, fecha_compra, fecha_vencimiento, observaciones
    ) VALUES (
        p_id_hogar, p_id_producto, p_id_estante, p_id_usuario,
        p_cantidad, p_fecha_compra, p_fecha_vencimiento, p_observaciones
    );

    SET nuevo_id = LAST_INSERT_ID();

    -- Log automático del movimiento
    INSERT INTO movimiento_inventario
        (id_inventario, id_usuario, tipo_movimiento, cantidad, descripcion)
    VALUES
        (nuevo_id, p_id_usuario, 'agregado', p_cantidad, 'Producto ingresado al inventario');

    SELECT nuevo_id AS id_inventario_creado;
END$$

DELIMITER ;

-- =========================================================
-- DATOS INICIALES
-- =========================================================

-- Categorías
INSERT INTO categoria_producto (nombre, icono, color) VALUES
('Lácteos',      '🥛', '#E3F2FD'),
('Carnes',       '🥩', '#FFEBEE'),
('Verduras',     '🥦', '#E8F5E9'),
('Frutas',       '🍎', '#FFF3E0'),
('Bebidas',      '🧃', '#E1F5FE'),
('Snacks',       '🍿', '#FFF8E1'),
('Condimentos',  '🫙', '#F3E5F5'),
('Granos',       '🌾', '#EFEBE9'),
('Congelados',   '❄️', '#E0F7FA'),
('Panadería',    '🍞', '#FBE9E7');

-- Tags de recetas
INSERT INTO tag_receta (nombre, color) VALUES
('Vegetariano',   '#4CAF50'),
('Vegano',        '#8BC34A'),
('Sin gluten',    '#FF9800'),
('Sin lactosa',   '#03A9F4'),
('Rápido',        '#9C27B0'),
('Económico',     '#F44336'),
('Alto proteico', '#3F51B5'),
('Bajo en calorías', '#009688');

-- =========================================================
-- CONSULTAS DE REFERENCIA (para el backend)
-- =========================================================

/*
-- 1. Productos próximos a vencer ordenados por urgencia
SELECT producto, zona, estante, cantidad, unidad_medida,
       fecha_vencimiento, dias_restantes, estado_caducidad
FROM v_inventario_completo
WHERE id_hogar = :hogar_id
  AND estado_caducidad IN ('amarillo','rojo','vencido')
ORDER BY dias_restantes ASC;

-- 2. "Tengo Hambre" — solo con lo crítico
CALL sp_tengo_hambre(:hogar_id, TRUE, 10);

-- 3. "Tengo Hambre" — con todo el inventario
CALL sp_tengo_hambre(:hogar_id, FALSE, 10);

-- 4. Recetas posibles con porcentaje de coincidencia
SELECT * FROM v_recetas_posibles
WHERE usa_criticos = 1
ORDER BY porcentaje_match DESC;

-- 5. Métricas de desperdicio del hogar
SELECT * FROM v_desperdicio_por_hogar
WHERE id_hogar = :hogar_id;

-- 6. Alertas no leídas del usuario
SELECT titulo, mensaje, tipo, fecha_alerta
FROM alerta
WHERE id_usuario = :usuario_id AND leida = FALSE
ORDER BY fecha_alerta DESC;

-- 7. Historial de movimientos del hogar (últimos 30 días)
SELECT u.nombres, p.nombre AS producto,
       mi.tipo_movimiento, mi.cantidad, mi.fecha_movimiento
FROM movimiento_inventario mi
JOIN inventario i ON mi.id_inventario = i.id_inventario
JOIN producto   p ON i.id_producto    = p.id_producto
JOIN usuario    u ON mi.id_usuario    = u.id_usuario
WHERE i.id_hogar = :hogar_id
  AND mi.fecha_movimiento >= NOW() - INTERVAL 30 DAY
ORDER BY mi.fecha_movimiento DESC;
*/
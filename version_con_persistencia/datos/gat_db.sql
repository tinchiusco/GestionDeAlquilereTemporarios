CREATE DATABASE IF NOT EXISTS gat_db;
USE gat_db;

-- 1. Tabla de Propietarios
CREATE TABLE IF NOT EXISTS propietarios (
    id_propietario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL,
    apellido VARCHAR(25) NOT NULL,
    telefono VARCHAR(25),
    email VARCHAR(50),
    dni VARCHAR(20) NOT NULL UNIQUE
);

-- 2. Tabla de Propiedades (Relación de Agregación con Propietarios: ON DELETE SET NULL)
CREATE TABLE IF NOT EXISTS propiedades (
    id_propiedad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    tipo VARCHAR(25),
    observaciones VARCHAR(150),
    id_propietario INT NULL,
    FOREIGN KEY (id_propietario) REFERENCES propietarios(id_propietario) ON DELETE SET NULL
);

-- 3. Tabla de Estadías (Relación de Composición con Propiedades: ON DELETE CASCADE)
CREATE TABLE IF NOT EXISTS estadias (
    id_estadia INT AUTO_INCREMENT PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    monto_total DECIMAL(10, 2) NOT NULL,
    plataforma VARCHAR(25),
    id_propiedad INT NOT NULL,
    FOREIGN KEY (id_propiedad) REFERENCES propiedades(id_propiedad) ON DELETE CASCADE
);

-- 4. Tabla de Egresos (Relación de Composición con Propiedades: ON DELETE CASCADE)
CREATE TABLE IF NOT EXISTS egresos (
    id_egreso INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    descripcion VARCHAR(150),
    id_propiedad INT NOT NULL,
    FOREIGN KEY (id_propiedad) REFERENCES propiedades(id_propiedad) ON DELETE CASCADE
);

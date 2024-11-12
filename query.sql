CREATE DATABASE proyecto;

USE proyecto;

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    tipo ENUM('administrador', 'empleado')
);

CREATE TABLE Departamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    gerente_id INT,
    FOREIGN KEY (gerente_id) REFERENCES Usuario(id)
);

CREATE TABLE Empleado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    direccion VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(50),
    fecha_inicio DATE,
    salario DECIMAL(10, 2),
    departamento_id INT,
    FOREIGN KEY (departamento_id) REFERENCES Departamento(id)
);

CREATE TABLE Proyecto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion TEXT,
    fecha_inicio DATE
);

CREATE TABLE RegistroTiempo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    horas INT,
    descripcion TEXT,
    empleado_id INT,
    proyecto_id INT,
    FOREIGN KEY (empleado_id) REFERENCES Empleado(id),
    FOREIGN KEY (proyecto_id) REFERENCES Proyecto(id)
);



INSERT INTO Usuario (username, password, tipo) VALUES 
('admin1', 'password123', 'administrador'),
('empleado1', 'password123', 'empleado'),
('empleado2', 'password123', 'empleado'),
('admin2', 'password456', 'administrador'),
('empleado3', 'password456', 'empleado');


INSERT INTO Departamento (nombre, gerente_id) VALUES 
('Recursos Humanos', 1),
('Desarrollo Sostenible', 4),
('Investigación y Desarrollo', 1),
('Ventas', 4);

INSERT INTO Empleado (nombre, direccion, telefono, email, fecha_inicio, salario, departamento_id) VALUES
('Carlos Perez', 'Calle 1', '123456789', 'carlos@example.com', '2022-01-15', 2500.00, 1),
('Ana Gomez', 'Calle 2', '987654321', 'ana@example.com', '2021-06-20', 2700.00, 2),
('Luis Morales', 'Calle 3', '456789123', 'luis@example.com', '2020-09-10', 2900.00, 3),
('Mariana Ruiz', 'Calle 4', '321654987', 'mariana@example.com', '2019-03-05', 3100.00, 4),
('Fernando Silva', 'Calle 5', '654123789', 'fernando@example.com', '2018-12-25', 2600.00, 1);


INSERT INTO Proyecto (nombre, descripcion, fecha_inicio) VALUES 
('Proyecto Solar', 'Implementación de paneles solares en la empresa', '2023-01-10'),
('Proyecto Eficiencia Energética', 'Mejorar la eficiencia energética de los procesos', '2022-11-15'),
('Proyecto Reciclaje', 'Implementación de un sistema de reciclaje', '2023-03-05');

INSERT INTO RegistroTiempo (fecha, horas, descripcion, empleado_id, proyecto_id) VALUES
('2023-01-12', 8, 'Instalación inicial de paneles solares', 1, 1),
('2023-01-13', 6, 'Configuración de inversores solares', 1, 1),
('2022-11-17', 7, 'Evaluación de consumo energético', 2, 2),
('2022-11-18', 5, 'Implementación de medidas de eficiencia', 2, 2),
('2023-03-07', 4, 'Capacitación de empleados en reciclaje', 3, 3),
('2023-03-08', 6, 'Recolección inicial de materiales reciclables', 3, 3);

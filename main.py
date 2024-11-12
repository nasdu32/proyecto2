import mysql.connector
from abc import ABC, abstractmethod

# Conexión a MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyecto"
)

# Clase abstracta Usuario
class Usuario(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abstractmethod
    def autenticar(self):
        pass

# Subclase Administrador
class Administrador(Usuario):
    def autenticar(self):
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE username = %s AND password = %s AND tipo = 'administrador'",
                       (self.username, self.password))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            print("Autenticación exitosa para Administrador.")
            return True
        else:
            print("Autenticación fallida.")
            return False

    def crear_departamento(self, nombre, gerente_id):
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Departamento (nombre, gerente_id) VALUES (%s, %s)", (nombre, gerente_id))
        conexion.commit()
        print(f"Departamento '{nombre}' creado.")
        cursor.close()

    def crear_proyecto(self, nombre, descripcion, fecha_inicio):
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Proyecto (nombre, descripcion, fecha_inicio) VALUES (%s, %s, %s)", 
                       (nombre, descripcion, fecha_inicio))
        conexion.commit()
        print(f"Proyecto '{nombre}' creado.")
        cursor.close()

# Subclase EmpleadoUsuario
class EmpleadoUsuario(Usuario):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.id = None

    def autenticar(self):
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM Usuario WHERE username = %s AND password = %s AND tipo = 'empleado'",
                       (self.username, self.password))
        resultado = cursor.fetchone()
        if resultado:
            self.id = resultado[0]
            print("Autenticación exitosa para Empleado.")
            cursor.close()
            return True
        else:
            print("Autenticación fallida.")
            cursor.close()
            return False

    def registrar_tiempo(self, fecha, horas, descripcion):
        if not self.id:
            print("No se pudo registrar el tiempo: Empleado no autenticado.")
            return
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO RegistroTiempo (fecha, horas, descripcion, empleado_id) VALUES (%s, %s, %s, %s)",
            (fecha, horas, descripcion, self.id)
        )
        conexion.commit()
        print("Registro de tiempo agregado.")
        cursor.close()

# Clase Autorizacion (Patrón Experto)
class Autorizacion:
    @staticmethod
    def verificar_permisos(usuario, accion):
        print(f"Verificando permisos para {usuario.username} en la acción {accion}")

# Función para registrar un nuevo usuario
def registrar_usuario():
    username = input("Ingrese nombre de usuario: ")
    password = input("Ingrese contraseña: ")
    tipo = input("Ingrese tipo de usuario (administrador/empleado): ").lower()
    if tipo not in ["administrador", "empleado"]:
        print("Tipo de usuario no válido.")
        return
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Usuario (username, password, tipo) VALUES (%s, %s, %s)", (username, password, tipo))
    conexion.commit()
    print(f"Usuario '{username}' registrado como {tipo}.")
    cursor.close()

def mostrar_menu():
    print("\nSistema de Gestión de Empleados")
    print("1. Autenticar Administrador")
    print("2. Registrar tiempo (Empleado)")
    print("3. Crear departamento (Administrador)")
    print("4. Listar Usuarios")
    print("5. Listar Departamentos")
    print("6. Listar Empleados")
    print("7. Listar Proyectos")
    print("8. Listar Registros de Tiempo")
    print("9. Registrar nuevo usuario")
    print("10. Crear proyecto (Administrador)")
    print("11. Salir")
    return input("Seleccione una opción: ")

# Funciones para listar información de cada tabla
def listar_usuarios():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Usuario")
    resultados = cursor.fetchall()
    print("\nUsuarios:")
    for fila in resultados:
        print(fila)
    cursor.close()

def listar_departamentos():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Departamento")
    resultados = cursor.fetchall()
    print("\nDepartamentos:")
    for fila in resultados:
        print(fila)
    cursor.close()

def listar_empleados():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Empleado")
    resultados = cursor.fetchall()
    print("\nEmpleados:")
    for fila in resultados:
        print(fila)
    cursor.close()

def listar_proyectos():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Proyecto")
    resultados = cursor.fetchall()
    print("\nProyectos:")
    for fila in resultados:
        print(fila)
    cursor.close()

def listar_registros_tiempo():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM RegistroTiempo")
    resultados = cursor.fetchall()
    print("\nRegistros de Tiempo:")
    for fila in resultados:
        print(fila)
    cursor.close()

# Menú principal
while True:
    opcion = mostrar_menu()

    if opcion == "1":
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        admin = Administrador(username, password)
        if admin.autenticar():
            print("Bienvenido Administrador.")
    
    elif opcion == "2":
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        empleado = EmpleadoUsuario(username, password)
        if empleado.autenticar():
            fecha = input("Fecha de registro (YYYY-MM-DD): ")
            horas = int(input("Horas trabajadas: "))
            descripcion = input("Descripción de tareas: ")
            empleado.registrar_tiempo(fecha, horas, descripcion)
    
    elif opcion == "3":
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        admin = Administrador(username, password)
        if admin.autenticar():
            nombre_departamento = input("Nombre del departamento: ")
            gerente_id = int(input("ID del gerente: "))
            admin.crear_departamento(nombre_departamento, gerente_id)
    
    elif opcion == "4":
        listar_usuarios()
    
    elif opcion == "5":
        listar_departamentos()
    
    elif opcion == "6":
        listar_empleados()
    
    elif opcion == "7":
        listar_proyectos()
    
    elif opcion == "8":
        listar_registros_tiempo()
    
    elif opcion == "9":
        registrar_usuario()
    
    elif opcion == "10":
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        admin = Administrador(username, password)
        if admin.autenticar():
            nombre_proyecto = input("Nombre del proyecto: ")
            descripcion = input("Descripción del proyecto: ")
            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
            admin.crear_proyecto(nombre_proyecto, descripcion, fecha_inicio)
    
    elif opcion == "11":
        print("Saliendo del sistema.")
        break
    
    else:
        print("Opción no válida. Intente nuevamente.")

conexion.close()

#importación de librerías
import socket    
import threading

clientes = {} # Diccionario para guardar usuarios conectados
lock = threading.Lock() # objeto de bloqueo para evitar problemas de accesos múltiples al diccionario

MENU = """ 
Seleccione una opción:
1) Login - iniciar sesión
2) Send - enviar mensaje privado
3) Sendall - enviar mensaje a todos
4) Show - mostrar usuarios conectados
5) Exit - salir
"""

def manejar_cliente(conn, addr): # maneja un cliente en un hilo, adrr es la información de ip
    nombre_usuario = None # al principio el cliente no está identificado
    conn.sendall(MENU.encode()) # se envía el menú al cliente

    while True:
        try:
            data = conn.recv(1024).decode().strip() # el servidor espera la opción elejida por el cliente, recibe 1024 bytes
            if not data:
                break # por si el cliente se desconecta

            if data == "1":  # Login
                conn.sendall("Ingrese su nombre de usuario: ".encode())
                nombre_usuario = conn.recv(1024).decode().strip()
                with lock:
                    clientes[nombre_usuario] = conn # se guarda la conexión
                conn.sendall(f"[Servidor] Bienvenido, {nombre_usuario}!\n".encode()) # el servidor envía un mensaje de bienvenida

            elif data == "2":  # Enviar mensaje privado
                conn.sendall("Ingrese el nombre del destinatario: ".encode()) 
                destinatario = conn.recv(1024).decode().strip()
                conn.sendall("Ingrese el mensaje: ".encode())
                mensaje = conn.recv(1024).decode().strip()
                
                with lock: # ejecución bajo bloqueo para que el hilo actual no se vea afectado por otro hilo que intente acceder 
                    if destinatario in clientes: # busca el destinatario en el diccionario clientes
                        clientes[destinatario].sendall(f"[{nombre_usuario}] {mensaje}\n".encode()) # envía el mensaje al destinatario
                    else:
                        conn.sendall("[Servidor] Usuario no encontrado.\n".encode()) # por si el destinatario no se encuentra

            elif data == "3":  # Enviar mensaje a todos
                conn.sendall("Ingrese el mensaje para todos: ".encode()) 
                mensaje = conn.recv(1024).decode().strip()
                with lock:
                    for usuario, c in clientes.items():
                        if usuario != nombre_usuario:
                            c.sendall(f"[{nombre_usuario} a todos] {mensaje}\n".encode())

            elif data == "4":  # Mostrar usuarios conectados
                with lock:
                    usuarios = ', '.join(clientes.keys()) # el método clientes.keys() devuelve una vista de las claves del diccionario clientes, join toma la vista y crea una cadena uniendo las claves separadas por una coma (,)
                conn.sendall(f"[Servidor] Usuarios conectados: {usuarios}\n".encode()) # el servidor envía los usuarios conectados

            elif data == "5":  # Salir
                break # finaliza el while

            else:
                conn.sendall("[Servidor] Opción inválida. Intente nuevamente.\n".encode()) # validación por si el usuario ingresa una opción incorrecta

            conn.sendall(MENU.encode()) # Volver a mostrar el menú

        except Exception as e: # para el caso de que el servidor encuentre algún error
            print(f"[Error] Cliente {addr} - {e}") # la variable "e" accede al tipo de error 
            break

    if nombre_usuario:
        with lock:
            clientes.pop(nombre_usuario, None) # se quita al usuario del diccionario cuando se va
    conn.close() # se cierra la conexión
    print(f"[Servidor] Cliente {addr} desconectado.") # mensaje de cliente desconectado 

def iniciar_servidor(): # bloque fincipal del servidor 
    host = "0.0.0.0" # para que el servidor escuhe cualquier conexión desde cualquier dispositivo de la red
    port = 12345
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crea el socket socket.AF_INET = ipv4, socket.SOCK_STREAM = TCP
    servidor.bind((host, port)) # enlaza el socket con la ip y el puerto servidor.bind((host, port)) # enlaza el socket con la ip y el puerto
    servidor.listen(5) # escucha 5 peticiones
    print(f"[Servidor] Escuchando en {host}:{port}...")
    
    while True:
        conn, addr = servidor.accept() # el servidor acepta la nueva conexión y crea un nuevo socket con la ip el puerto del cliente
        print(f"[Servidor] Nueva conexión desde {addr}") # mensaje de nueva conexión
        threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start() # se crea un nuevo hilo con Thread, start() inicia la ejecución del hilo, threading permite controlar el acceso a recursos compartidos entre hilos
        #target=manejar_cliente: manejar_cliente es la función que se encargará de procesar la conexión con un cliente, args=(conn, addr): define los argumentos que se pasarán a la función manejar_cliente, conn y adrr (conexión e ip)
        #daemon=True: el hilo finalizará automáticamente cuando el programa principal termine de ejecutarse. 
        
if __name__ == "__main__": # para que el código se ejecute cuando el archivo se ejecute directamente como un script principal
    iniciar_servidor()





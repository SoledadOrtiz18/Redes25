#importación de librerías
import socket
import threading

def recibir_mensajes(sock): # función para recibir mensajes del servidor
    while True:
        try:
            mensaje = sock.recv(1024).decode() # el cliente recibe el mensaje
            if not mensaje:
                break
            print("\n" + mensaje)
        except:
            break

def enviar_mensajes(sock): # función para enviar mensajes al servidor
    while True:
        try:
            opcion = input("> ").strip() # el cliente elige una opción del 1 al 5
            sock.sendall(opcion.encode()) # envía la opción elegida

            if opcion == "1":  # Login
                usuario = input("Ingrese nombre de usuario: ")
                sock.sendall(usuario.encode())

            elif opcion == "2":  # Enviar mensaje privado
                destinatario = input("Enviar a: ")
                mensaje = input("Mensaje: ")
                sock.sendall(destinatario.encode())
                sock.recv(1024)  # espera prompt "Ingrese el mensaje"
                sock.sendall(mensaje.encode())

            elif opcion == "3":  # Enviar mensaje a todos
                mensaje = input("Mensaje para todos: ")
                sock.sendall(mensaje.encode())

            elif opcion == "4":
                continue  # Solo muestra usuarios

            elif opcion == "5": #salir
                break

            else:
                print("Opción inválida.")

        except:
            break

def main():
    host = "127.0.0.1"
    port = 12345

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port)) # Conexión con el servidor

    print("[Conectado al servidor]")

    threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True).start() # Hilo para recibir mensajes mientras se escriben otros
    enviar_mensajes(cliente) # Se queda esperando input

    cliente.close()
    print("[Cliente desconectado]")

if __name__ == "__main__":
    main()
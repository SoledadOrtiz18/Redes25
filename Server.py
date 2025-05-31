# Este es el primer programa donde vamos a usar la libreria socket
# vamos a trabajar con el modelo cliente-Servidor


import socket  # importa la libreria socket

print("Este programa es el primer programa servidor en python")
print("IP address:", socket.gethostbyname(socket.gethostname()))
print("Hostname:", socket.gethostname())
print("IP address:", socket.gethostbyname("www.google.com"))

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crea el socket socket.AF_INET = ipv4, socket.SOCK_STREAM = TCP
host = socket.gethostname()
port = 12345
ServerSocket.bind(("0.0.0.0", port)) # enlaza el socket con la ip y el puerto ServerSocket.bind((host, port)) # enlaza el socket con la ip y el puerto

ServerSocket.listen(5) # escucha 5 peticiones

while True: # bucle infinito
    cliente = input("¡Bienvenido! Ingrese su nombre: ") #Recibido el nombre del cliente
    ClientSocket, addr = ServerSocket.accept()
    print("Conexion desde: ", addr)
    msg = "Gracias por la conexion" + "" + cliente + "\r\n"
    ClientSocket.send(msg.encode("utf-8"))
    while True:
        data = ClientSocket.recv(1024)
        print("El cliente " + cliente + " " + "mandó: ", data.decode("utf-8"))
        if data.decode("utf-8") == "chau":
            ClientSocket.close()
            break





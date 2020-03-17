import socket 
import select
import sys
import threading


#Funcion que logea al cliente con un nickname
def login(cliente):
	#Se envia un 0 al servidor para indicar que se enviara el nickname
	while True:
		nickname = input("\nIntroduce nickname: ")
		#Se envia la flag 0 para indicar que se enviara el nickname
		cliente.send("0".encode())
		if( cliente.recv(1).decode() == "0" ):
			#Se recibio confirmacion para conectarse
			cliente.send(nickname.encode())
			break
		else:
			print("\nOcurrió un error...")	

#Funcion para enviar archivos
def enviar_archivo(cliente):
	print("Enviar archivo")
	cliente.send("1".encode())

#Funcion para enviar mensajes
def enviar_msg(cliente):
	msg = input("Mensaje: ")
	cliente.send(msg.encode())

#Funcion del hilo para recibir mensajes
def recibir_msg(cliente):
	while True:
			try:
				msg_recv = cliente.recv(1024).decode()
				print("Mensaje recibido: "+msg_recv)
			except:
				pass

#Funcion que indica la acción a ejecutar en cliente
def menu_cliente(cliente):
	#Hilo para que el cliente pueda recibir mensajes
	msg_recv = threading.Thread(target=recibir_msg, args=(cliente,))
	msg_recv.daemon = True
	msg_recv.start()

	#Ciclo infinito para realizar una accion en el cliente
	while True:
		opc = input("\nElige una opcion: \n1.Enviar mensaje\n2.Enviar archivo\n3.Cerrar sesión\n")

		if opc == "1":
			enviar_msg(cliente)
		if opc == "2":
			enviar_archivo(cliente)
		if opc == "3":
			cliente.close()
			sys.exit()


#Se crea el socket 
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = "192.168.0.29"
port = 1211

#Se conecta al socket mediante la ip y el puerto
cliente.connect((host, port))

print("\n")

login(cliente)	

menu_cliente(cliente)

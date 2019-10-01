#!/usr/bin/env python3
import socket
import time
import threading

buffer_size = 1024


def conexion(): #Funcion que recibe Ip y Port del usuario
    #addr=input('Enter ip address: ')
    #port=input('Enter port: ')
    addr='10.100.74.228'
    port=1234
    return addr,port


def difficult(TCPClientSocket,data):#Funcion en sincronia con welcome from server
    difficult = input("dif"+data)
    difficult = difficult.upper()
    data = str.encode(difficult)
    TCPClientSocket.sendall(data)  # Envia dificultad



def send_recive_data(TCPClientSocket):
    while True: #COMUNICACION JUEGO
        data = TCPClientSocket.recv(buffer_size)  # recive msg from server correct or incorrect
        data = data.decode(encoding="utf-8")      # o bandera de perdedor o ganador
        if data == 'W':                           #o Peticion de otra letra
            print('YOU WIN')
            return False
        elif data == 'L':
            print('YOU LOSE')
            return False
        else:
            letra=input(data)
            letra=letra.lower()
            letra= str.encode(letra)
            TCPClientSocket.sendall(letra)          #Send new_letter

            data=TCPClientSocket.recv(buffer_size)  #Recive answer
            data= data.decode(encoding="utf-8")
            print('respuesta: '+ data)

            data=b'respuesta confirmada'            #Answer confirmed
            TCPClientSocket.sendall(data)

            data=TCPClientSocket.recv(buffer_size) #recive table
            data = data.decode(encoding="utf-8")
            print(".::"+data+"::.")

            data=b'tablero confirmado'            #Tablero confirmado
            TCPClientSocket.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    addr,port=conexion()
    TCPClientSocket.connect(( addr, int(port) ))
    data = TCPClientSocket.recv(buffer_size)  #Recibe mensaje welcome players o P2
    data = data.decode(encoding="utf-8")
    if data == 'P2':
        data=b'P2 recived'
        TCPClientSocket.sendall(data)
        time.sleep(0.1)
        """data = TCPClientSocket.recv(buffer_size)
        data = data.decode(encoding="utf-8")
        print('tablero:' + data*2)
        time.sleep(0.5)"""

        send_recive_data(TCPClientSocket) #Llamada de funcion que inicia la comunicacion del juego
    else:                           #Solo entra Player 1
        difficult(TCPClientSocket,data) #Envio y recepcion de mensajes entre esta funcion y welcome de servidor
        send_recive_data(TCPClientSocket)





#!/usr/bin/env python3
import socket
import time
import threading
import os

buffer_size = 1024


def conexion(): #Funcion que recibe Ip y Port del usuario
    #addr=input('Enter ip address: ')
    #port=input('Enter port: ')
    addr='127.0.0.1'
    port=1234
    return addr,port


def difficult(TCPClientSocket,data):#Funcion en sincronia con welcome from server
    difficult = input(data)
    difficult = difficult.upper()
    data = str.encode(difficult)
    TCPClientSocket.sendall(data)  # Envia dificultad



def send_recive_data(TCPClientSocket):
    while True: #COMUNICACION JUEGO
        data = TCPClientSocket.recv(buffer_size)  # recive msg from server correct or incorrect
        data = data.decode(encoding="utf-8")      # signal of loser or winner or table
        if data == 'W':                           #o Peticion de otra letra
            print('YOU WIN')
            break
        elif data == 'L':
            print('YOU LOSE')
            break
        elif data=='table':
            data = TCPClientSocket.recv(buffer_size)
            data = data.decode(encoding="utf-8")
            print(".::"+data+"::.")
        else:
            letra=input(data)
            letra=letra.lower()
            letra= str.encode(letra)
            TCPClientSocket.sendall(letra)          #Send new_letter
            os.system("clear")
            data=TCPClientSocket.recv(buffer_size)  #Recive answer
            data= data.decode(encoding="utf-8")
            print('respuesta: '+ data)
            data=b'respuesta confirmada'            #Answer confirmed
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
        send_recive_data(TCPClientSocket) #Llamada de funcion que inicia la comunicacion del juego
    else:                           #Solo entra Player 1
        difficult(TCPClientSocket,data) #Envio y recepcion de mensajes entre esta funcion y welcome de servidor
        send_recive_data(TCPClientSocket)





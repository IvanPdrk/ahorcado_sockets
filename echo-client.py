#!/usr/bin/env python3
import socket
import time
import threading

buffer_size = 1024


def conexion(): #Funcion que recibe Ip y Port del usuario
    addr=input('Enter ip address: ')
    port=input('Enter port: ')
    #addr='127.0.0.1'
    #port=1234
    return  addr,port


def send_recive_data(TCPClientSocket):
    while True: #COMUNICACION JUEGO
        data = TCPClientSocket.recv(buffer_size)  # recive msg from server respuesta
        data = data.decode(encoding="utf-8")      # o bandera de perdeor o ganador
        if data == 'W':
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
    addr,port=conexion() #
    TCPClientSocket.connect(( addr, int(port) ))

    data = TCPClientSocket.recv(buffer_size)  # Recibe mensaje welcome(difficultad) o P2
    data = data.decode(encoding="utf-8")

    if data == 'P2':
        time.sleep(0.01)
        data = TCPClientSocket.recv(buffer_size)
        data = data.decode(encoding="utf-8")
        print('tablero:' + data)
        send_recive_data(TCPClientSocket) #Llamada de funcion que inicia la comunicacion del juego

    else:                           #Solo entra Player 1
        difficult = input(data)
        difficult = difficult.upper()
        data = str.encode(difficult)
        TCPClientSocket.sendall(data) #Envia dificultad
        send_recive_data(TCPClientSocket)





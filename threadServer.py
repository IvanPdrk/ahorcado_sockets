# !/usr/bin/env python3

import socket
import sys
import threading
import random
import time



easy = ['acosadores', 'justiciera', 'educativas', 'eclipsante',
        'danzadores', 'cabelleras', 'babilonias', 'obscuridad',
        'ochenteros','efectuamos']
hard = ['constantinopolitanos', 'carboximetilcelulosa', 'contrarevolucionaria',
           'descongestionamiento', 'electroluminiscentes', 'electronegatividades',
           'hiperlipoproteinemia', 'microemprendimientos', 'semipresidencialista',
           'superplastificadores']

word = ''
tries = 0
index = ''
indexes = ''
hidden_word = ''
tablero=''

def msg_all(mensaje):
    for c in listaConexiones:
        try:
            c.sendall(mensaje)
        except:
            listaConexiones.remove(c)

def welcome(conn):
    data = ' W E L C O M E  T O  A H O R C A D O \nDifficulty: \n [E]asy \n [H]ard \n'
    data = str.encode(data)
    conn.sendall(data)  # Send welcome message
    data = conn.recv(1024)  # Recive diffuculty answer
    data = data.decode(encoding="utf-8")
    return data

def ahorcado(conn,word):
    global index,indexes,tries,hidden_word,tablero
    while True:
        worst = 0
        data = b'\nIngresa letra\n'
        conn.sendall(data)
        print('Usuario ingresando letra...')
        data = conn.recv(1024)  # Recive new letter
        new_letter = data.decode(encoding="utf-8")  # New letter decode
        for letter in word:
            if letter == new_letter:
                index += new_letter  # Index if is in hidden word
                indexes += new_letter  # Index in string of tries
        if not index:  # Isnt the new letter
            tries += 1
            response = bytes("worst :(\n", 'ascii')  # Send answer
            conn.sendall(response)
        else:
            response = bytes("great (:\n", 'ascii')  # send answer
            conn.sendall(response)
        data = conn.recv(1024)  # respuesta confirmada
        for letter in word:
            if letter in indexes:
                hidden_word += letter + ' '
            else:
                hidden_word += '_ '
                worst += 1
        tablero = hidden_word
        table = str.encode(hidden_word)  # encode hidden_word
        conn.sendall(table)  # Send table
        print(hidden_word)  # There is the current hidden_word
        data = conn.recv(1024)  # tablero confirmado
        print(worst)
        if worst == 0:  # YOU WIN
            response = bytes("W", 'ascii')
            time.sleep(0.01)
            #conn.sendall(response)
            msg_all(response)
            return False
        if tries == 6:
            response = bytes("L", 'ascii')
            time.sleep(0.01)
            #conn.sendall(response)
            msg_all(response)
            return False
        hidden_word = ''  # reset to clean string
        index = ''  # Reset to clean index comodin


def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()   #Conexion done
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            #thread_read.join()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def recibir_datos(conn, addr):
    global tablero,word
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            if len(listaConexiones) > 1:
                data=b'P2'
                conn.sendall(data) #Send P2
                table=str.encode(tablero)
                time.sleep(0.01)
                msg_all(table) #Send table
                time.sleep(0.01)
                ahorcado(conn,word)

            else:
                data=welcome(conn)
                if data == 'E':
                    x = random.randrange(10)
                    word = easy[x]
                    ahorcado(conn,word)
                    break
                elif data == 'H':
                    x = random.randrange(10)
                    word = hard[x]
                    ahorcado(conn,word)
                    break
            if not data:
                print("Fin")
                break
            #conn.sendall(response) #Send response
    except Exception as e:
        print(e)
    finally:
        conn.close()



listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)

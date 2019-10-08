# !/usr/bin/env python3

import socket
import sys
import threading
import random
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-2s) %(message)s',
                    )


easy = ['acosadores', 'justiciera', 'educativas', 'eclipsante',
        'danzadores', 'cabelleras', 'babilonias', 'obscuridad',
        'ochenteros','efectuamos']
hard = ['constantinopolitanos', 'carboximetilcelulosa', 'contrarevolucionaria',
           'descongestionamiento', 'electroluminiscentes', 'electronegatividades',
           'hiperlipoproteinemia', 'microemprendimientos', 'semipresidencialista',
           'superplastificadores']
i=1
j=1
cola=[]
word = ''
tries = 0
index = ''
indexes = ''
hidden_word = ''
tablero=''
condition=threading.Condition()

def msg_all(mensaje):
    for c in listaConexiones:
        try:
            c.sendall(mensaje)
        except:
            listaConexiones.remove(c)

def difficult(conn):
    data = bytes("W E L C O M E  T O  A H O R C A D O\nDifficulty: \n [E]asy \n [H]ard \n", 'ascii')
    conn.sendall(data)  # Send welcome message
    data = conn.recv(1024)  # Recive diffuculty answer
    data = data.decode(encoding="utf-8")
    return data


def release(barrier):
    global cola,j
    logging.debug('Waitting Barrier')
    actual = threading.currentThread().getName()
    current=barrier.wait()
    logging.debug('Barrier release')


def define_turn(current):
    global j
    if current == str(j):
        if j==num_players:
            j=0
        return True
    else:
        return False


def ahorcado(conn,word,barrier,lock):
    global index,indexes,tries,hidden_word,tablero,j,condition
    release(barrier)
    while True:
        with condition:
            actual = threading.currentThread().getName()
            your_turn = define_turn(actual)
            if your_turn is True:
                worst = 0
                data = b'\nIngresa letra\n'
                conn.sendall(data)
                logging.debug('Usuario ingresando letra...')
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
                data = b'table'
                msg_all(data)
                time.sleep(0.2)
                msg_all(table)  # Send table
                print(hidden_word)  # There is the current hidden_word
                if worst == 0:  # YOU WIN
                    response = bytes("W", 'ascii')
                    time.sleep(0.01)
                    msg_all(response)
                    break
                if tries == 6:
                    response = bytes("L", 'ascii')
                    time.sleep(0.01)
                    msg_all(response)
                    break
                hidden_word = ''  # reset to clean string
                index = ''  # Reset to clean index comodin
                j += 1
                condition.notifyAll()
            else:
                logging.debug('Bloqueado')
                condition.wait()

def servirPorSiempre(socketTcp, listaconexiones, barrier, lock):
    global num_players,i
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()   #Conexion done
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(name=str(i) ,target=recibir_datos, args=[client_conn, client_addr, lock, barrier])
            thread_read.start()
            gestion_conexiones(listaConexiones)
            i+=1
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


def recibir_datos(conn, addr, barrier, lock):
    global tablero, word, num_players
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            if len(listaConexiones) > 1:
                data=b'P2'
                conn.sendall(data) #Send P2
                data=conn.recv(1024) #P2 confirmed
                ahorcado(conn,word,barrier,lock) #Call ahorcado
            else:
                dif = difficult(conn)   #Call Function to messages, define difficult
                if dif == 'E':
                    x = random.randrange(10)
                    word = easy[x]
                    ahorcado(conn,word,barrier,lock)
                    break
                elif dif == 'H':
                    x = random.randrange(10)
                    word = hard[x]
                    ahorcado(conn,word,barrier,lock)
                    break
            if not data:
                print("Fin")
                break
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
    num_players=input('Hoy many players do you want?')
    num_players=int(num_players)
    barrier=threading.Barrier(num_players)
    lock=threading.Lock()
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")


    servirPorSiempre(TCPServerSocket, listaConexiones, lock, barrier)

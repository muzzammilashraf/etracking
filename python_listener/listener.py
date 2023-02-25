from http import server
import socket
from _thread import *
from socket import error as SocketError
import errno
from time import *
import mysql.connector
from Parser import Parser

class Parser():
    def __inti__(self, server_data):
        pData = bytes.fromhex(server_data)
        self.preamble = pData[:4]

def threaded(sock,addr):
    dev_imei = ''
    while True:
        try:
            recv_data = sock.recv(4096)
            if recv_data == b'':
                raise Exception('Empty packet')
            try:
                recv_data_array = str(recv_data.decode())
            except UnicodeDecodeError:
                try:
                    recv_data_array = str(recv_data.decode(encoding = 'ascii'))
                except UnicodeDecodeError as e:
                    recv_data_array = recv_data.hex()
            recv_data = recv_data_array
            if (len(recv_data) == 17):
                dev_imei = recv_data[2:]
                print("IMEI:",recv_data[2:])
                reply = b'\x01'
                sock.send(reply)
            else:
                parser = Parser(dev_imei, recv_data)
                reply = parser.num_data_1.to_bytes(1, "big")
                sock.send(reply)
                for x in range(parser.num_data_1):
                    print(str(x+1) + ". IMEI = " + parser.imei)
                    print(str(x+1) + ". GPS DATA")
                    print(parser.avl_data.gpsrecords[x].__dict__)
                    print(str(x+1) + ". N1 RECORDS")
                    for y in range(0, parser.avl_data.n1records[x].num_data):
                        print(parser.avl_data.n1records[x].records[y].__dict__)
                    print(str(x+1) + ". N2 RECORDS")
                    for y in range(0, parser.avl_data.n2records[x].num_data):
                        print(parser.avl_data.n2records[x].records[y].__dict__)
                    print(str(x+1) + ". N4 RECORDS")
                    for y in range(0, parser.avl_data.n4records[x].num_data):
                        print(parser.avl_data.n4records[x].records[y].__dict__)
                    print(str(x+1) + ". N8 RECORDS")
                    for y in range(0, parser.avl_data.n8records[x].num_data):
                        print(parser.avl_data.n8records[x].records[y].__dict__)
        except socket.timeout:
            print('Timed Out!! closing connection to', addr)
            sock.close()
            break
        except OSError as e:
            print('Error other: %s' % e)
            print('closing connection to', addr)
            sock.close()
            break
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise  # Not error we are looking for
            print('closing connection to', addr)
            sock.close()
            break
        except Exception as e:
            print("in exception ignoring")
            print(e)
            print('closing connection to', addr)
            sock.close()
            break
        except KeyboardInterrupt as e:
            print(e)
            print("Keyboard interrupt exception caught")


lsock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock1.bind(('', 1237))
print("server binded to port", 1237)
lsock1.listen()
print('listening on', ('', 1237))
while True:
    try:
        c, addr = lsock1.accept()
        print('Connected to :', addr[0], ':', addr[1]) 
        start_new_thread(threaded, (c,addr,))
    except KeyboardInterrupt as e:
        lsock1.shutdown(socket.SHUT_RDWR)
        lsock1.close()
        print("\nTerminating listener")
        exit()
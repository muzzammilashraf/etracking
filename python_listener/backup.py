import socket
from _thread import *
from socket import error as SocketError
import errno

def threaded(sock,addr):
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
                print("IMEI:",recv_data[2:])
                reply = b'\x01'
                sock.send(reply)
            else:
                print(recv_data)
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
# lsock1.setblocking(False)
# lsock1.settimeout(1)
while True:
    c, addr = lsock1.accept()
    print('Connected to :', addr[0], ':', addr[1]) 
    start_new_thread(threaded, (c,addr,))
    # except KeyboardInterrupt as e:
    #     lsock1.shutdown(socket.SHUT_RDWR)
    #     lsock1.close()
    #     print("\nTerminating listener")
    #     exit()
import bluetooth
import time
import socket
import threading


TONE_1 = "01fe000053fe1a000000000000000000f00124000138000000f779"
TONE_2 = "01fe000053fe1a000000000000000000f00123010138000001f779"
TONE_3 = "01fe000053fe1a000000000000000000f00125020138000002f779"
TONE_4 = "01fe000053fe1a000000000000000000f00120030138000003f779"
tones = [TONE_1,TONE_2,TONE_3,TONE_4]



class ReceiverThread(threading.Thread):
    def __init__(self,serverSocket,clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        
    def run(self):
        msg = ''
        while True:
            data = self.csocket.recv(1)
            msg = data.decode()
            print ("from client: ", data)
                    
class SenderThread(threading.Thread):
    def __init__(self,serverSocket,clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        self.counter = 0
        
    def run(self):
        while True:
            self.counter=self.counter+1
            data= bytes(str(self.counter % 10), 'UTF-8')
            self.csocket.send(data)
            print ("to client: ", data)
            time.sleep(1)

    

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def main():
    # Then bluetooth part
    print ("Checking for bluetooth devices...")
    found = False
    while not found:
        print ("Looking for Spark")
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print ("Found {} devices.".format(len(nearby_devices)))
        for addr, name in nearby_devices:
            print("  {} - {}".format(addr, name))
            if name == "Spark 40 Audio":
                server_addr = addr
                found = True
                print ("Found Spark")
            
    print ("Connecting to {}...".format(server_addr))
    SERVER_PORT = 2

    try:
        client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        client_socket.connect((server_addr, SERVER_PORT))
        print ("Connected successfully")

        for count in range(5):
            msg = bytes.fromhex(tones[count % 4])
            client_socket.send(msg)
            time.sleep (1)

    except OSError as e:
        print(e)

    finally:
        if client_socket is not None:
            client_socket.close()

    print ("My IP: ", get_ip())

    WiFiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        WiFiSocket.bind(("192.168.1.135", 20001))
    except socket.error as msg:
        print ("Bind failed ", msg[0], msg[1])
        sys.exit()
    
    WiFiSocket.listen(5)
    print ("Waiting")
    clientsock, clientaddress = WiFiSocket.accept()
    print ("Connected from", clientaddress)

    while True:
        sendThread = SenderThread(clientsock, clientsock)
        recvThread = ReceiverThread(clientsock, clientsock)
        sendThread.start()
        recvThread.start()
        sendThread.join()
        recvThread.join()
    
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    #print ("Received something")
    #msg = clientsocket.recv(10)
    #print (msg)
    #clientsocket.send(bytes("Thanks",'utf-8'))

if __name__ == "__main__":
        main()
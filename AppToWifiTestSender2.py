import time
import socket


#s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("192.168.1.135",20000))
#s.connect(("localhost",20000))
count = 0
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.135",20001))
    
while True:
    # accept connections from outside
#    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.connect(("192.168.1.135",20001))
    msg = bytes("Hello" + str(count), 'utf-8')
    s.send(msg)
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    print ("Sent something ", count)
    msg2=s.recv(1)
    print (msg2)
    count=count+1
#    s.close()
    time.sleep(1)
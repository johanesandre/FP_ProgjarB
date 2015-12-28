import sys
import socket
import io
import threading
import Queue


HOST, PORT = '', 8889
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the port
port = int(sys.argv[1])
sock.bind((HOST,port))
sock.listen(1)
print 'starting up on port %s' % port
# sock.bind(server_address)

class serverThread(threading.Thread):
  def __init__(self, conn, client_addr, client_data):
    threading.Thread.__init__(self)
    self.conn = conn
    self.client_addr = client_addr
    self.client_data = client_data
    
  def run(self):
    print "start client data"
    print self.client_data
    print "end client data"
    filename = self.client_data.split()
    print filename
    
    file1 = filename[1]      
    file2 = file1[1:]
    f=open(file2+".png",'r+')
    jpgdata2 = f.read()
    f.close()
    http_response = "\HTTP/1.1 200 OK \n\n%s"%jpgdata2
    self.conn.sendall(http_response)
    self.conn.close()
    return

# Listen for incoming connections

clientQueue = Queue.Queue(maxsize=1000)
threads = []
jumlahClient = 0

while True:
    	# Wait for a connection
    	# print >>sys.stderr, 'waiting for a connection'
    	conn, client_address = sock.accept()
    	clientQueue.put(conn)
	data = clientQueue.get().recv(1024)
	
	if not data:
	  data = "GET /image4 HTTP/1.1"
	  
	serverWorker = serverThread(conn, client_address, data)
	serverWorker.start()
	  
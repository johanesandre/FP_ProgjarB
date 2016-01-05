import sys
import socket
import io
import threading
import Queue
import os

sys.setrecursionlimit(100000)


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
  def __init__(self, clientQueue):
    threading.Thread.__init__(self)
    self.clientQueue = clientQueue
    
  def run(self):
    global clientQueue
    
    self.conn = clientQueue.get(True)
    self.client_data = self.conn.recv(1024)
    if not self.client_data:
      self.client_data = "GET /image4 HTTP/1.1"
    print "start client data"
    print self.client_data
    print "end client data"
    self.filename = self.client_data.split()
    print self.filename
    
    self.file1 = self.filename[1]      
    self.file2 = self.file1[1:]
    self.file2+=".png"
    
    if os.path.isfile(self.file2):
      self.f=open(self.file2,'r+')
    else:
      self.f=open("not-found.png",'r+')
      
    self.jpgdata2 = self.f.read()
    self.f.close()
    self.http_response = "\HTTP/1.1 200 OK \n\n%s"%self.jpgdata2
    self.conn.sendall(self.http_response)
    self.conn.close()
    self.clientQueue.task_done()
    self.run()

# Listen for incoming connections
def main():
  global clientQueue
  
  clientQueue = Queue.Queue()
  threads = []
  jumlahClient = 0
  for x in range(10):
	    serverWorker = serverThread(clientQueue)
	    serverWorker.daemon = True
	    serverWorker.start()
  while True:
	  # Wait for a connection
	  # print >>sys.stderr, 'waiting for a connection'
	  
	  
	  conn, client_address = sock.accept()
	  jumlahClient+=1
	  clientQueue.put(conn)
	  #if jumlahClient == 10:
	    #serverWorker.join()
	    #jumlahClient=0
	  clientQueue.join()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print 'Quited'
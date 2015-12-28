import socket
import threading
import logging
import time
import sys
import os
from time import time
import subprocess
import Queue

HOST = ''
PORT = 8018
WJUMLAHKONEKSI = 0.3
WRESPONTIME = 0.5

class connectToServer(threading.Thread):
  def __init__(self, conn, data):
    threading.Thread.__init__(self)
    self.connClient = conn
    self.sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.dataClient = data
  
  def run(self):
    global servers
    
    print self.dataClient
    print "selesai print data"
    self.calculateResponTime()
    print "selesai calculateResponTime"
    self.giliran = self.calculateTurn()
    print "selesai calculateTurn"
    print servers[self.giliran].getAll()[0]
    print servers[self.giliran].getAll()[1]
    servers[self.giliran].setJumlahKoneksi(+1)
    print servers[self.giliran].getAll()[3]
    
    print "masuk run connectToServer"
    #self.sockServer.connect((servers[self.giliran].getAll()[0], servers[self.giliran].getAll()[1]))
    #self.sockServer.sendall(self.dataClient)
    print "waiting for incoming data"
    #self.dataServer = self.sockServer.recv(10000000)
    print "receiving incoming data and sending"
    #self.connClient.sendall(self.dataServer)
    print "end run connectToServer"
    self.TARGET = "http://" + str(servers[self.giliran].getAll()[0]) +  ":" + str(servers[self.giliran].getAll()[1]) + str(self.dataClient.split()[1])
    print self.TARGET
    self.sendline("HTTP/1.1 302 Found")
    self.sendline("Location: " + self.TARGET)
    self.sendline("Connection: close")
    self.sendline("Cache-control: private")
    self.sendline("")
    self.sendline("<html><body>Encryption Required.  Please go to <a href='" + self.TARGET + "'>" + self.TARGET + "</a> for this service.</body></html>")
    self.sendline("")
    
    self.connClient.close()
    #self.sockServer.close()
    servers[self.giliran].setJumlahKoneksi(-1)
    #thread.exit()
    return
  
  def sendline(self, data):
    print "lala"
    self.connClient.send(data+"\r\n")
  
  def calculateTurn(self):
    global servers
    global jumlahServer
    hasil = 0
    print "masuk calculateTurn"
    print hasil
    print jumlahServer
    for indeks in range(1,jumlahServer):
      #print indeks
      #data1 = servers[indeks].getAll()[2]*WRESPONTIME + servers[indeks].getAll()[3]*WJUMLAHKONEKSI
      #print "data 1 : "
      #rint data1
      #data2 = servers[hasil].getAll()[2]*WJUMLAHKONEKSI + servers[indeks].getAll()[3]*WRESPONTIME
      #print "data 2 : "
      #print data2
      if ((servers[indeks].getAll()[2]*WRESPONTIME + servers[indeks].getAll()[3]*WJUMLAHKONEKSI)) < ((servers[hasil].getAll()[3]*WJUMLAHKONEKSI + servers[hasil].getAll()[2]*WRESPONTIME)):
	hasil = indeks
	print hasil
    
    print "keluar for"
    return hasil

  def calculateResponTime(self):
    global servers
    global jumlahServer
    
    #print 'calculate respon time'
    #print server
    for indeks in range(0, jumlahServer):
      timeString = [line.rpartition('=')[-1] for line in subprocess.check_output(['ping', '-c', '1','-p',str(servers[indeks].getAll()[1]), servers[indeks].getAll()[0]]).splitlines()[2:-4]]
      time = float(timeString[0].split(' ',1)[0])
      servers[indeks].setResponTime(time)
    return

class server(threading.Thread):
  def __init__(self, ip, port):
    threading.Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.responTime = 0
    self.jumlahKoneksi = 0
    
  def getAll(self):
    return [self.ip, self.port, self.responTime, self.jumlahKoneksi]
  
  def setResponTime(self, responTime):
    self.responTime = responTime
  
  def setJumlahKoneksi(self, koneksi):
    self.jumlahKoneksi = self.jumlahKoneksi+koneksi


clientQueue = Queue.Queue(maxsize=1000)

def main():
  global servers
  global jumlahServer
  
  servers = {}
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((HOST, PORT))
  sock.listen(100000)
  jumlahServer = int(raw_input('Jumlah server : '))
  #print jumlahServer
  #print type(HOST)
  #print type(PORT)
  
  for indeks in range(0, jumlahServer):
    ip = raw_input('IP Server %s : ' % indeks)
    port = int(raw_input('Port Server %s : ' % indeks))
    servers[indeks] = server(ip, port)
    servers[indeks].start()
    print servers[indeks]
    
  while 1:
    try:
      print 'waiting connection'
      conn, addr = sock.accept()
      clientQueue.put(conn)
      print 'connected from conn %s ip %s' %(conn, addr)
      print type(conn)
      print type(addr)
      data = clientQueue.get().recv(4096)
      beginServer = connectToServer(conn, data)
      print "lala"
      beginServer.start()
      print "yeye"
      
    except:
      sys.exit()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print 'Quited'
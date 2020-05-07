import socket
import threading

class clientsocket:
    def __init__(self):
        self.header=64
        self.port=5055
        self.format='utf-8'
        self.hostname=socket.gethostname()
        self.host=socket.gethostbyname(self.hostname)
        self.close='close'
        self.addr=(self.host,self.port)
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.mesrec=[]
        self.messend=[]
        self.client.connect(self.addr)
    def addlist(self,msg):
        self.messend.append(msg)
        return None
    def connect(self):
        
        thread1=threading.Thread(target=self.send)
        thread2=threading.Thread(target=self.recv)
        thread1.start()
        thread2.start()
    def send(self):
        print('thead2')
        que=0
        while True:
            tmp=[]
            if(len(self.messend)>que):
                tmp=self.messend[que:]
                for msg in tmp:
                    message=msg.encode(self.format)
                    msglen=len(message)
                    sendlen=str(msglen).encode(self.format)
                    sendlen += b' '*(self.header-len(sendlen))
                    self.client.send(sendlen)
                    self.client.send(message)
                    print("sent: ",message)
                    que=len(self.messend)
    def recv(self):
        print('thread 1')
        while True:
            msglen=self.client.recv(self.header).decode(self.format)
            if msglen:
                msglen=int(msglen)
                msg =self.client.recv(msglen).decode(self.format)
            self.mesrec.append(msg)
            print("received: ",msg)
    
           
       
k=clientsocket()
def connectthread():
    k.connect()
def sendthread():
    msg='client'
    k.addlist(msg)
    
connectthread=threading.Thread(target=connectthread)
sendthread=threading.Thread(target=sendthread)
connectthread.start()
sendthread.start()
import socket
import threading

class seversocket:
    def __init__(self):
        self.header=64
        self.port=5055
        self.format='utf-8'
        self.hostname=socket.gethostname()
        self.host=socket.gethostbyname(self.hostname)
        self.close='close'
        self.messagelist=['world']
        self.addr=(self.host,self.port)
        self.soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soc.bind(self.addr)
        print('server socket created and binded;')
        self.listener()
    def messageupdate(self,msgcount):
       
        result_list=[]
        if(len(self.messagelist)>msgcount):
            result_list=self.messagelist[msgcount:]
            return result_list,len(self.messagelist)
        else:
            return None,msgcount



    def clients(self,conn,addr):
        print(f'connected to {addr}')
        connected=True
        msgcount=0
        while connected:
            msglen=conn.recv(self.header).decode(self.format)
            if msglen:
                msglen=int(msglen)
                msg = conn.recv(msglen).decode(self.format)
                if msg == self.close:
                    connected=False
                print(f"[{addr}]{msg}")
            li,msgcount= self.messageupdate(msgcount)
            if li is not None:
                for i in li:
                    print(i)                    
                    message=i.encode(self.format)
                    print(message)
                    msglen=len(message)
                    print(msglen)
                    sendlen=str(msglen).encode(self.format)
                    sendlen += b' '*(self.header-len(sendlen))
                    conn.send(sendlen)
                    conn.send(message)
            

               
        conn.close()
         
    def listener(self):
        self.soc.listen()
        print(f'socket is listening to {self.host}')
        while True:
            conn,addr=self.soc.accept()
            thread=threading.Thread(target=self.clients,args=(conn,addr))
            thread.start()
    def listappened(self,mes):
        self.messagelist.append(mes)
        return None
    

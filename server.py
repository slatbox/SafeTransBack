import socket
import ssl
import threading
from protocal import Proto
from database import UserDB
import os
class Server:
    
    def __init__(self) -> None:
        pass
    def start(self):
        HOST = 'localhost'
        PORT = 8889
        CERT_FILE = 'keys/server.crt'
        KEY_FILE = 'keys/server.key'
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print('Server listening on {}:{}'.format(HOST, PORT))
        
        while True:
            # 接收客户端连接
            client_socket, client_address = server_socket.accept()
            print('Accepted connection from {}:{}'.format(client_address[0], client_address[1]))
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                # 加载服务器所用证书和私钥
            context.load_cert_chain(CERT_FILE, KEY_FILE)
            tunnel = context.wrap_socket(client_socket, server_side=True)
            self.tunnel = tunnel
            client_thread = threading.Thread(target=Server.handle_client, args=(self,tunnel,))
            client_thread.start()
    
    def signUp(self,user_name,password):
        self.db.createUser(user_name,password)
        
    def login(self,data):
        info = data.decode('utf-8')
        user_name,password= info.split(',')
        result = self.db.verify(user_name,password)
        falg = Proto.STATE_SUCCESS if result == True else Proto.STATE_FAIL
        rep = Proto.createReq(falg,b'')
        self.tunnel.send(rep)
        
    def get_file_list(self):
        file_list = os.listdir('storage')
        rep = Proto.createReq(Proto.STATE_SUCCESS,','.join(file_list).encode())
        self.tunnel.send(rep)
    
    def download(self,file_name):
        cmd_size = Proto.getCmdLen()
        file_size = os.path.getsize('storage/' + file_name)
        self.tunnel.send(Proto.createReq(Proto.STATE_DOWN_START,str(file_size).encode()))
        with open('storage/'+ file_name,'rb') as f:
            while True:
                content = f.read(1024 - cmd_size)
                state = Proto.STATE_SUCCESS if file_size > 1024 - cmd_size else Proto.STATE_END
                rep = Proto.createReq(state,content)
                self.tunnel.send(rep)
                file_size -= len(content)
                if file_size <= 0:
                    break
    
    def upload(self,file_name):
        cur_len = 0
        self.tunnel.send(Proto.createReq(Proto.STATE_SUCCESS,b''))
        with open('storage/'+file_name,'wb') as f:
            while True:
                state,data = Proto.unpack(self.tunnel.recv())
                f.write(data)
                cur_len += len(data)
                if state == Proto.CMD_UPLOAD_END:
                    break
    def handle_client(self,tunnel):
        self.db = UserDB('users.db')
        while True:
            req = tunnel.recv()
            header,data = Proto.unpack(req)
            if header == Proto.CMD_LOGIN:
                self.login(data)
            elif header == Proto.CMD_CLOSE:
                tunnel.close()
            elif header == Proto.CMD_GET_FILE_LIST:
                self.get_file_list()
            elif header == Proto.CMD_DOWNLOAD:
                self.download(data.decode())
            elif header == Proto.CMD_UPLOAD:
                self.upload(data.decode())
            # if data:
            #     print('Received: ', data.decode('utf-8'))
            #     response = 'Message received: ' + data.decode('utf-8')
            #     ssl_client.send(response.encode('utf-8'))
            # else:
            #     break
        

    

if __name__ == '__main__':
    server = Server()
    server.start()

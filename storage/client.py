import socket
import ssl
from protocal import Proto
from OpenSSL import crypto
import os

class Client:
    def __init__(self) -> None:
        self.HOST = 'localhost'
        self.PORT = 8889
        self.CERT_FILE = 'keys/client.crt'
        self.CA_CERT_FILE = 'keys/ca.crt'
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        with open(self.CA_CERT_FILE, 'rb') as f:
            ca_cert_data = f.read()
            # ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert_data)
            context.load_verify_locations(cafile=self.CA_CERT_FILE)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_client = ssl.wrap_socket(client_socket)
        ssl_client.connect((self.HOST, self.PORT))
        print('Connected to {}:{}'.format(self.HOST,self.PORT))
        self.client = ssl_client
        
    def send(self,byte_data):
        self.client.send(byte_data) 
        reply = self.client.recv(1024)
        header,info = Proto.unpack(reply)
        return header,info
    
    def recv(self):
        reply = self.client.recv(1024)
        header,info = Proto.unpack(reply)
        
        return header,info
    def login(self,username,password):
        data = username + ',' + password
        req = Proto.createReq(Proto.CMD_LOGIN,data.encode())
        state,info = self.send(req)
        if state == Proto.STATE_SUCCESS:
            return True
        else:
            return False
    
    def getFileList(self):
        req = Proto.createReq(Proto.CMD_GET_FILE_LIST,b'')
        state,info = self.send(req)
        return info.decode()
    def download(self,file_name):
        req = Proto.createReq(Proto.CMD_DOWNLOAD,file_name.encode())
        state,info = self.send(req)
        return state,info.decode()
    
    def cd(path):
        pass

# 发送数据给服务器

# client = Client()

# while True:
    # message = input('输入：')
    # print(client.login('admin','82819639'))
# print(client.getFileList())
    # print('Received from server: ', data.decode('utf-8'))


# 关闭SSL客户端socket
# client.close()

#coding:utf8
import socket

def listen():
    addr = ('',5000)
    sok = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sok.bind(addr)
    sok.listen(1024)
    sok.settimeout(30)
    while True:
        try:
            print ('waiting for connection......')
            des,ip = sok.accept()
            print(des)
            print(ip)
            print ('connection for',ip)
            while True:
                data = des.recv(1024).decode()
                print(ip[0],"说:",data)
                des.send(data.encode())
        except Exception as e:
            print(e)
listen()
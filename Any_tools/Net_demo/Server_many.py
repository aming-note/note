#coding:utf8
import socketserver,time,platform,psutil
from socketserver import StreamRequestHandler as SRH
import os
class physical_info():
    os_type = platform.system()
    cpu_count = psutil.cpu_count()
    cpu_version = platform.processor()
    if os_type == 'Windows':
        os_info = platform.version()
        mem_total = "%.2f" % (psutil.virtual_memory().total /1024 /1024 /1024)
        mem_used = "%.2f" % (psutil.virtual_memory().used /1024 /1024 /1024)
        mem_free = "%.2f" % (psutil.virtual_memory().free /1024 /1024 /1024)
        swap_total = "%.2f" % (psutil.swap_memory().total /1024 /1024 /1024)
        swap_used = "%.2f" % (psutil.swap_memory().used /1024 /1024 /1024)
        swap_free = "%.2f" % (psutil.swap_memory().free /1024 /1024 /1024)
    elif os_type == 'Linux':
        os_info = platform.platform()
        mem_total = psutil.virtual_memory().total / 1024 / 1024
        mem_used = psutil.virtual_memory().used / 1024 / 1024
        mem_free = psutil.virtual_memory().free / 1024 / 1024
        swap_total = psutil.swap_memory().total / 1024 / 1024
        swap_used = psutil.swap_memory().used / 1024 / 1024
        swap_free = psutil.swap_memory().free / 1024 / 1024

class MasterServer(SRH):
    print ('wait for connection...')
    def handle(self):
        try:
            print ('connection form',self.client_address[0])
            verify = 'Success Receive Your Connect'
            self.request.send(verify.encode())
            while True:
                time.sleep(0.1)
                data = self.request.recv(1024)
                print (self.client_address[0], ':', data.decode())
                if data.decode() == 'get_os_type':
                    rese = physical_info.os_type
                    self.request.send(str(rese).encode())
                elif data.decode() == 'get_os_info':
                    rese = physical_info.os_info
                    self.request.send(str(rese).encode())
                elif data.decode() == 'get_cpu_count':
                    rese = physical_info.cpu_count
                    self.request.send(str(rese).encode())
                elif data.decode() == 'get_cpu_version':
                    rese = physical_info.cpu_version
                    self.request.send(str(rese).encode())
                elif data.decode() == 'get_mem_total':
                    rese = physical_info.mem_total
                    self.request.send(str(rese).encode())
                elif data.decode() == 'get_mem_used':
                    rese = physical_info.mem_used
                    self.request.send(str(rese).encode())
                elif data.decode() == 'get_mem_free':
                    rese = physical_info.mem_free
                    self.request.send(str(rese).encode())
                else:
                    try:
                        os.system(data.decode())
                        info = '执行成功'
                        self.request.send(info.encode())
                    except Exception as e:
                        info = '命令执行错误:' + str(e)
                        self.request.send(info.encode())
        except:
            print (self.client_address[0],'initiative close connect')
            print ('waiting for connection...')
if __name__ == '__main__':
    addr = ('',6666)
    server = socketserver.ThreadingTCPServer(addr,MasterServer)
    server.serve_forever()

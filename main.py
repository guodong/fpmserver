import socket
import fpm_pb2 as fpm

addr = ('127.0.0.1', 26200)
s = socket.socket()
s.bind(addr)
s.listen(10)
while True:
    conn, addr = s.accept()
    print("new conn")
    data = b''
    while True:
        data += s.recv(1000)
        m = fpm.Message()
        m.ParseFromString(data)
        print(m.type)
    conn.close()
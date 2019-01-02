import socket
import fpm_pb2 as fpm

addr = ('127.0.0.1', 26200)
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(10)
while True:
    conn, addr = s.accept()
    print("new conn")
    data = b''
    while True:
        data += conn.recv(1000)
        m = fpm.Message()
        m.ParseFromString(data)
        print(m.type)
        if m.type == fpm.Message.ADD_ROUTE:
            print("add route")
        elif m.type == fpm.Message.REMOVE_ROUTE:
            print("remove route")
        else:
            conn.close()

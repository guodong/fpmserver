import socket
import struct
from pyroute2 import IPDB
import fpm_pb2 as fpm

ip = IPDB()
print ip.by_name.keys()
print ip.by_index.keys()

addr = ('127.0.0.1', 2620)
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(10)
while True:
    conn, addr = s.accept()
    print("new conn")

    while True:
        data = conn.recv(4)
        d = bytearray(data)
        x, y, size = struct.unpack(">ccH", d)
        print(size)
        body = conn.recv(size - 4)
        m = fpm.Message()
        m.ParseFromString(body)
        print(m)
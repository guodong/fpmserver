import socket
import array
import struct
import os
import netifaces
import fpm_pb2 as fpm

ifaces = netifaces.interfaces()


# fpm nexthop interface id to ovs port id, eg: 9 -> 0 means #9 is i0, i0 -> eth0, eth0 -> of port 1
def ifIdtoPortId(ifId):
    iface = ifaces[ifId - 1]
    idx = iface[1:]
    if idx == 'o':
        return None
    return int(idx) + 1


def add_flow(dst, output):
    cmd = 'ovs-ofctl add-flow s table=100,ip,nw_dst=' + dst + ',actions=output:' + output
    print cmd
    os.system(cmd)


def bytes2Ip(bts):
    for i in range(len(bts), 4):
        bts += '\0'

    return '.'.join("{:d}".format(ord(x)) for x in bts)


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
        body = conn.recv(size - 4)
        m = fpm.Message()
        m.ParseFromString(body)
        print(m)
        if m.add_route:
            dst = bytes2Ip(m.add_route.key.prefix.bytes) + '/' + str(m.add_route.key.prefix.length)
            output = ifIdtoPortId(m.add_route.nexthops[0].if_id.index)
            if output is not None:
                add_flow(dst, str(output))

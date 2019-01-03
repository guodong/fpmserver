#!/usr/bin/python
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI


class NetworkTopo(Topo):
    def build(self, **opts):
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.1.1/24')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s2')

        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)
        self.addLink(s3, h2)


if __name__ == "__main__":
    setLogLevel("info")
    topo = NetworkTopo()
    net = Mininet(controller=RemoteController, topo=topo)
    net.start()
    CLI(net)
    net.stop()

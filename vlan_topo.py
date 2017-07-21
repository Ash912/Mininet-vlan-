#!/usr/bin/python

#from mininet.net import Mininet
from mininet.net import Containernet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.node import Docker
from mininet.link import Link, TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def topo():

    net = Containernet(controller = RemoteController, link=TCLink, switch=OVSKernelSwitch)
    info("*** Adding Controller ")
    c1 = net.addController('c1', ip='127.0.0.1',port=6633)
    info('*** Adding Switch')
    s2 = net.addSwitch('s2', protocols='OpenFlow10',listenPort=6670,mac='00:00:00:00:00:02')
    s3 = net.addSwitch('s3', protocols='OpenFlow10',listenPort=6671,mac='00:00:00:00:00:03')

    info('*** Adding Docker Containers')
    d4 = net.addDocker('d4',mac='00:00:00:00:00:04', ip='10.0.20.3/24',dimage="ubuntu:trusty", cpu_period=50000, cpu_quota=25000)
    d5 = net.addDocker('d5',mac='00:00:00:00:00:05', ip='10.0.10.3/24',dimage="ubuntu:trusty", cpu_period=50000, cpu_quota=25000)
    d6 = net.addDocker('d6',mac='00:00:00:00:00:06', ip='10.0.10.2/24',dimage="ubuntu:trusty", cpu_period=50000, cpu_quota=25000)
    d7 = net.addDocker('d7',mac='00:00:00:00:00:07', ip='10.0.20.2/24',dimage="ubuntu:trusty", cpu_period=50000, cpu_quota=25000)

    info('*** Adding links ')
    net.addLink(d4, s2, cls=TCLink, delay="5ms", bw=1, loss=0)
    net.addLink(d6, s2, cls=TCLink, delay="10ms", bw=10, loss=0)
    net.addLink(d7, s3, cls=TCLink, delay="5ms", bw=1, loss=0)
    net.addLink(d5, s3, cls=TCLink, delay="10ms", bw=10, loss=0)
    net.addLink(s2, s3, cls=TCLink, delay="100ms", bw=1, loss=0)

    info('*** Starting ')
    net.build()
    c1.start()
    s3.start([c1])
    s2.start([c1])

    CLI(net)
    net.stop()


if __name__=='__main__':
    setLogLevel('info')
    topo()

#Name: legacyrouter.py
#Author(s):Jose Crescencio, Judith Ramirez
#Date: April 12, 2019
#Description: This program forwards packets between two hosts(h1,h2) using subnets

#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.topo import Topo

#Function where evrything happens
def myNetwork():

    defaultIP = '192.168.1.1/24'

    net = Mininet( topo= None,
                   build=False,
                   ipBase=defaultIP)
    
    #Creating switches
    s1, s2, s3 = [ net.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

    info( '*** Adding controller\n' )
    
    #Creating the router "r1" and starting the process of forwarding
    info( '*** Add switches\n')
    r1 = net.addHost('r1', cls=Node,ip= defaultIP)
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    #Creation of two hosts "h1,h2" with different IP addresses and default routes
    #becauce they are in different subnets
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.100/24',defaultRoute='via 192.168.1.1')
    h2 = net.addHost('h2', cls=Host, ip='172.16.0.100/12',defaultRoute='via 172.16.0.1')

    #Giving the hosts interfaces
    info( '*** Add links\n')
    net.addLink(h1, r1, intfName2='r0-eth0',params2={ 'ip' : defaultIP})
    net.addLink(h2, r1, intfName2='r0-eth1',params2={ 'ip' : '172.16.0.1/12'})

    #The network starts building
    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
    
    #Mapping the switches to the host
    info( '*** Starting switches\n')
    for h, s in [ (h1, s1), (h2, s2)]:
        net.addLink(h,s)

    info( '*** Post configure switches and hosts\n')

    #Starting the promt
    CLI(net)
    net.stop()

if __name__ == '__main__':
    #Program starts here
    setLogLevel( 'info' )
    #Function where everything happens is called
    myNetwork()


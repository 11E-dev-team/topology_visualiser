import operations as op
def test1():
    pxp = op.start_telnet("172.23.201.115", "32792")
    data = op.get_neig_data(pxp)
    print (data)
    print (op.match_neighbors(data))

def test2 ():
    out = ("""
        Device ID: Client1
        Entry address(es): 
        IP address: 192.168.0.10
        Platform: Linux Unix,  Capabilities: Router Source-Route-Bridge 
        Interface: Ethernet0/1,  Port ID (outgoing port): Ethernet0/0
        Holdtime : 166 sec

        Version :
        Cisco IOS Software, Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.7(3)M2, DEVELOPMENT TEST SOFTWARE
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Wed 28-Mar-18 11:18 by prod_rel_team

        advertisement version: 2
        Management address(es): 
        IP address: 192.168.0.10

        -------------------------
        Device ID: client3
        Entry address(es): 
        IP address: 192.168.0.3
        Platform: Linux Unix,  Capabilities: Router Source-Route-Bridge 
        Interface: Ethernet0/2,  Port ID (outgoing port): Ethernet0/0
        Holdtime : 177 sec

        Version :
        Cisco IOS Software, Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.7(3)M2, DEVELOPMENT TEST SOFTWARE
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Wed 28-Mar-18 11:18 by prod_rel_team

        advertisement version: 2
        Management address(es): 
        IP address: 192.168.0.3

        -------------------------
        Device ID: Router
        Entry address(es): 
        IP address: 192.168.0.1
        Platform: Linux Unix,  Capabilities: Router Source-Route-Bridge 
        Interface: Ethernet0/0,  Port ID (outgoing port): Ethernet0/0
        Holdtime : 155 sec

        Version :
        Cisco IOS Software, Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.7(3)M2, DEVELOPMENT TEST SOFTWARE
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Wed 28-Mar-18 11:18 by prod_rel_team

        advertisement version: 2
        Management address(es): 
        IP address: 192.168.0.1

        -------------------------
        Device ID: SW2
        Entry address(es): 
        IP address: 192.168.0.8
        Platform: Linux Unix,  Capabilities: Router Switch IGMP 
        Interface: Ethernet0/3,  Port ID (outgoing port): Ethernet0/1
        Holdtime : 150 sec

        Version :
        Cisco IOS Software, Linux Software (I86BI_LINUXL2-ADVENTERPRISEK9-M), Version 15.2(CML_NIGHTLY_20180510)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  V152_6_0_81_E
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Thu 10-May-18 02:45 by mmen

        advertisement version: 2
        VTP Management Domain: 'VLANchiki'
        Native VLAN: 1
        Duplex: full
        Management address(es): 
        IP address: 192.168.0.8

        """)
    
from topology_visualizer import visualize_topolgy

d = {("R4", "Eth0/1"): ("R5", "Eth0/1"),
    ("R4", "Eth0/2"): ("R6", "Eth0/0"),}
def test3 (d):
    visualize_topolgy(d)
    
test3(d)


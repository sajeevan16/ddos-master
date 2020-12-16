import socket
import struct
from scapy.all import *
#from dpkt import ip


from netfilterqueue import NetfilterQueue

def ip_to_string(ip):
        return ".".join(map(lambda n: str(ip>>n & 0xff), [24,16,8,0]))

def print_and_accept(pkt):
    #print(pkt)
    
    pl = pkt.get_payload()
    
    packIP = IP(pl)
    packEth = Ether(pl)
    
    print (packIP.show())
    print (packEth.show())
    
    #print (packIP.summary())
    
    if IP in packIP:
        ip_src=packIP[IP].src
        ip_dst=packIP[IP].dst
        
        #print " IP src " + str(ip_src)
        #print " IP dst " + str(ip_dst) 
        
        
    if TCP in packIP:
        tcp_sport=packIP[TCP].sport
        tcp_dport=packIP[TCP].dport
        
        #print " TCP sport " + str(tcp_sport)
        #print " TCP dport" + str(tcp_dport) 
        
    
        
    pkt.accept()
    #pkt.drop()
    
    
    
    
    #src_ip = struct.unpack('>I', pl[12:16])[0]
    #tcp_offset = (struct.unpack('>B', pl[0:1])[0] & 0xf) * 4
    #tmp = struct.unpack('>B', pl[tcp_offset+12:tcp_offset+13])[0]
    #data_offset = ((tmp & 0xf0) >> 4) * 4
    #src_port = struct.unpack('>H', pl[tcp_offset+0:tcp_offset+2])[0]
    #data = pl[tcp_offset + data_offset:]
    #print 'from {}:{}, "{}"'.format(ip_to_string(src_ip), src_port, data)
    

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)

try:
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('KeyboardInterrupt')
    os.system('iptables -F')

s.close()
nfqueue.unbind()

# import nfqueue
import socket
import struct
from scapy.all import *
from dpkt import ip
from netfilterqueue import NetfilterQueue
import socket
from environment import Environment
import learning, nn

# $ sudo iptables -A INPUT -j NFQUEUE --queue-num 1
# $ sudo python3 packet_mangling.py
# $ sudo iptables -F

env = Environment()
nn_param = [128, 128]
params = {
    "batchSize": 64,
    "buffer": 50000,
    "nn": nn_param
}

model = nn.neural_net(learning.NUM_INPUT, nn_param)

learning_train = learning.train_net(model, params, env, "modelname")

def analyzer(pkt):
    global env,learning_train
    env.setState([3,46,64])
    
    # GET FEATURES
    
    pkt_pl = pkt.get_payload()
    state = []
    packIP = IP(pkt_pl)
    packEth = Ether(pkt_pl)

    # print("######## packIP.show() Start ###########")
    # print (packIP.show())
    # print("######## packEth.show() Start ###########")
    # print (packEth.show())
    # print("######## End ###########")
    state.append(0)
    env.setState(state)
    # RL 
    true = next(learning_train)
    res = next(learning_train)
    print(true,res)
    if (res == 1):
        pkt.accept()
        #pkt.drop()
    else:
        pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, analyzer)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)

try:
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('KeyboardInterrupt')

s.close()
nfqueue.unbind()

###################################################


# def ip_to_string(ip):
#         return ".".join(map(lambda n: str(ip>>n & 0xff), [24,16,8,0]))

# def analyzer(pkt):
#     #print(pkt)
    
#     pl = pkt.get_payload()
    
#     packIP = IP(pl)
#     packEth = Ether(pl)
    
#     print (packIP.show())
#     print (packEth.show())
    
#     #print (packIP.summary())
    
#     if IP in packIP:
#         ip_src=packIP[IP].src
#         ip_dst=packIP[IP].dst
        
#         #print " IP src " + str(ip_src)
#         #print " IP dst " + str(ip_dst) 
        
        
#     if TCP in packIP:
#         tcp_sport=packIP[TCP].sport
#         tcp_dport=packIP[TCP].dport
        
#         #print " TCP sport " + str(tcp_sport)
#         #print " TCP dport" + str(tcp_dport) 
        
    
        
#     pkt.accept()
#     #pkt.drop()
    
    
    
    
#     #src_ip = struct.unpack('>I', pl[12:16])[0]
#     #tcp_offset = (struct.unpack('>B', pl[0:1])[0] & 0xf) * 4
#     #tmp = struct.unpack('>B', pl[tcp_offset+12:tcp_offset+13])[0]
#     #data_offset = ((tmp & 0xf0) >> 4) * 4
#     #src_port = struct.unpack('>H', pl[tcp_offset+0:tcp_offset+2])[0]
#     #data = pl[tcp_offset + data_offset:]
#     #print 'from {}:{}, "{}"'.format(ip_to_string(src_ip), src_port, data)
    

# nfqueue = NetfilterQueue()
# nfqueue.bind(1, analyzer)
# s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)

# try:
#     nfqueue.run_socket(s)
# except KeyboardInterrupt:
#     print('KeyboardInterrupt')
#     os.system('iptables -F')

# s.close()
# nfqueue.unbind()
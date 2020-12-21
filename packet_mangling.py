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

# TCP-Flags

TCP_FLAGS = {
    'FIN': 0x01,
    'SYN': 0x02,
    'RST': 0x04,
    'PSH': 0x08,
    'ACK': 0x10,
    'URG': 0x20,
    'ECE': 0x40,
    'CWR': 0x80,
}


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
    
    
    # GET FEATURES

    
    ###################################packEth = Ether(pkt_pl)
    # print("######## packIP.show() Start ###########")
    # print (packIP.show())
    # print("######## packEth.show() Start ###########")
    # print (packEth.show())
    # print("######## End ###########")

    print("YYYYYYYYYYYYYYYYYYYY")
    pkt_pl = pkt.get_payload()
    scapktIP = IP(pkt_pl)
    print()
    if scapktIP.haslayer(TCP) and (scapktIP[TCP].flags & TCP_FLAGS['SYN']):
        print("Connection Estalishment.... ")

        #Feature selection
        state = []
        state.append(0)
        state.append(0)
        state.append(0)
        env.setState(state)
        # RL 
        true = next(learning_train)
        res = next(learning_train)
        print(true,res)
        if (res == 1):
            #pkt.accept()
            pkt.drop()
        else:
            pkt.drop()
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
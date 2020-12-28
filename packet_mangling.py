# import nfqueue

from scapy.all import *
from dpkt import ip
from netfilterqueue import NetfilterQueue
from environment import Environment
import learning, nn, settings
import os, netifaces, socket, struct




settings.init_interface()




env = Environment()
nn_param = [128, 128]

params = {
    "batchSize": 64,
    "buffer": 50000,
    "nn": nn_param
}

model = nn.neural_net(learning.NUM_INPUT, nn_param)

learning_train = learning.train_net(model, params, env, "modelname")

def send_403(pkt):
    # pkt[SYN]
    pkt[IP].src,pkt[IP].dst =  pkt[IP].dst , pkt[IP].src
    pkt[TCP].sport,pkt[TCP].dport=pkt[TCP].dport,pkt[TCP].sport
    pkt[TCP].flags='RST'
    
    send(pkt)

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
    if scapktIP.haslayer(TCP) and (scapktIP[TCP].flags & settings.TCP_FLAGS['SYN']):
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
            send_403(scapktIP)
            pkt.drop()
        else:
            send_403(scapktIP)
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
finally:
    settings.flushup_rules()
    s.close()
    nfqueue.unbind()
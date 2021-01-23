# import nfqueue

from scapy.all import *
from dpkt import ip
from netfilterqueue import NetfilterQueue
from environment import Environment
import learning, nn, settings
import os, netifaces, socket, struct
import pyshark

from settings import TCP_FLAGS


settings.init_interface()
settings.add_netfilterqueue()

env = Environment()
nn_param = [128, 128]

params = {
    "batchSize": 64,
    "buffer": 50000,
    "nn": nn_param
}

model = nn.neural_net(learning.NUM_INPUT, nn_param)

learning_train = learning.train_net(model, params, env, "modelname")

def feature_extention(packet):
    return [0,0,0,0,0,0,0,0,0,0,0,0] #12
    temp = []
    # temp.append(str(packet.frame_info._all_fields["frame.encap_type"]) )#0
    # temp.append(str(packet.frame_info._all_fields["frame.len"])) #1
    # temp.append(str(packet.frame_info._all_fields["frame.protocols"])) #2
    IP(packet).show()
    
    if packet.haslayer(IP):
        
        temp.append(str(packet[IP].ihl))#3 hdr_len
        temp.append(str(packet[IP].len))#4 len
        temp.append(str(packet[IP].flags))#5 flags.rb
        temp.append(str(packet[IP].flags))#6 flags.df
        temp.append(str(packet[IP].flags))#7 flags.mf
        temp.append(str(packet[IP].frag))#8 frag_offset
        temp.append(str(packet[IP].ttl))#9 ttl
        temp.append(str(packet[IP].proto))#10 proto
        temp.append(str(packet[IP].src))#10 src
        temp.append(str(packet[IP].dst))#11 dst
    else:
        temp.extend(["0","0","0","0","0","0","0","0","0","0"])
    if packet.haslayer(TCP):
        
        temp.append(str(packet[TCP].sport))#12 tcp.srcport
        temp.append(str(packet[TCP].dport))#13 tcp.dstport
        temp.append(str(packet[TCP].seq))#14 tcp.len
        temp.append(str(packet[TCP].ack))#15 tcp.-ack

        temp.append(str(packet[TCP].flags & TCP_FLAGS['RST']))#16 tcp.flags.res
        temp.append(str(packet[TCP].flags & TCP_FLAGS['SYN']))#17 tcp.flags.ns
        temp.append(str(packet[TCP].flags & TCP_FLAGS['CWR']))#18 tcp.flags.cwr
        temp.append(str(packet[TCP].flags & TCP_FLAGS['ECE']))#19 tcp.flags.ecn
        temp.append(str(packet[TCP].flags & TCP_FLAGS['URG']))#20 tcp.flags.urg
        temp.append(str(packet[TCP].flags & TCP_FLAGS['ACK']))#21 tcp.flags.ack
        temp.append(str(packet[TCP].flags & TCP_FLAGS['PSH']))#22 tcp.flags.push
        temp.append(str(packet[TCP].flags & TCP_FLAGS['RST']))#23 tcp.flags.reset
        temp.append(str(packet[TCP].flags & TCP_FLAGS['SYN']))#24 tcp.flags.syn
        temp.append(str(packet[TCP].flags & TCP_FLAGS['FIN']))#25 tcp.flags.fin
        temp.append(str(packet[TCP].window))#26 tcp.window_size
    #temp.append(packet.tcp._all_fields['tcp.analysis.bytes_in_flight'])
    #temp.append(packet.tcp._all_fields['tcp.analysis.push_bytes_sent'])
        # temp.append(str(packet.tcp._all_fields['tcp.time_delta']))#27
    else:
        temp.extend(["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0",])
    print(temp)
    # return temp
    return [0,0,0,0,0,0,0,0,0,0,0,0] #12


def send_403(pkt):
    # pkt[SYN]
    # pkt[IP].src,pkt[IP].dst =  pkt[IP].dst , pkt[IP].src
    # pkt[TCP].sport,pkt[TCP].dport=pkt[TCP].dport,pkt[TCP].sport
    # pkt[TCP].flags='RST'

    ip = IP(src = pkt[IP].dst, dst= pkt[IP].src)
    tcp = TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, flags='SR')
    pkt = ip/tcp
    
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

    
    pkt_pl = pkt.get_payload()
    scapktIP = IP(pkt_pl)
    print("TTTT")
    if scapktIP.haslayer(TCP) and (scapktIP[TCP].flags & TCP_FLAGS['SYN']):
        print("Connection Estalishment.... ")

        #Feature selection
        state = feature_extention(scapktIP)
        env.setState(state)
        print("YYYYYYYYYYYYYYYYYYYY")
        # RL 
        true = next(learning_train)
        res = next(learning_train)
        print("truePARRRRRRRRRRR",res)
        if (res == 1):
            #pkt.accept()
            # send_403(scapktIP)
            pkt.drop()
        else:
            # send_403(scapktIP)
            pkt.accept()
    else:
        print("Act")
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
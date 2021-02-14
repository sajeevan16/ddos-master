# import nfqueue

from scapy.all import *
from dpkt import ip
from netfilterqueue import NetfilterQueue
from environment import Environment
import learning, nn, settings
import os, netifaces, socket, struct
import pyshark

from settings import TCP_FLAGS
import numpy as np

settings.init_interface()
settings.add_netfilterqueue()

env = Environment()

model = nn.neural_net(learning.NUM_INPUT, learning.params['window'], learning.params['nn'])

learning_train = learning.train_net(model, learning.params, env, "modelname")

def feature_extention(packet):
    # return [0,0,0,0,0,0,0,0,0,0,0,0] #12
    temp = []
    # temp.append(str(packet.frame_info._all_fields["frame.encap_type"]) )#0
    # temp.append(str(packet.frame_info._all_fields["frame.len"])) #1
    # temp.append(str(packet.frame_info._all_fields["frame.protocols"])) #2
    # IP(packet).show()
    if packet.haslayer(IP):
        temp.append(int(packet[IP].ihl))#3 hdr_len
        temp.append(int(packet[IP].len))#4 len
        temp.append(int(packet[IP].flags))#5 flags.rb
        temp.append(int(packet[IP].flags))#6 flags.df
        temp.append(int(packet[IP].flags))#7 flags.mf
        temp.append(int(packet[IP].frag))#8 frag_offset
        temp.append(int(packet[IP].ttl))#9 ttl
        temp.append(int(packet[IP].proto))#10 proto
        
        # temp.append(int(packet[IP].src))#10 src
        # temp.append(int(packet[IP].dst))#11 dst
    else:
        temp.extend([0,0,0,0,0,0,0,0])
    if packet.haslayer(TCP):
        
        temp.append(int(packet[TCP].sport))#12 tcp.srcport
        temp.append(int(packet[TCP].dport))#13 tcp.dstport
        # temp.append(int(packet[TCP].seq))#14 tcp.len
        temp.append(int(packet[TCP].ack))#15 tcp.-ack
        
        temp.append(int(packet[TCP].flags & TCP_FLAGS['RST']))#16 tcp.flags.res
        temp.append(int(packet[TCP].flags & TCP_FLAGS['SYN']))#17 tcp.flags.ns
        temp.append(int(packet[TCP].flags & TCP_FLAGS['CWR']))#18 tcp.flags.cwr
        temp.append(int(packet[TCP].flags & TCP_FLAGS['ECE']))#19 tcp.flags.ecn
        temp.append(int(packet[TCP].flags & TCP_FLAGS['URG']))#20 tcp.flags.urg
        temp.append(int(packet[TCP].flags & TCP_FLAGS['ACK']))#21 tcp.flags.ack
        temp.append(int(packet[TCP].flags & TCP_FLAGS['PSH']))#22 tcp.flags.push
        temp.append(int(packet[TCP].flags & TCP_FLAGS['RST']))#23 tcp.flags.reset
        temp.append(int(packet[TCP].flags & TCP_FLAGS['SYN']))#24 tcp.flags.syn
        temp.append(int(packet[TCP].flags & TCP_FLAGS['FIN']))#25 tcp.flags.fin
        temp.append(int(packet[TCP].window))#26 tcp.window_size
    #temp.append(packet.tcp._all_fields['tcp.analysis.bytes_in_flight'])
    #temp.append(packet.tcp._all_fields['tcp.analysis.push_bytes_sent'])
        # temp.append(int(packet.tcp._all_fields['tcp.time_delta']))#27
    else:
        temp.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    label = get_payload_pkt(packet)
    
    # return temp
    temp = adversarial_noise(temp,0.1)
    temp.append(int(label))
    print(temp)
    return temp,label #12

def papams_value(act):
    if (random.random()<0.9316):
        return act
    else:
        return int(not act)

def adversarial_noise(arr,r=0.2):
    tempa = np.array(arr)
    noise = np.random.normal(0,r, tempa.shape)
    temp4p = np.array(arr)
    temp4p[temp4p == 0] = 1
    noise *= temp4p
    return list(tempa+noise)



def get_payload_pkt(packet):
    l=0
    if packet.haslayer(IP):
        l = not str(packet[IP].src).startswith(settings.LOCAL_NET_SUB)
        # Legitimate - 0
        # Attack - 1
    return l


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
    # print("TTTT")
    # state,label = feature_extention(scapktIP)
    # print(state)
    if scapktIP.haslayer(TCP) and (scapktIP[TCP].flags & TCP_FLAGS['SYN']):
        # print("Connection Estalishment.... ")

        #Feature selection
        state,label = feature_extention(scapktIP)
        env.addStateBuffer(state)
        env.setStateLabel(label)
        # RL 
        true = next(learning_train)
        res = next(learning_train)

        # print(true,res)
        # feature_extention(scapktIP)
        if (res == 1):
            #pkt.accept()
            pkt.drop()
        else:
            pkt.accept()
    else:
        pkt.accept()
        # state,label = feature_extention(scapktIP)
        # res = papams_value(int(label))
        # # print("No TCP SYN")
        # if (res == 1):
        #     #pkt.accept()
        #     pkt.drop()
        # else:
        #     pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, analyzer)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)

try:
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('KeyboardInterrupt')
except:
    pass
finally:
    settings.flushup_rules()
    s.close()
    nfqueue.unbind()
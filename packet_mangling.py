# import nfqueue

from scapy.all import *
from dpkt import ip
from netfilterqueue import NetfilterQueue
from environment import Environment
import learning, nn, settings
import os, netifaces, socket, struct
import pyshark




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
    temp = []
    # temp.append(str(packet.frame_info._all_fields["frame.encap_type"]) )#0
    # temp.append(str(packet.frame_info._all_fields["frame.len"])) #1
    # temp.append(str(packet.frame_info._all_fields["frame.protocols"])) #2
    if hasattr(packet, 'ip'):
        temp.append(str(packet.ip._all_fields['ip.hdr_len']))#3
        temp.append(str(packet.ip._all_fields['ip.len']))#4
        temp.append(str(packet.ip._all_fields['ip.flags.rb']))#5
        temp.append(str(packet.ip._all_fields['ip.flags.df']))#6
        temp.append(str(packet.ip._all_fields['ip.flags.mf']))#7
        temp.append(str(packet.ip._all_fields['ip.frag_offset']))#8
        temp.append(str(packet.ip._all_fields['ip.ttl']))#9
        temp.append(str(packet.ip._all_fields['ip.proto']))#10
        temp.append(str(packet.ip._all_fields['ip.src']))#10
        temp.append(str(packet.ip._all_fields['ip.dst']))#11
    else:
        temp.extend(["0","0","0","0","0","0","0","0","0","0"])
    if hasattr(packet, 'tcp'):
        temp.append(str(packet.tcp._all_fields['tcp.srcport']))#12
        temp.append(str(packet.tcp._all_fields['tcp.dstport']))#13
        temp.append(str(packet.tcp._all_fields['tcp.len']))#14
        temp.append(str(packet.tcp._all_fields['tcp.ack']))#15
        temp.append(str(packet.tcp._all_fields['tcp.flags.res']))#16
        temp.append(str(packet.tcp._all_fields['tcp.flags.ns']))#17
        temp.append(str(packet.tcp._all_fields['tcp.flags.cwr']))#18
        temp.append(str(packet.tcp._all_fields['tcp.flags.ecn']))#19
        temp.append(str(packet.tcp._all_fields['tcp.flags.urg']))#20
        temp.append(str(packet.tcp._all_fields['tcp.flags.ack']))#21
        temp.append(str(packet.tcp._all_fields['tcp.flags.push']))#22
        temp.append(str(packet.tcp._all_fields['tcp.flags.reset']))#23
        temp.append(str(packet.tcp._all_fields['tcp.flags.syn']))#24
        temp.append(str(packet.tcp._all_fields['tcp.flags.fin']))#25
        temp.append(str(packet.tcp._all_fields['tcp.window_size']))#26
    #temp.append(packet.tcp._all_fields['tcp.analysis.bytes_in_flight'])
    #temp.append(packet.tcp._all_fields['tcp.analysis.push_bytes_sent'])
        temp.append(str(packet.tcp._all_fields['tcp.time_delta']))#27
    else:
        temp.extend(["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0",])
    print(temp)
    return temp


def send_403(pkt):
    # pkt[SYN]
    # pkt[IP].src,pkt[IP].dst =  pkt[IP].dst , pkt[IP].src
    # pkt[TCP].sport,pkt[TCP].dport=pkt[TCP].dport,pkt[TCP].sport
    # pkt[TCP].flags='RST'

    ip = IP(src=pkt[IP].dst, dst= pkt[IP].src)
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

    print("YYYYYYYYYYYYYYYYYYYY")
    pkt_pl = pkt.get_payload()
    scapktIP = IP(pkt_pl)
    print()
    feature_extention(scapktIP)
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
        feature_extention(scapktIP)
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
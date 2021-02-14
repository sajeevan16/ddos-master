from telnetlib import Telnet
import time, datetime, netifaces, os



def is_interface_up(interface):
    addr = netifaces.ifaddresses(interface)
    return netifaces.AF_INET in addr


def init_interface(maintap = 'wlp3s0',tap = 'tap1', user='sajeev'):
    print("Settings for Network...")
    if(tap not in netifaces.interfaces()):
        os.system("sudo tunctl -t tap1 -u "+user) 
        # sudo tunctl -t tap1 -u sajeev
        os.system("sudo ifconfig tap1 192.168.100.25 netmask 255.255.255.0 up")
        os.system("sudo iptables -t nat -A POSTROUTING -o "+maintap+" -j MASQUERADE")
        # sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE
        os.system("sudo iptables -A FORWARD -i tap1 -j ACCEPT")
        os.system("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
        os.system("sudo ip route add 192.168.0.0/16 via 192.168.100.25 dev tap1")


def add_netfilterqueue(): 
    os.system("sudo iptables -A INPUT -i tap1 -j NFQUEUE --queue-num 1")


def flushup_rules():
    os.system("sudo iptables -F")

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

LOCAL_NET_SUB = "192.168"

def start_legitimate_user(legitimate_users_port):
    legitimate_users_port = [5041, 5002, 5004, ]
    for iport in legitimate_users_port:
        try:
            tn = Telnet('localhost', iport)
            tn.write("python3 legitimate.py".encode('ascii') + b"\n")
            
        except:
            pass
        
def attacker_controller(attacker_port,id):
    intervel = 300
    if (id%intervel==0 and id%(2*intervel)!=0):
        for iport in attacker_port:
            tn = Telnet('localhost', iport)
            tn.write(b"\n")
            tn.write('python pyddos1.py -d "192.168.1.103" -p "5000" -T 10 -Synflood'.encode('ascii') + b"\n")
            output = tn.read_until("#".encode('ascii'), timeout=0.1).decode('ascii').split('\n')
            tn.write("ls".encode('ascii') + b"\n")
    if ((id-(1.5*intervel))%(intervel*2)==0):
        for iport in attacker_port:
            try:
                tn = Telnet('localhost', iport)
                tn.write(b"\n")
                tn.write("ls".encode('ascii') + b"\n")
                output = tn.read_until("#".encode('ascii'), timeout=0.1).decode('ascii').split('\n')
                tn.write("\x03".encode('ascii') + b"\n")
                tn.write("ls".encode('ascii') + b"\n")
                tn = Telnet('localhost', iport)
            except Exception as e:
                print(e)


### TEST

if __name__ == '__main__':
    attacker_controller([5009],75)
from telnetlib import Telnet
import time, datetime, netifaces, os



def is_interface_up(interface):
    addr = netifaces.ifaddresses(interface)
    return netifaces.AF_INET in addr


def init_interface(maintap = 'wlp3s0',tap = 'tap1', user='sajeev'):
    print("Setiiii")
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
    os.system("sudo iptables -A OUTPUT -o tap1 -j NFQUEUE --queue-num 1")


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
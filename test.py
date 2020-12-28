from telnetlib import Telnet
import time
import datetime
import netifaces
import os, math
# tn = Telnet('localhost', 5029)

# tn.write("cat file.txt".encode('ascii') + b"\n")
# output = tn.read_until(":~#".encode('ascii'), timeout=0.1)
# tn.close()

# print(output.decode('ascii'))
# import os

############################

import time

def  init_interface(tap = 'tap1', user='sajeev'):
    if(tap not in netifaces.interfaces()):
        os.system("sudo tunctl -t tap1 -u "+user)
        os.system("sudo ifconfig tap1 192.168.100.25 netmask 255.255.255.0 up")
        os.system("sudo iptables -t nat -A POSTROUTING -o wlp3s0 -j MASQUERADE")
        os.system("sudo iptables -A FORWARD -i tap1 -j ACCEPT")
        os.system("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
        os.system("sudo ip route add 192.168.0.0/16 via 192.168.100.25 dev tap1")

print(netifaces.interfaces())

legitimate_users_port = [5032]


def get_reward():
    delay = []
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    reward = 0
    for iport in legitimate_users_port:
            try:
                tn = Telnet('localhost', iport)
                tn.write("tail -15 result.txt".encode('ascii') + b"\n")
                output = tn.read_until("#".encode('ascii'), timeout=0.1).decode('ascii').split('\n')
                
                for t in output[::-1]:
                    try:
                        if('tail' in t or '#' in t or len(t)<5):
                            continue
                        m,n = t.split()[:2]
                        m,n = float(m),float(n)
                        ts = datetime.datetime.now().timestamp()
                        print("#######")
                        print(m,n)
                        print(ts)
                        print("#######")
                        if ts - m <1:
                            print(ts,n,m,"UUUUUUUUUUUUU")
                            delay.append((ts - m, n ))
                            if (n==-1):
                                reward -= 100*abs(1-(ts-m))
                            elif(0<n<1):
                                reward+= 100*abs(1-(ts-m))*math.exp(-5*n)
                        else:
                            break
                    except Exception as e:
                        print(e,"@@@@@@@",t)
                        pass
                tn.close()
                print(delay)
                #tn.interact()
            except ConnectionRefusedError:
                print("ConnectionRefusedError",iport,"############")
            except Exception as e:
                print(e,iport,"$$$$$$$$$$$$")
            finally:
                print("****************************")
                print(reward)
                print("****************************")
                if(len(delay)==0):
                    return 0
                return reward/len(delay)

            
while True:
    print(get_reward())
    
from telnetlib import Telnet
import time
tn = Telnet('localhost', 5029)

tn.write("cat file.txt".encode('ascii') + b"\n")
output = tn.read_until(":~#".encode('ascii'), timeout=0.1)
tn.close()

print(output.decode('ascii'))


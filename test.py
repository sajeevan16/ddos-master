from telnetlib import Telnet
import time
# tn = Telnet('localhost', 5029)

# tn.write("cat file.txt".encode('ascii') + b"\n")
# output = tn.read_until(":~#".encode('ascii'), timeout=0.1)
# tn.close()

# print(output.decode('ascii'))
# import os

############################

import time
for i in range(65535):
    try:
        tn = Telnet('localhost', i)
        print(i)
        #tn.interact()
    except ConnectionRefusedError:
        pass
    except KeyboardInterrupt:
        print('KeyboardInterrupt',i)
# tn.interact()

tn.write("cat result.txt".encode('ascii') + b"\n")
output = tn.read_until("#".encode('ascii'), timeout=0.1)
tn.close()

print(output.decode('ascii').split('\n'))


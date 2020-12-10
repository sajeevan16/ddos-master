import nfqueue
import socket
from dpkt import ip


q = None
def cb(dummy, payload):
    # make decision about if the packet should be allowed. in this case, drop everything:
    payload.set_verdict(nfqueue.NF_DROP)
q = nfqueue.queue()
q.open()
q.bind(socket.AF_INET)#q.bind()
q.set_callback(cb)
q.create_queue(0) 
try:
        q.try_run()
except KeyboardInterrupt:
        print ("Exiting...")
q.unbind(socket.AF_INET)
q.close()
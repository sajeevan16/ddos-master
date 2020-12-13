# import nfqueue
import socket
from dpkt import ip
from netfilterqueue import NetfilterQueue
import socket
from environment import Environment
import learning, nn

# q = None
# def cb(dummy, payload):
#     # make decision about if the packet should be allowed. in this case, drop everything:
#     payload.set_verdict(nfqueue.NF_DROP)
# q = nfqueue.queue()
# q.open()
# q.bind(socket.AF_INET)#q.bind()
# q.set_callback(cb)
# q.create_queue(0) 
# try:
#         q.try_run()
# except KeyboardInterrupt:
#         print ("Exiting...")
# q.unbind(socket.AF_INET)
# q.close()

# sudo iptables -A INPUT -j NFQUEUE --queue-num 1
# sudo iptables -F

env = Environment()
nn_param = [128, 128]
params = {
    "batchSize": 64,
    "buffer": 50000,
    "nn": nn_param
}

model = nn.neural_net(learning.NUM_INPUT, nn_param)

learning_train = learning.train_net(model, params, env, "modelname")

def print_and_accept(pkt):
    global env,learning_train
    env.setState([3,46,64])
    #print(pkt)
    #print(pkt.get_payload())
    true = next(learning_train)
    res = next(learning_train)
    print(true,res)
    if (res == 1):
        pkt.accept()
    else:
        pkt.drop()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)

try:
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('KeyboardInterrupt')

s.close()
nfqueue.unbind()


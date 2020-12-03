import os, time
import uuid

from flask import Flask, render_template, request, send_file,request, jsonify


from flask import Flask


import fnfqueue

queue = 1
conn = fnfqueue.Connection()

try:
    q = conn.bind(queue)
    q.set_mode(0xffff, fnfqueue.COPY_PACKET)
except PermissionError:
    print("Access denied; Do I have root rights or the needed capabilities?")
    sys.exit(-1)

while True:
    try:
        for packet in conn:
            packet.payload = packet.payload # modify the packet here
            packet.mangle()
    except fnfqueue.BufferOverflowException:
        print("buffer error")
        pass

conn.close() # this can be called concurrently to cancel the above for loop

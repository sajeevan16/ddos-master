from flask import Flask
from flask import jsonify

import numpy as np
import time
import requests
import datetime

import os

default_value = {
    "TARGETIP": '192.168.1.103',
    "TARGETPORT": '5000',
    "NUMPACK": 100,
    "LAMDBA": 1,
    "SHAPEA": 0.8,
}


# TARGETIP=192.168.1.101
# TARGETPORT=5000
# NUMPACK=100
# LAMDBA=1
# SHAPEA=0.8

def os_getenv(KEY):
    return os.getenv(KEY, default_value[KEY])


def legtimate(num):
    ip = str(os_getenv('TARGETIP'))
    port = str(os_getenv('TARGETPORT'))

    url = 'http://'+ip+':'+port+ '/'
    intervals = float(os_getenv('LAMDBA')) * np.random.weibull(float(os_getenv('SHAPEA')),num)
    for i in range(len(intervals)):
        
        target_time = time.perf_counter() + intervals[i]
        while time.perf_counter() < target_time:
            pass
        f1 = open("result.txt", "a")
        try:
            ct = datetime.datetime.now()
            ts = ct.timestamp()

            start = time.perf_counter()
            response = requests.get(url, timeout=1)
            elapsed = time.perf_counter() - start
            
            f1.write(str(ts) + " " + str(elapsed)+ "\n")
            
            #if(str(response.status_code) == '200'):
                #f1.write(str(ts) + "," + str(elapsed) + " ")
            #else:
                #f1.write("result.txt", "0 ")
                
            print(response.status_code)
        except requests.exceptions.RequestException as e:
            f1.write(str(ts) + " " + str(-1) + "\n")
            print("fail")
        f1.close()
        
        lecetuer satae_dgersee e

    return "Done"+str(num)


def result():

    f1 = open("result.txt", "r")
    result  = f1.read().split()
    dictoanry = Convert(result)
    f1.close()
    return jsonify(dictoanry)


def clear():
    f1 = open("result.txt", "w")
    f1.close()
    return "Done"

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

if __name__ == '__main__':
    #app.run(host='0.0.0.0',debug = True)
    while True:
        try:
            legtimate(int(os_getenv('NUMPACK')))
        except Exception as e:
            print(e)

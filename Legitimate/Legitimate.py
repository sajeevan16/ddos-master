from flask import Flask
from flask import jsonify

import numpy as np
import time
import requests
import datetime


app = Flask(__name__)

@app.route('/<int:num>')
def legtimate(num):
    ip = '192.168.110.230'
    url = 'http://192.168.110.230:5000/'
    intervals = np.random.weibull(0.8,num)
    
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
            
            f1.write(str(ts) + " " + str(elapsed) + " ")
            
            #if(str(response.status_code) == '200'):
                #f1.write(str(ts) + "," + str(elapsed) + " ")
            #else:
                #f1.write("result.txt", "0 ")
                
            print(response.status_code)
        except requests.exceptions.RequestException as e:
            f1.write(str(ts) + " " + str(1) + " ")
            print("fail")
        f1.close()

    
    return "Done"

@app.route('/result')
def result():

    f1 = open("result.txt", "r")
    result  = f1.read().split()
    dictoanry = Convert(result)
    f1.close()
    return jsonify(dictoanry)


@app.route('/clear')
def clear():
    f1 = open("result.txt", "w")
    f1.close()
    return "Done"

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True)


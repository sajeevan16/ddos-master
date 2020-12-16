from flask import Flask
from flask import jsonify

import numpy as np
import time
import requests


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
            response = requests.get(url, timeout=1)
            if(str(response.status_code) == '200'):
                f1.write("1 ")
            else:
                f1.write("result.txt", "0 ")
            print(response.status_code)
        except requests.exceptions.RequestException as e:
            f1.write("0 ")
            print("fail")
        f1.close()

    
    return "Done"

@app.route('/result')
def result():

    f1 = open("result.txt", "r")
    result  = f1.read().split()
    f1.close()
    return jsonify(result)


@app.route('/clear')
def clear():
    f1 = open("result.txt", "w")
    f1.close()
    return "Done"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True)


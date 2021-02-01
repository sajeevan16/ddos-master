"""
A simple service that responds with whether an input (post) is
prime or not.
Usage::
./web-server.py [port]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "num=4" http://localhost
"""


from functools import wraps
from math import factorial
from flask import Flask,request,json,Response,jsonify, _request_ctx_stack
app = Flask(__name__)


# Error handler
class Error(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(Error)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def analyser(f):
    """
        Determines if f is an attack
    """
    
    @wraps(f)
    def decorated(*args, **kwargs):
        print(args)
        if False:
            raise Error({ "code": "flood_attack",
                        "description": "Identified as Flood Attack"}, 401)
        return f(*args, **kwargs)
    return decorated

def is_prime(num):
    if num > 1:
        for i in range(2, num//2):
            if (num % i) == 0:
                return False
        else:
            return True
    return False


def sum_primes(num):
    sum = 0
    while (num > 1):
        if is_prime(num):
            sum = sum+num
        num = num - 1
    return sum


# @app.route("/")
# def hello():
#     return "Server successfully started!"

@app.route("/factorial")
def get_factorial():
    try:
        num = int(request.args.get('num'))
    except TypeError:
        data = {'status':422, 'errormsg': 'Parameter  Not Found'}
    except ValueError:
        data = {'status':422, 'errormsg': 'Parameter Error'}
    else:
        if num>=0:
            data = {
                'status':200,
                'number': num,
                'factorial': factorial(num),
                'msg': 'The factorial of %d is %d' %(num, factorial(num))
            }
        else:
            data = {'status':422, 'errormsg': 'Parameter num should grater than or equal to zreo'}
    return Response(json.dumps(data), mimetype='application/json')



@app.route("/")
@analyser
def get_sum_primes():
    print(request.args.get('language'))
    try:
        num = int(request.args.get('num'))
    except TypeError:
        num = 3249
        data = {'status':422, 'errormsg': 'Parameter Not Found'}
    except ValueError:
        num=3249
        data = {'status':422, 'errormsg': 'Parameter Error'}
    if num>=0:
        data = {
            'status':200,
            'number': num,
            'sumprimes': sum_primes(num),
            'msg':'The sum of all primes less than %d is %d' % (num, sum_primes(num))
        }
    else:
        data = {'status':422, 'errormsg': 'Parameter num should grater than or equal to zreo'}
        
    return Response(json.dumps(data), mimetype='application/json')


@app.route("/isprime")
def api_is_prime():
    try:
        num = int(request.args.get('num'))
    except TypeError:
        data = {'status':422, 'errormsg': 'Parameter  Not Found'}
    except ValueError:
        data = {'status':422, 'errormsg': 'Parameter Error'}
    else:
        if num>=0:
            data = {
                'status':200,
                'number': num,
                'is_prime': is_prime(num),
                'msg': str(num)+ ' is a prime number' if  (num) else str(num)+ ' is a not prime number' 
            }
        else:
            data = {'status':422, 'errormsg': 'Parameter num should grater than or equal to zreo'}
    return Response(json.dumps(data), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True, port=5000)

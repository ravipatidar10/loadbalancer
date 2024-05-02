from flask import Flask
import socket
import time
import subprocess
import logging
import random
app = Flask(__name__)

@app.route('/')
def hello_world():
    logging.error("Request received")
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    # if (IPAddr == socket.gethostbyname('loadbalancer-server-3')):
    time.sleep(5)

    return f'{random.random()} <h1>Hello World from server {socket.gethostname()}<h1>'

@app.route('/test')
def test():
    return '<h1>Test from server<h1>'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
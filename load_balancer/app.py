from flask import Flask, request
import requests
import asyncio
import json
import time
import os
import logging
from datetime import datetime, timedelta
import threading
from .tasks import scale_down, cache

lock = threading.Lock()

app = Flask(__name__)

servers = {}

MIN_NO_OF_REPLICAS = int(os.environ.get('MIN_NO_OF_REPLICAS', 1))
MAX_NO_OF_REPLICAS = int(os.environ.get('MAX_NO_OF_REPLICAS', -1))
TIME_FOR_SCALE_DOWN = float(os.environ.get('TIME_FOR_SCALE_DOWN', 2))
SERVER_MAX_REQUESTS = int(os.environ.get('SERVER_MAX_REQUESTS', 2))


NO_OF_REPLICAS = MIN_NO_OF_REPLICAS

i = 1

for i in range(NO_OF_REPLICAS):
    servers[str(i+1)] = {
        'id': i + 1,
        'server_url': f'loadbalancer-server-{i+1}',
        'requests': 0,
        'last_request_time': datetime.utcnow().isoformat(),
    }

cache.set('servers', json.dumps(servers))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world(path):
    global NO_OF_REPLICAS
    i = 0
    logging.error(f"*********** {i}")
    # curr = i

    server_url = None
    busy_servers = 0

    lock.acquire()
    servers = json.loads(cache.get('servers'))
    
    logging.error(f'{servers} {SERVER_MAX_REQUESTS}')

    while True:
        i += 1
        if str(i) not in servers:
            if i < NO_OF_REPLICAS:
                i += 1
                continue
            break
        if servers[str(i)]['requests'] < SERVER_MAX_REQUESTS:
            server_url = servers[str(i)]['server_url']
            servers[str(i)]['requests'] += 1
            servers[str(i)]['last_request_time'] = datetime.utcnow().isoformat()
            break
        busy_servers += 1
        if busy_servers == NO_OF_REPLICAS:
            break
    
    logging.error(server_url)
    if  not server_url:
    # else:
        if len(servers.keys()) >= NO_OF_REPLICAS:
            NO_OF_REPLICAS += 1
        os.system(f'docker compose scale server={NO_OF_REPLICAS}')
        for j in range(1, NO_OF_REPLICAS+1):
            if str(j) not in servers:
                servers[str(NO_OF_REPLICAS)] = {
                    'id': NO_OF_REPLICAS,
                    'server_url': f'loadbalancer-server-{NO_OF_REPLICAS}',
                    'requests': 1,
                    'last_request_time': datetime.utcnow().isoformat()
                } 
            server_url = f'loadbalancer-server-{NO_OF_REPLICAS}'
        i += 1
        time.sleep(5)
        # server_url = f'http://{server_url}:5000'

    cache.set('servers', json.dumps(servers))

    scale_down.apply_async((i, ), eta=datetime.utcnow()+timedelta(minutes=TIME_FOR_SCALE_DOWN))
    server_url = f'http://{server_url}:5000' 

    full_url = f"{server_url}/{path}" 
    req_type = request.method

    lock.release()

    logging.error(f"Sending request {i}")
    # logging.error(server_url)
    # Forward the request with the same request type and parameters
    if req_type == 'GET':
        response = requests.get(full_url, params=request.args)
    elif req_type == 'POST':
        response = requests.post(full_url, json=request.json)
    elif req_type == 'PUT':
        response = requests.put(full_url, json=request.json)
    elif req_type == 'DELETE':
        response = requests.delete(full_url)

    servers[str(i)]['requests'] -= 1
    cache.set('servers', json.dumps(servers))

    # if len(servers.keys()) > 1:
    #     for j in range(1, NO_OF_REPLICAS+1):
    #         if j not in servers:
    #             continue
    #         if (datetime.utcnow() - servers[j]['last_request_time']).seconds > TIME_THRESHOLD * 60:
    #             os.system(f'docker stop loadbalancer-server-{j}')
    #             servers.pop(j)
    #             if (j == NO_OF_REPLICAS):
    #                 os.system(f'docker rm loadbalancer-server-{j}')
    #                 NO_OF_REPLICAS -= 1
    #                 os.system(f'docker compose scale server={NO_OF_REPLICAS}')


    # Return the response from the server
    logging.error(f"response for {i} {response.text}")
    return response.text, response.status_code, response.headers.items()


if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port='5000')
    pass
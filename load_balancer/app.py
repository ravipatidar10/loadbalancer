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
from traceback import format_exc

lock = threading.Lock()

app = Flask(__name__)

servers = {}

MIN_NO_OF_REPLICAS = int(os.environ.get('MIN_NO_OF_REPLICAS', 1))
MAX_NO_OF_REPLICAS = int(os.environ.get('MAX_NO_OF_REPLICAS', -1))
TIME_FOR_SCALE_DOWN = float(os.environ.get('TIME_FOR_SCALE_DOWN', 2))
SERVER_MAX_REQUESTS = int(os.environ.get('SERVER_MAX_REQUESTS', 2))

# ALGO = 'least_connection'
# ALGO = 'round_robin'
ALGO = os.environ.get('ALGO', 'least_connection')


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
    req_type = request.method
    server_url = None
    busy_servers = 0

    lock.acquire()
    # try:
    servers = json.loads(cache.get('servers'))
    

    # while True:
    #     i += 1
    #     if str(i) not in servers:
    #         if i < NO_OF_REPLICAS:
    #             i += 1
    #             continue
    #         break
    #     if servers[str(i)]['requests'] < SERVER_MAX_REQUESTS:
    #         break
    #     busy_servers += 1
    #     if busy_servers == NO_OF_REPLICAS:
    #         break
    server_list = list(servers.values())
    server_url = None
    if ALGO == 'least_connection':
        server_list.sort(key=lambda x: x['requests'])
        server = server_list[0]
        if server['requests'] < SERVER_MAX_REQUESTS:
            i = server['id']
            server_url = servers[str(i)]['server_url']
            servers[str(i)]['requests'] += 1
            servers[str(i)]['last_request_time'] = datetime.utcnow().isoformat()
    elif ALGO == 'round_robin':
        # for server in server_list:
        #     i = server['id']
        if i == 0:
            i = 1
        server = server_list[0]
        if server['requests'] < SERVER_MAX_REQUESTS:
            i = server['id']
            server_url = servers[str(i)]['server_url']
            servers[str(i)]['requests'] += 1
            servers[str(i)]['last_request_time'] = datetime.utcnow().isoformat()
        servers[str(i)] = servers.pop(str(i))
        cache.set('servers', json.dumps(servers))
    
    logging.error(server_url)
    if  not server_url:
    # else:
        if len(servers.keys()) >= NO_OF_REPLICAS:
            if MAX_NO_OF_REPLICAS == -1 or NO_OF_REPLICAS <= MAX_NO_OF_REPLICAS:
                NO_OF_REPLICAS += 1
                os.system(f'docker compose scale server={NO_OF_REPLICAS}')
                time.sleep(2)
        j = 1

        servers = json.loads(cache.get('servers'))
        for j in range(1, NO_OF_REPLICAS+1):
            if str(j) not in servers:
                servers[str(j)] = {
                    'id': j,
                    'server_url': f'loadbalancer-server-{j}',
                    'requests': 1,
                    'last_request_time': datetime.utcnow().isoformat()
                } 
            server_url = f'loadbalancer-server-{NO_OF_REPLICAS}'
        i = j
        # server_url = f'http://{server_url}:5000'

    cache.set('servers', json.dumps(servers))

    scale_down.apply_async((i, ), eta=datetime.utcnow()+timedelta(minutes=TIME_FOR_SCALE_DOWN))
    server_url = f'http://{server_url}:5000' 

    logging.error(f'{servers} {SERVER_MAX_REQUESTS}')
    full_url = f"{server_url}/{path}" 

    # except Exception as e:
    #     format_exc()
    #     print(e)
    lock.release()


    logging.error(f"Sending request {i}")
    # logging.error(server_url)
    # Forward the request with the same request type and parameters
    # response = None
    # try:
    if req_type == 'GET':
        response = requests.get(full_url, params=request.args)
    elif req_type == 'POST':
        response = requests.post(full_url, json=request.json)
    elif req_type == 'PUT':
        response = requests.put(full_url, json=request.json)
    elif req_type == 'DELETE':
        response = requests.delete(full_url)
    # except Exception as e:
    lock.acquire()
    if response.status_code != 200:
        try:
            servers = json.loads(cache.get('servers'))
            servers.pop(i)
            cache.set('servers', json.dumps(servers))
        except Exception as e:
            print(e)
    lock.release()

    lock.acquire()
    try:
        servers = json.loads(cache.get('servers'))
        servers[str(i)]['requests'] -= 1
        if servers[str(i)]['requests'] < 0:
            servers[str(i)]['requests'] = 0
        cache.set('servers', json.dumps(servers))
    except Exception as e:
        print(e)
    lock.release()
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
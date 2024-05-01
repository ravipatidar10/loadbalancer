from flask import Flask, request
import requests
import asyncio
import time
import os
import logging

app = Flask(__name__)

SERVERS = {
    'vcc_assignment4-server1-1': {
        'requests': 0
    }
}

NO_OF_REPLICAS = int(os.environ.get('NO_OF_REPLICAS'))
i = 1

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def hello_world(path):
    global i, NO_OF_REPLICAS
    i = i % NO_OF_REPLICAS + 1 
    logging.error(f"*********** {i}")
    curr = i
    if (i == 3): 
        logging.error(f"Process {i} sleeping")
        await asyncio.sleep(40)
    
    logging.error(f"Sending request {i}")
        
    server_url = f'http://vcc_assignment4-server-{curr}:5000' 
    full_url = f"{server_url}/{path}" 
    req_type = request.method

    # Forward the request with the same request type and parameters
    if req_type == 'GET':
        response = requests.get(full_url, params=request.args)
    elif req_type == 'POST':
        response = requests.post(full_url, json=request.json)
    elif req_type == 'PUT':
        response = requests.put(full_url, json=request.json)
    elif req_type == 'DELETE':
        response = requests.delete(full_url)

    # Return the response from the server
    logging.error(f"response for {curr} {response.text}")
    return response.text, response.status_code, response.headers.items()


if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port='5000')
    pass
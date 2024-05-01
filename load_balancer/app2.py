from quart import Quart, request, jsonify
import aiohttp
import asyncio
import os
import logging
import time

app = Quart(__name__)

# SERVERS = {
#     'vcc_assignment4-server1-1': {
#         'requests': 0
#     }
# }

NO_OF_REPLICAS = 5
i = 1

async def forward_request(path):
    global i, NO_OF_REPLICAS
    i = i % NO_OF_REPLICAS + 1
    logging.error(f"*********** {i}")
    if (i == 3):
        time.sleep(30)
        logging.error(f"Process {i} sleeping")
    logging.error(f"Sending request {i}")
        
    server_url = f'http://vcc_assignment4-server-{i}:5000'
    full_url = f"{server_url}/{path}"
    req_type = request.method

    async with aiohttp.ClientSession() as session:
        if req_type == 'GET':
            async with session.get(full_url, params=request.args) as response:
                return await response.text(), response.status, response.headers.items()
        elif req_type == 'POST':
            async with session.post(full_url, json=await request.json) as response:
                return await response.text(), response.status, response.headers.items()
        elif req_type == 'PUT':
            async with session.put(full_url, json=await request.json) as response:
                return await response.text(), response.status, response.headers.items()
        elif req_type == 'DELETE':
            async with session.delete(full_url) as response:
                return await response.text(), response.status, response.headers.items()

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def hello_world(path):
    return await forward_request(path)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import requests
import httpx
import json
import time
import os
import logging
import asyncio

app = FastAPI()

SERVERS = {
    'vcc_assignment4-server1-1': {
        'requests': 0
    }
}

NO_OF_REPLICAS = int(os.environ.get('NO_OF_REPLICAS'))
i = 1

async def sleep_for_50_seconds():
    await asyncio.sleep(50)

@app.get("/")
@app.post("/")
@app.put("/")
@app.delete("/")
async def hello_world(request: Request, response: Response, path: str = ""):
    global i, NO_OF_REPLICAS
    i = i % NO_OF_REPLICAS + 1
    curr = i
    logging.error(f"*********** {i}")
    # if i == 3:
    #     logging.error(f"Process {i} sleeping")
    #     asyncio.create_task(sleep_for_50_seconds())

    logging.error(f"Sending request {curr}")

    server_url = f'http://vcc_assignment4-server-{curr}:5000'
    full_url = f"{server_url}/{path}"
    req_type = request.method

    # Forward the request with the same request type and parameters
    async with httpx.AsyncClient() as client:
        if req_type == 'GET':
            response = await client.get(full_url, params=request.query_params, timeout=90)
        elif req_type == 'POST':
            response = await client.post(full_url, json=request.json(), timeout=90)
        elif req_type == 'PUT':
            response = await client.put(full_url, json=request.json(), timeout=90)
        elif req_type == 'DELETE':
            response = await client.delete(full_url, timeout=90)
        # return response.text, response.status_code, dict(response.headers)

    logging.error(f"response for {i} {response.text}")
    # Return the response from the server
    return Response(content=response.text, status_code=response.status_code, headers=dict(response.headers))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
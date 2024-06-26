from celery import Celery
import logging
import redis
import json
import os
from datetime import datetime

# Creating a celery instance with redis as message broker.
application = Celery('scale_worker', broker='redis://redis:6379/0')
cache = redis.Redis(host='redis', port='6379')

TIME_FOR_SCALE_DOWN = float(os.environ.get('TIME_FOR_SCALE_DOWN', 2))
MIN_NO_OF_REPLICAS = int(os.environ.get('MIN_NO_OF_REPLICAS', 1))

@application.task
def scale_down(server_id):
    servers = json.loads(cache.get('servers'))
    if str(server_id) not in servers: 
        return str(server_id)
    server = servers[str(server_id)]
    server_name = server['server_url']
    last_request_time = datetime.fromisoformat(server['last_request_time'])

    if (
        (datetime.utcnow() - last_request_time).seconds >= TIME_FOR_SCALE_DOWN * 60
        and
        len(servers.keys()) > MIN_NO_OF_REPLICAS
        and
        server['requests'] <= 0
    ):
        os.system(f'docker stop {server_name}')
        servers.pop(str(server_id))
        cache.set('servers', json.dumps(servers))
        logging.info(f'removing ********* {server_name}, {servers}')
        
    return str(server_id)
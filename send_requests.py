import threading
import requests
import time

success = 0

def reqs(port):
    global success
    res = requests.get(f'http://0.0.0.0:{port}/')
    if res.status_code == 200:
        success += 1

def get_success():
    return success

def send_requests(n, port):
    global success
    success = 0
    start = time.time()
    l = []
    for i in range(n):
        t = threading.Thread(target=reqs, args=(port, ))
        time.sleep(0.2)
        t.start()
        l.append(t)

    for i in l:
        i.join()

    end = time.time()
    # print("Success: ", success)

    t = end - start

    return success, t
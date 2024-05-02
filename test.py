import threading
import requests
import time

success = 0

def reqs():
    global success
    res = requests.get('http://0.0.0.0:5000/')
    if res.status_code == 200:
        success += 1


l = []
for i in range(6):
    t = threading.Thread(target=reqs)
    time.sleep(0.2)
    t.start()
    l.append(t)

for i in l:
    i.join()

print("Success: ", success)
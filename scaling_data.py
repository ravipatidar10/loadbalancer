from send_requests import send_requests, get_success
import subprocess
from threading import Thread
import time

bash_command = "docker ps | wc -l"

def generate_data():
    data = []
    start = time.time()
    data.append([0, 0])
    for i in range(100):
        time.sleep(4)
        res = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        res = res.stdout
        data.append([i, int(res), get_success()])
        print(f'{i},{int(res)},{get_success()}')
    # for i in data:
    #     print(data)    


thrd = Thread(target=generate_data)
thrd.start()
success, t = send_requests(300)
# print(success, t)
thrd.join()
import time
from send_requests import send_requests
import subprocess
import sys

data = []

port = sys.argv[1]

bash_command = "docker ps | wc -l"

for i in range(1, 3):
    success, t = send_requests(i*10, port)
    res = subprocess.run(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    res = res.stdout
    data.append([i*10, success, int(res),t])
    print(f'{i*10},{success},{int(res)},{t}')
    # time.sleep(10)

# for i in data:
#     print(i)
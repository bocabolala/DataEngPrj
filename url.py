import grequests
import time 
# url = 'http://127.0.0.1:5100/accuracy'
url = 'http://130.238.29.77:5100/accuracy'
start = time.time()
req_list = [grequests.get(url) for i in range(1000)]
grequests.map(req_list)
print("DONE", time.time()-start)

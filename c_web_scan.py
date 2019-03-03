from IPy import IP
from queue import Queue
import requests
import threading
import sys


class ScanThread(threading.Thread):
    def __init__(self, queue):
        super(ScanThread, self).__init__()
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            # print(url)
            try:
                resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                if resp.status_code == 200:
                    print("[*]" + url)
                    f = open("./result.html", "a")
                    f.write("<a href='{}' target='_blank'>{}</a></br>".format(url, url))
                    f.close()
            except:
                pass


def create_url(ips):
    queue = Queue()
    req_m = ["http://", "https://"]
    ip = IP(ips, make_net=True)
    ports = [80, 81, 8080, 443]
    # url http://127.0.0.1:80
    for m in req_m:
        for i in ip:
            for port in ports:
                queue.put(m + str(i) + ":" + str(port))
    return queue


def main(ips, counts):
    queue = create_url(ips)
    threads = []
    thread_count = int(counts)
    for i in range(thread_count):
        threads.append(ScanThread(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Example: python c_web_scan.py 192.168.1.0/24 6")
        sys.exit()
    else:
        main(sys.argv[1], sys.argv[2])

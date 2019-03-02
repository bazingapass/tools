from queue import Queue
from proxy_ua import user_agent_pool
import threading
import requests
import sys


# 目录扫描
class DirScan(threading.Thread):
    def __init__(self, queue):
        super(DirScan, self).__init__()
        self._queue = queue

    # 扫描函数
    def run(self):
        while not self._queue.empty():
            url = self._queue.get()
            # print(url)
            try:
                resp = requests.get(url, headers=user_agent_pool.get_user_agent(), timeout=6)
                if resp.status_code == 200:
                    print("[*]", url)
            except:
                pass


def start(url, ext, count):
    queue = Queue()
    # 根据用户输入的扩展(如php)选择字典文件
    with open("./dics/{}.txt".format(ext), "r") as f:
        for i in f:
            queue.put(url+i.rstrip("\r\n"))

    threads = []
    threads_count = int(count)

    for i in range(threads_count):
        threads.append(DirScan(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Use method: python dir_scan.py target extent threads_count")
        print("Example: python dir_scan.py http://hellopentest.com php 2")
        sys.exit()
    else:
        start(sys.argv[1], sys.argv[2], sys.argv[3])

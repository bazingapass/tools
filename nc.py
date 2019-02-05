from socket import *
import argparse
import threading
import subprocess
import sys


# 解析参数
def arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port")
    parser.add_argument("-l", "--listen", action="store_true", help="listen mode")
    parser.add_argument("-c", "--command", action="store_true", help="return shell")
    parser.add_argument("-o", "--other", action="store_true", help="connect to other program")
    arguments = parser.parse_args()
    return arguments


# 服务端socket
def server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    new_socket, address = server_socket.accept()
    return new_socket


# 客户端socket
def client():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket


# 发送数据
def send(sock):
    while True:
        data = sys.stdin.readline()
        if not data:
            break
        sock.send(data.encode())


# 接收数据
def receive(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        sys.stdout.write(data.decode())


# 接收输入，打印命令结果
def command_shell(sock):
    while True:
        c = input("<nc:# >")
        sock.send(c.encode())
        output = sock.recv(1024)
        print(output.decode())


# 执行命令并返回结果
def run_command(sock):
    while True:
        c = sock.recv(1024).decode()
        try:
            output = subprocess.check_output(c)
        except FileNotFoundError:
            output = b"No such file or directory"
        sock.send(output)


# 根据参数配置模块
def main():

    if args.listen:
        sock = server()
    else:
        sock = client()

    # 两端都是nc时进行参数交互
    # arg_c 表示对方是否设置了参数 c
    arg_c = b"0"
    if not args.other:
        if args.command:
            sock.send(b"1")
        else:
            sock.send(b"0")
        arg_c = sock.recv(1)

    if args.command and arg_c == b"0":
        command_shell(sock)

    if (not args.command) and arg_c == b"1":
        run_command(sock)

    if (not args.command) and arg_c == b"0":

        t1 = threading.Thread(target=send, args=(sock,))
        t2 = threading.Thread(target=receive, args=(sock,))
        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()

        while True:
            if (not t1.is_alive()) or (not t2.is_alive()):
                sock.shutdown(2)
                break


if __name__ == '__main__':

    args = arg()
    host = args.host
    port = int(args.port)
    main()


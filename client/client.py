import socket
import threading

# 1 创建tcp套接字
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2 创建连接
tcp_socket.connect(('10.144.200.140', 8080))


def send():
    while True:
        # 3 发送数据
        tcp_input = input('请输入发送内容：')
        tcp_socket.send(tcp_input.encode('gbk'))  # utf-8 中文会乱码


def revice():
    # 接收响应，最大为1024字节
    response = tcp_socket.recv(1024).decode("gbk")
    while response:
        print("来自服务器的数据：%s" % response)
        response = tcp_socket.recv(1024).decode("gbk")
    # 4.关闭套接字
    tcp_socket.close()

# 接收PC端控制LED灯的命令
def revice_led():
    # 接收响应，最大为1024字节
    response = tcp_socket.recv(1024).decode("gbk")
    while response:
        print("来自服务器的数据：%s" % response)
        if response == "1已打开":
            print("111111")
        elif response == "1已关闭":
            print("222222")
        response = tcp_socket.recv(1024).decode("gbk")
    # 4.关闭套接字
    tcp_socket.close()


# 接收pc端控制LED2灯的命令
def revice_led2():
    # 接收响应，最大为1024字节
    response = tcp_socket.recv(1024).decode('gbk')
    while response:
        print("来自服务器的数据：%s" % response)
        if response == "2已打开":
            print("111111")
        elif response == "2已关闭":
            print("222222")
        response = tcp_socket.recv(1024).decode('gbk')
    # 关闭套接字
    tcp_socket.close()

while True:
    # 创建线程
    thread_msg = threading.Thread(target=send, )
    thread_msg1 = threading.Thread(target=revice, )
    thread_msg2 = threading.Thread(target=revice_led,)
    thread_msg3 = threading.Thread(target=revice_led2, )
    # 子线程守护主线程
    thread_msg.setDaemon(True)
    thread_msg1.setDaemon(True)
    thread_msg2.setDaemon(True)
    thread_msg3.setDaemon(True)
    # 启动线程
    thread_msg.start()
    thread_msg1.start()
    thread_msg2.start()
    thread_msg3.start()

    thread_msg.join()
    thread_msg1.join()
    thread_msg2.join()
    thread_msg3.join()

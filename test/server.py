# 1.导入模块
import socket
import threading

def recv_msg(new_tcp_socket, ip_port):
    # 这个while可以不间断的接收客户端信息
    # 7.接受客户端发送的信息
    recv_data = new_tcp_socket.recv(1024)
    while recv_data:
        # 8.解码数据并输出
        recv_text = recv_data.decode('gbk')
        print('来自[%s]的信息：%s' % (str(ip_port), recv_text))
        recv_data = new_tcp_socket.recv(1024)
    new_tcp_socket.close()
    # 关闭客户端连接
    # new_tcp_socket.close()

def send():
    while True:
        # 3 发送数据
        tcp_input = input('请输入发送内容：')
        new_tcp_socket.send(tcp_input.encode('gbk'))  # utf-8 中文会乱码


# 2.创建套接字
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 3.设置地址可以重用
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
# 4.绑定端口
tcp_server_socket.bind(("172.20.176.85", 8080))

# 5.设置监听，套接字由主动变为被动
tcp_server_socket.listen(10)

# 用一个while True来接受多个客户端连接
while True:
    # 6.接收客户端连接
    new_tcp_socket, ip_port = tcp_server_socket.accept()
    print('新用户[%s]连接' % str(ip_port))

    # 创建线程
    thread_msg = threading.Thread(target=recv_msg, args=(new_tcp_socket, ip_port))
    thread_msg1 = threading.Thread(target=send, )
    # 子线程守护主线程
    thread_msg.setDaemon(True)
    thread_msg1.setDaemon(True)
    # 启动线程
    thread_msg.start()
    thread_msg1.start()

# tcp_server_socket.close()

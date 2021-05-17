# 1.导入模块
import socket
import sqlite3
import threading
from common import get_host_ip

con = sqlite3.connect('db.db', check_same_thread=False)
cursor = con.cursor()
lock = threading.Lock()


# 接收树莓派数据
def recv_msg(new_tcp_socket, ip_port):
    recv_data = new_tcp_socket.recv(1024)
    while recv_data:
        # 8.解码数据并输出
        recv_text = recv_data.decode('gbk')
        print('来自[%s]的信息：%s' % (str(ip_port), recv_text))
        if recv_text[0] == "B":  # 接收烟雾浓度数据
            lock.acquire(True)
            nongdu = recv_text[1:]
            cursor.execute('''UPDATE guanli
                            SET  zhuangtai= (?) 
                            WHERE guanli = "yanwu1";''', [nongdu])
            con.commit()
            lock.release()
        elif recv_text[0] == "C":  # 接收火焰传感器1数据
            lock.acquire(True)
            huoyan1 = recv_text[1:]
            cursor.execute('''UPDATE guanli            
                        SET zhuangtai = (?)
                        WHERE guanli = "huoyan1";''', [huoyan1])
            con.commit()
            lock.release()
        elif recv_text[0] == "D":  # 接收火焰传感器2数据
            lock.acquire(True)
            huoyan2 = recv_text[1:]
            cursor.execute('''UPDATE guanli            
                        SET zhuangtai = (?)
                        WHERE guanli = "huoyan2";''', [huoyan2])
            con.commit()
            lock.release()
        elif recv_text[0] == "E":  # 接收烟雾浓度数据
            lock.acquire(True)
            nongdu2 = recv_text[1:]
            cursor.execute('''UPDATE guanli
                            SET  zhuangtai= (?) 
                            WHERE guanli = "yanwu2";''', [nongdu2])
            con.commit()
            lock.release()
        recv_data = new_tcp_socket.recv(1024)
    # 关闭客户端连接
    new_tcp_socket.close()


# 向树莓派发送数据
# LED1
def send_msg_led1():
    flag1 = 1
    flag2 = 1
    while True:
        # 3 发送数据
        lock.acquire(True)
        cursor.execute('''select zhuangtai from guanli where guanli = "led1"''')
        led1 = cursor.fetchone()
        if led1[0] == "已打开" and flag1 == 1:
            listled1 = "1" + str(led1[0])
            print(listled1)
            new_tcp_socket.send(listled1.encode('gbk'))  # utf-8 中文会乱码
            flag1 = 0
            flag2 = 1
        elif led1[0] == "已关闭" and flag2 == 1:
            listled1 = "1" + str(led1[0])
            print(listled1)
            new_tcp_socket.send(listled1.encode('gbk'))  # utf-8 中文会乱码
            flag1 = 1
            flag2 = 0
        con.commit()
        # 4.关闭套接字
        # new_tcp_socket.close()
        lock.release()


print("ip地址为:", get_host_ip())
# 2.创建套接字
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 3.设置地址可以重用
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
# 4.绑定端口
tcp_server_socket.bind((get_host_ip(), 8080))

# 5.设置监听，套接字由主动变为被动
tcp_server_socket.listen(10)

# 用一个while True来接受多个客户端连接
while True:
    # 6.接收客户端连接
    new_tcp_socket, ip_port = tcp_server_socket.accept()
    print('新用户[%s]连接' % str(ip_port))

    # 创建线程
    thread_msg = threading.Thread(target=recv_msg, args=(new_tcp_socket, ip_port))
    thread_msg1 = threading.Thread(target=send_msg_led1, )
    # 子线程守护主线程
    thread_msg.setDaemon(True)
    thread_msg1.setDaemon(True)
    # 启动线程
    thread_msg.start()
    thread_msg1.start()

# tcp_server_socket.close()

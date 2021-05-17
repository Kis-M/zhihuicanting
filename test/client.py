import socket
import time

while True:
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_client.connect(('172.20.176.85', 8080))

    send_data = "wo"

    tcp_client.send(send_data.encode('gbk'))

    time.sleep(10)
    # tcp_client.close()

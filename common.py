import socket
import numpy as np


# 查询本地ip
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# 统计出现的个数
def num(lis):
    lis = np.array(lis)
    key = np.unique(lis)
    result = {}
    for k in key:
        mask = (lis == k)
        list_new = lis[mask]
        v = list_new.size
        result[k] = v
    return result

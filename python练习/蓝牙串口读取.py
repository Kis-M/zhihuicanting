import serial  # ����serial��
import time  # ����time��

s = serial.Serial('com4', 9600, timeout=10)  # �򿪴��ڣ������Ǵ�������

while True:  # ����ѭ����ȡ����

    localtime = time.asctime(time.localtime(time.time()))  # time��������ñ���ʱ����÷�
    n = s.readline()  # serial�����÷� ��ȡ���ڵ�һ������
    data_pre = str(n.decode().strip())  # �Ѷ�ȡ������ת�����ַ���
    print(data_pre)
    print(len(data_pre))
    time.sleep(5)
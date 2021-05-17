import socket
import threading
import RPi.GPIO as GPIO
import time

# LED1灯
pins = {'pin_R': 17, 'pin_G': 27, 'pin_B': 22}  # pins is a dict

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
for i in pins:
    GPIO.setup(pins[i], GPIO.OUT)  # Set pins' mode is output
    GPIO.output(pins[i], GPIO.HIGH)  # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 5000)

p_R.start(100)  # Initial duty Cycle = 100(leds off)
p_G.start(100)
p_B.start(100)


#烟雾1
CHANNEL1=21 # 确定引脚口。按照真实的位置确定
GPIO.setmode(GPIO.BCM) # 选择引脚系统，这里我们选择了BCM，也可以换BOARD
GPIO.setup(CHANNEL1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#烟雾2
CHANNEL2=20 # 确定引脚口。按照真实的位置确定
GPIO.setmode(GPIO.BCM) # 选择引脚系统，这里我们选择了BCM，也可以换BOARD
GPIO.setup(CHANNEL2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

# 蜂鸣器   pin24
Buzzer = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.output(Buzzer, GPIO.HIGH)

# 火焰传感器1 pin25
pin_fire = 25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_fire, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 火焰传感器2 18
pin_fire2 = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_fire2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 1 创建tcp套接字
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2 创建连接
tcp_socket.connect(('192.168.137.157', 8080))


# RGB_LED
def map(x, in_min, in_max, out_min, out_max):  # 将一个数从一个区间线性映射到另一个区间，比如将0~100之间的一个数映射到0~255之间
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def leds(col):
    R_val = (col & 0xFF0000) >> 16
    G_val = (col & 0x00FF00) >> 8
    B_val = (col & 0x0000FF) >> 0

    R_val = map(R_val, 0, 255, 0, 100)  # change a num(0~255) to 0~100.
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)

    return R_val, G_val, B_val


def setColor(col):  # For example : col = 0x112233
    r_val, g_val, b_val = leds(col)
    p_R.ChangeDutyCycle(100 - r_val)  # Change duty cycle
    p_G.ChangeDutyCycle(100 - g_val)
    p_B.ChangeDutyCycle(100 - b_val)

# 蜂鸣器
def on():
    GPIO.output(Buzzer, GPIO.LOW)

def off():
    GPIO.output(Buzzer, GPIO.HIGH)


# 发送烟雾数据1
def sendyanwu1():
    try:
        while True:
            status1 = GPIO.input(CHANNEL1)  # 检测引脚口的输入高低电平状态
            # print(status) # 实时打印此时的电平状态
            if status1 == True:  # 如果为高电平，说明MQ-2正常，并打印“OK”
                off()
                tcp_input = "B正常"
                tcp_socket.send(tcp_input.encode('gbk'))
            else:  # 如果为低电平，说明MQ-2检测到有害气体，并打印“dangerous”
                on()
                tcp_input = "B检测到有害气体"
                tcp_socket.send(tcp_input.encode('gbk'))
            time.sleep(2)  # 睡眠5秒，以后再执行while循环
    except KeyboardInterrupt:  # 异常处理，当检测按下键盘的Ctrl+C，就会退出这个>脚本
        GPIO.cleanup()  # 清理运行完成后的残余

# 发送烟雾数据2
def sendyanwu2():
    time.sleep(3)
    try:
        while True:
            status2 = GPIO.input(CHANNEL2)  # 检测引脚口的输入高低电平状态
            # print(status) # 实时打印此时的电平状态
            if status2 == True:  # 如果为高电平，说明MQ-2正常，并打印“OK”
                off()
                tcp_input = "E正常"
                tcp_socket.send(tcp_input.encode('gbk'))
            else:  # 如果为低电平，说明MQ-2检测到有害气体，并打印“dangerous”
                on()
                tcp_input = "E检测到有害气体"
                tcp_socket.send(tcp_input.encode('gbk'))
            time.sleep(2)  # 睡眠5秒，以后再执行while循环
    except KeyboardInterrupt:  # 异常处理，当检测按下键盘的Ctrl+C，就会退出这个>脚本
        GPIO.cleanup()  # 清理运行完成后的残余

# 发送火焰传感器1状态
def sendhuoyan():
    flage1 = 1
    while True:
        status = GPIO.input(pin_fire)
        if status == True and flage1 == 1:
            off()
            tcp_input = 'C正常'
            tcp_socket.send(tcp_input.encode('gbk'))
            flage1 = 0
        elif status == False:
            on()
            tcp_input = 'C检测到火源'
            tcp_socket.send(tcp_input.encode('gbk'))
            flage1 = 1
            time.sleep(3)
        time.sleep(0.5)


# 发送火焰传感器2状态
def sendhuoyan2():
    flage2 = 1
    time.sleep(5)
    while True:
        status2 = GPIO.input(pin_fire2)
        if status2 == True and flage2 == 1:
            off()
            tcp_input = 'D正常'
            tcp_socket.send(tcp_input.encode('gbk'))
            flage2 = 0
        elif status2 == False:
            on()
            tcp_input = 'D检测到火源'
            tcp_socket.send(tcp_input.encode('gbk'))
            flage2 = 1
            time.sleep(3)
        time.sleep(0.5)


# 接收PC端控制LED灯的命令
def revice_led():
    # 接收响应，最大为1024字节
    response = tcp_socket.recv(1024).decode("gbk")
    while response:
        print("来自服务器的数据：%s" % response)
        if response == "1已打开":
            setColor(0xFF0000)
            # print("111111")
        elif response == "1已关闭":
            setColor(0xFFFFFF)
            # print("222222")
        response = tcp_socket.recv(1024).decode("gbk")
    # 4.关闭套接字
    tcp_socket.close()



def revice():
    while True:
        # 接收响应，最大为1024字节
        response = tcp_socket.recv(1024).decode("gbk")
        print("来自服务器的数据：%s" % response)

    # 4.关闭套接字
    # tcp_socket.close()


while True:
    # 创建线程
    thread_msg1 = threading.Thread(target=revice_led, )
    thread_msg2 = threading.Thread(target=sendyanwu1, )
    thread_msg5 = threading.Thread(target=sendyanwu2, )
    thread_msg3 = threading.Thread(target=sendhuoyan, )
    thread_msg4 = threading.Thread(target=sendhuoyan2, )
    # 子线程守护主线程
    thread_msg1.setDaemon(True)
    thread_msg2.setDaemon(True)
    thread_msg3.setDaemon(True)
    thread_msg4.setDaemon(True)
    thread_msg5.setDaemon(True)
    # 启动线程
    thread_msg1.start()
    thread_msg2.start()
    thread_msg3.start()
    thread_msg4.start()
    thread_msg5.start()

    thread_msg1.join()
    thread_msg2.join()
    thread_msg3.join()
    thread_msg4.join()
    thread_msg5.join()

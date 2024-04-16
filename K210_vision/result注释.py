from machine import Timer, PWM
from machine import UART
from fpioa_manager import fm
import sensor
import image
import lcd
import time





# 初始化LCD显示器
lcd.init()
lcd.rotation(2)

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

# 预留一些时间让摄像头稳定
#sensor.skip_frames(time = 2000)

# 阶段数储存
data = 0
# 方向储存
var = 0
# 当前所在的块
block = '00'

# 初始化三个舵机，将它们都放在最初的位置

tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim1 = Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim2 = Timer(Timer.TIMER2, Timer.CHANNEL0, mode=Timer.MODE_PWM)

S1 = PWM(tim0, freq=50, duty=0, pin=19)  # 一号仓舵机
S2 = PWM(tim1, freq=50, duty=0, pin=17)  # 二号仓舵机
S3 = PWM(tim2, freq=50, duty=0, pin=18)  # 摄像头舵机


# 将三个舵机的角度都设为 angle 度
def Servo(servo, angle):
    S1.duty((angle+90)/180*10+2.5)


def Servo2(servo, angle):
    S2.duty((angle+90)/180*10+2.5)


def Servo3(servo, angle):
    S3.duty((angle+90)/180*10+2.5)


fm.register(15, fm.fpioa.UART1_TX, force=True)
fm.register(16, fm.fpioa.UART1_RX, force=True)

# 启动摄像头
sensor.run(1)

# 红色的颜色阈值
red_threshold = (31, 47, 10, 37, -10, 29)
# 绿色灯的颜色阈值
green_light = (75, 100, -31, -10, -8, 9)
# 黑色的颜色阈值
black_threshold = (0, 34, -12, 9, -9, 8)
# 棕色的颜色阈值
brown_threshold = (12, 29, -5, 27, -9, 14)

# 先将所有舵机复位
Servo(S1, -4)
Servo2(S2, -4)
Servo3(S3, -4)


# 循环读取图像进行处理
while True:
    img = sensor.snapshot()

    # 如果 data 为 0，则进行二维码的识别
    if data == 0:
        # 检测二维码
        code = img.find_qrcodes()
        if code:
            for c in code:
                # 将二维码框出
                imp = img.draw_rectangle(
                    c[0:4], color=(255, 0, 0), thickness=2)
                # 在图像上显示二维码内容
                img.draw_string(2, 2, code[0].payload(),
                                color=(0, 128, 0), scale=2)
                code_data = code[0].payload

                # 根据二维码的内容进行相应的处理
                block = code_data
                print('block=', block)
                if code_data == '11':
                    # 初始化串口，发送信号给控制云台的板子
                    uart_A = UART(UART.UART1, 9600, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)
                    uart_A.write('A7:00001')
                    print('uart_A.write(A7:00001)')
                    # 控制云台转动到特定位置
                    Servo(S1, -90)
                    print('S1=-90')
                    data = 1
                    var = 1
                    print('var=', var)
                    time.sleep(3)
                    # 控制云台转动到初始位置
                    Servo(S1, -4)
                    print('S1=-4')
                    # 初始化串口，发送信号给另一个板子
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)
                    uart_A.write('6')
                    time.sleep(0.01)
                if code_data == '12':
                    # 初始化端口，发送信号给控制云台的板子
                    fm.register(15, fm.fpioa.UART1_TX, force=True)
                    fm.register(16, fm.fpioa.UART1_RX, force=True)
                    uart_A = UART(UART.UART1, 9600, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)
                    uart_A.write('A7:00001')
                    print('uart_A.write(A7:00001)')
                    # 控制云台转动到特定位置
                    Servo(S1, -90)
                    print('S1=-90')
                    data = 1
                    var = 1
                    print('var=', var)
                    time.sleep(5)
                    # 控制云台转动到初始位置
                    Servo(S1, -4)
                    print('S1=-4')
                    # 初始化端口，发送信号给另一个板子
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)
                    uart_A.write('5')
                    time.sleep(0.01)
                if code_data == '21':
                    # 初始化端口，发送信号给控制云台的板子


                    uart_A = UART(UART.UART1, 9600, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)

                    uart_A.write('A7:00002')  # 向云台控制板发送信号

                    print('uart_A.write(A7:00002)')

                    Servo2(S2, -90)  # 将云台向左旋转

                    print('S2=-90')

                    data = 1
                    var = 2
                    print('var=', var)

                    time.sleep(5)  # 等待5秒


                    Servo2(S2, -4)  # 将云台向右旋转

                    print('S2=-4')

                    uart_A = UART(UART.UART1, 115200, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)

                    uart_A.write('6')  # 发送一个信号


                if code_data == '22':
                    uart_A = UART(UART.UART1, 9600, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)

                    uart_A.write('A7:00002')  # 向云台控制板发送信号

                    print('uart_A.write(A7:00002)')

                    Servo2(S2, -90)  # 将云台向左旋转

                    print('S2=-90')

                    data = 1
                    var = 2
                    print('var=', var)

                    time.sleep(5)  # 等待5秒


                    Servo2(S2, -4)  # 将云台向右旋转

                    print('S4=-4')

                    uart_A = UART(UART.UART1, 115200, 8, 0, 0,
                                  timeout=1000, read_buf_len=4096)

                    uart_A.write('5')  # 发送一个信号


                    time.sleep(0.01)

   # 判断 data 是否等于 1
    if data == 1:
        # 控制舵机将摄像头旋转到指定角度
        Servo3(S3, -90)
        # 等待 3 秒，让摄像头稳定
        time.sleep(3)
        # 识别图像中的红线
        redthreshold = img.find_blobs([red_threshold])
        # 判断是否识别到红线
        if redthreshold:
            # 初始化最大区域为0
            max_size = 0
            # 遍历所有红线区域
            for r in redthreshold:
                # 如果当前红线区域的面积比最大区域还大，就更新最大区域
                if r[2]*r[3] > max_size:
                    mr = r
                    max_size = r[2]*r[3]
            # 在原图上标注红线区域
            img = img.draw_rectangle(mr[0:4], color=(255, 0, 0), thickness=2)
            # 控制串口向下位机发送数据，表示识别到了红线
            print('输出0')
            uart_A.write('0')
            time.sleep(0.01)
            # 将 data 设置为 2
            data = 2

    if data == 2:
        Servo3(S3, -4)  # 舵机3转到-4度
        greenlight = img.find_blobs([green_light])  # 识别绿灯
        if greenlight:
            max_size = 0
            for gl in greenlight:
                if gl[2]*gl[3] > max_size:
                    mgl = gl  # 获取绿灯中最大的一个区域
                    max_size = gl[2]*gl[3]
            img = img.draw_rectangle(mgl[0:4], color=(
                255, 0, 0), thickness=2)  # 在图像上标记出绿灯位置
            print('8')  # 输出8
            uart_A.write('8')  # 发送8到控制云台的板子
            time.sleep(0.01)
            data = 3  # 切换到下一状态

    if data == 3:
        # 控制舵机转动
        Servo3(S3, -90)
        # 等待 3 秒钟
        time.sleep(3)
        # 识别棕色区域
        brownthreshold = img.find_blobs([brown_threshold])
        if brownthreshold:
            # 找到最大的棕色区域
            max_size = 0
            for b in brownthreshold:
                if b[2]*b[3] > max_size:
                    mb = b
                    max_size = b[2]*b[3]
            # 在图片上标注棕色区域
            img = img.draw_rectangle(mb[0:4], color=(255, 0, 0), thickness=2)
            # 发送信号给下一个控制板
            print('next')
            data = 4

    if data == 4:
        Servo3(S3, -4)  # 舵机3转动到指定角度
        code_two = img.find_qrcodes()  # 识别二维码
        if code_two:
            for c in code_two:
                imp = img.draw_rectangle(c[0:4], color=(
                    255, 0, 0), thickness=2)  # 将二维码框出
                img.draw_string(2, 2, code_two[0].payload(), color=(
                    0, 128, 0), scale=2)  # 显示二维码内容
                code_two_data = code_two[0].payload()  # 获取二维码内容
                print('code_two_data=', code_two_data)
                if code_two_data == block:  # 如果变量code_two_data等于block
                    if var == 1:  # 如果变量var等于1
                        uart_A = UART(UART.UART1, 9600, 8, 0, 0,  # 初始化UART模块
                                      timeout=1000, read_buf_len=4096)

                        Servo(S1, -90)  # 将舵机S1转到-90度位置
                        print('S1=-90')
                        uart_A.write('A7:00003')  # 通过UART发送数据
                        print('A7:00003')
                        time.sleep(5)  # 等待5秒
                        Servo(S1, -4)  # 将舵机S1转到-4度位置
                        print('S1=-4')
                        print('9')
                        uart_A = UART(UART.UART1, 115200, 8, 0, 0,  # 初始化UART模块
                                      timeout=1000, read_buf_len=4096)

                        uart_A.write('9')  # 通过UART发送数据
                        time.sleep(0.01)  # 等待0.01秒
                        data = 5  # 将变量data赋值为5
                    if var == 2:  # 如果变量var等于2
                        # 设置引脚15用于UART1的TX输出
                        fm.register(15, fm.fpioa.UART1_TX, force=True)
                        # 设置引脚16用于UART1的RX输入
                        fm.register(16, fm.fpioa.UART1_RX, force=True)

                        uart_A = UART(UART.UART1, 9600, 8, 0, 0,  # 初始化UART模块
                                      timeout=1000, read_buf_len=4096)

                        Servo2(S2, -90)  # 将舵机S2转到-90度位置
                        print('S2=-90')
                        uart_A.write('A7:00004')  # 通过UART发送数据
                        print('A7:00004')
                        time.sleep(5)  # 等待5秒
                        Servo2(S2, -4)  # 将舵机S2转到-4度位置
                        print('S2=-4')
                        print('9')
                        uart_A = UART(UART.UART1, 115200, 8, 0, 0,  # 初始化UART模块
                                      timeout=1000, read_buf_len=4096)

                        uart_A.write('9')  # 通过UART发送数据
                        time.sleep(0.01)  # 等待0.01秒
                        data = 5  # 将变量data赋值为5

    lcd.display(img)

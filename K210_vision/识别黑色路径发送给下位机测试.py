import sensor
import image
import lcd
import time

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)
data=0 #阶段数储存
var =0 #方向储存
block = '00'

from fpioa_manager import fm
from machine import UART
from fpioa_manager import fm

from machine import Timer,PWM

tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim1 = Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim2 = Timer(Timer.TIMER2, Timer.CHANNEL0, mode=Timer.MODE_PWM)

S1 = PWM(tim0, freq=50, duty=0, pin=19)#一号仓舵机
S2 = PWM(tim1, freq=50, duty=0, pin=17)#二号仓舵机
S3 = PWM(tim2, freq=50, duty=0, pin=18)#摄像头舵机


def Servo(servo,angle):
    S1.duty((angle+90)/180*10+2.5)
def Servo2(servo,angle):
    S2.duty((angle+90)/180*10+2.5)
def Servo3(servo,angle):
    S3.duty((angle+90)/180*10+2.5)



fm.register(15, fm.fpioa.UART1_TX, force=True)
fm.register(16, fm.fpioa.UART1_RX, force=True)

sensor.run(1)

red_threshold =(31, 47, 10, 37, -10, 29)#(15, 54, 4, 53, 1, 55)
green_light =(75, 100, -31, -10, -8, 9)#(86, 100, -46, -16, -32, 8)#(95, 100, -20, 11, -8, 13)
black_threshold=(0, 21, -11, 6, -5, 3)# (0, 34, -12, 9, -9, 8)
brown_threshold =(12, 29, -5, 27, -9, 14)
purple_threshold =(13, 32, 2, 36, -39, -7)
brown_threshold =(12, 29, -5, 27, -9, 14)
yellow_threshold =(44, 54, -23, -6, 1, 21)

Servo(S1,-4)#三个舵机复位
Servo2(S2,-4)
Servo3(S3,-4)

i=0


while True:
    img=sensor.snapshot()
    if data == 0:
        code = img.find_qrcodes() #识别二维码
        if code:
            for c in code:
                imp=img.draw_rectangle(c[0:4],color = (255, 0, 0), thickness = 2)#将二维码框出
                img.draw_string(2,2, code[0].payload(), color=(0,128,0), scale=2)
                code_data = code[0].payload()
                block = code_data
                print('block=',block)
                if code_data == '11':
                    uart_A = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)
                    uart_A.write('A7:00001')
                    print('uart_A.write(A7:00001)')
                    Servo(S1,-90)
                    print('S1=-90')
                    data=1
                    var=1
                    print('var=',var)
                    time.sleep(3)
                    Servo(S1,-4)
                    print('S1=-4')
                    uart_A.write('6')
                    time.sleep(0.01)
                    Servo3(S3,-60)
                    time.sleep(2)
                if code_data == '12':
                    fm.register(15, fm.fpioa.UART1_TX, force=True)
                    fm.register(16, fm.fpioa.UART1_RX, force=True)
                    uart_A = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)
                    uart_A.write('A7:00001')
                    print('uart_A.write(A7:00001)')
                    Servo(S1,-90)
                    print('S1=-90')
                    data=1
                    var=1
                    print('var=',var)
                    time.sleep(5)
                    Servo(S1,-4)
                    print('S1=-4')
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                    uart_A.write('5')
                    time.sleep(0.01)
                    Servo3(S3,-60)
                    time.sleep(2)
                if code_data == '21':
                    uart_A = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)
                    uart_A.write('A7:00011')
                    print('uart_A.write(A7:00011)')
                    Servo2(S2,-90)
                    print('S2=-90')
                    data=1
                    var=2
                    print('var=',var)
                    time.sleep(5)
                    Servo2(S2,-4)
                    print('S2=-4')
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                    uart_A.write('6')
                    time.sleep(0.01)
                    Servo3(S3,-60)
                    time.sleep(2)
                if code_data == '22':
                    uart_A = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)
                    uart_A.write('A7:00011')
                    print('uart_A.write(A7:00011)')
                    Servo2(S2,-90)
                    print('S2=-90')
                    data=1
                    var=2
                    print('var=',var)
                    time.sleep(5)
                    Servo2(S2,-4)
                    print('S4=-4')
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                    uart_A.write('5')
                    time.sleep(0.01)
                    Servo3(S3,-60)
                    time.sleep(2)

    if data==1:
        blackthreshold=img.find_blobs([black_threshold])#识别黑线
        if blackthreshold:
            max_size=0
            for bl in blackthreshold:
                if bl[2]*bl[3] > max_size:
                    mbl=bl
                    max_size = bl[2]*bl[3]
            img=img.draw_rectangle(mbl[0:4],color = (255, 0, 0), thickness = 2)
            if mbl[5] > 180:
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('5')
                time.sleep(0.2)
                print('逆')
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('2')
                time.sleep(0.2)
                print('前进')
            if mbl[5] < 60:
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('6')
                time.sleep(0.2)
                print('顺')
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('2')
                time.sleep(0.2)
                print('前进')
            if mbl[5] > 60:
                if mbl[5]<120:
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                    uart_A.write('6')
                    time.sleep(0.2)

                    print('顺')
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                    uart_A.write('2')
                    time.sleep(0.2)
                    print('前进')
            if mbl[5] > 120 :
                   if mbl[5]<180:
                       uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                       uart_A.write('5')
                       time.sleep(0.2)

                       print('逆')
                       uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                       uart_A.write('2')
                       time.sleep(0.2)
                       print('前进')




    if data == 2:
        Servo3(S3,-4)
        greenlight = img.find_blobs([green_light])#识别绿灯
        if greenlight:
            max_size=0
            for gl in greenlight:
                if gl[2]*gl[3] > max_size:
                    mgl=gl
                    max_size = gl[2]*gl[3]
            img=img.draw_rectangle(mgl[0:4],color = (255, 0, 0), thickness = 2)
            print('8')
            uart_A.write('8')
            time.sleep(0.01)
            data=3
            Servo3(S3,-70)
            time.sleep(3)

    if data == 3:
        blackthreshold=img.find_blobs([black_threshold])#识别黑线
        brownthreshold = img.find_blobs([brown_threshold])#识别棕色
        if brownthreshold:
            max_size=0
            for b in brownthreshold:
                if b[2]*b[3] > max_size:
                    mb=b
                    max_size = b[2]*b[3]
            img=img.draw_rectangle(mb[0:4],color = (255, 0, 0), thickness = 2)
            print('next')
            data=4
        if blackthreshold:
            max_size=0
            for bl in blackthreshold:
                if bl[2]*bl[3] > max_size:
                    mbl=bl
                    max_size = bl[2]*bl[3]
            img=img.draw_rectangle(mbl[0:4],color = (255, 0, 0), thickness = 2)
            if mbl[5] > 180:
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('5')
                time.sleep(0.2)
                print('逆')
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('2')
                time.sleep(0.2)
                print('前进')
            if mbl[5] < 60:
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('6')
                time.sleep(0.2)
                print('顺')
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('2')
                time.sleep(0.2)
                print('前进')
            if mbl[5] > 60:
                if mbl[5]<120:
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                    uart_A.write('6')
                    time.sleep(0.2)

                    print('顺')
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                    uart_A.write('2')
                    time.sleep(0.2)
                    print('前进')
            if mbl[5] > 120 :
                   if mbl[5]<180:
                       uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                       uart_A.write('5')
                       time.sleep(0.2)

                       print('逆')
                       uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                       uart_A.write('2')
                       time.sleep(0.2)
                       print('前进')


    if data == 4:
        Servo3(S3,-4)
        code_two = img.find_qrcodes() #识别二维码
        if code_two:
            for c in code_two:
                imp=img.draw_rectangle(c[0:4],color = (255, 0, 0), thickness = 2)#将二维码框出
                img.draw_string(2,2, code_two[0].payload(), color=(0,128,0), scale=2)
                code_two_data = code_two[0].payload()
                print('code_two_data=',code_two_data)
                if code_two_data == block:
                    if var == 1:

                        uart_A = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)

                        Servo(S1,-90)
                        print('S1=-90')
                        uart_A.write('A7:00111')
                        print('A7:00003')
                        time.sleep(5)
                        Servo(S1,-4)
                        print('S1=-4')


                        data=5
                    if var == 2:
                        fm.register(15, fm.fpioa.UART1_TX, force=True)
                        fm.register(16, fm.fpioa.UART1_RX, force=True)

                        uart_A = UART(UART.UART1, 9600, 8, 0, 0, timeout=1000, read_buf_len=4096)

                        Servo2(S2,-90)
                        print('S2=-90')
                        uart_A.write('A7:01111')
                        print('A7:00004')
                        time.sleep(5)
                        Servo2(S2,-4)
                        print('S2=-4')


                        data=5

    i=0
    if data == 5:
        while i < 15 :
            uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
            uart_A.write('6')
            time.sleep(0.2)
            i=i+1
        if i>14:
            data=6


    if data == 6:
        blackthreshold=img.find_blobs([black_threshold])#识别黑线

        yellow = img.find_blobs([yellow_threshold])
        if yellow:
            max_size=0
            for y in yellow:
                if y[2]*y[3] > max_size:
                    my=y
                    max_size = y[2]*y[3]
            img=img.draw_rectangle(my[0:4],color = (255, 0, 0), thickness = 2)
            data=7
        if blackthreshold:
            max_size=0
            for bl in blackthreshold:
                if bl[2]*bl[3] > max_size:
                    mbl=bl
                    max_size = bl[2]*bl[3]
            img=img.draw_rectangle(mbl[0:4],color = (255, 0, 0), thickness = 2)
            if mbl[5] > 180:
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('5')
                time.sleep(0.2)
                print('逆')
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('2')
                time.sleep(0.2)
                print('前进')
            if mbl[5] < 60:
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('6')
                time.sleep(0.2)
                print('顺')
                uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                uart_A.write('2')
                time.sleep(0.2)
                print('前进')
            if mbl[5] > 60:
                if mbl[5]<120:
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                    uart_A.write('6')
                    time.sleep(0.2)

                    print('顺')
                    uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                    uart_A.write('2')
                    time.sleep(0.2)
                    print('前进')
            if mbl[5] > 120 :
                   if mbl[5]<180:
                       uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

                       uart_A.write('5')
                       time.sleep(0.2)

                       print('逆')
                       uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)
                       uart_A.write('2')
                       time.sleep(0.2)
                       print('前进')
    lcd.display(img)




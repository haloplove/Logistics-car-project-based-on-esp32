'''from machine import Timer,PWM
import time

tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)

S1 = PWM(tim0, freq=50, duty=0, pin=17)


def Servo(servo,angle):
    S1.duty((angle+90)/180*10+2.5)


Servo(S1,0)
while True:
    for angle_data in range(0,-90):
        Servo(S1,angle_data)
        time.sleep(0.05)
    for angle_data in range(0,-90):
        i=0-angle_data
        Servo(S1,i)
        time.sleep(0.05)

    Servo(S1,0)
    time.sleep(2)
    Servo(S1,-90)
    time.sleep(2)
'''
from machine import Timer,PWM
import time

#PWM通过定时器配置，接到IO17引脚
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
S1 = PWM(tim, freq=50, duty=0, pin=17)

'''
说明：舵机控制函数
功能：180度舵机：angle:-90至90 表示相应的角度
     360连续旋转度舵机：angle:-90至90 旋转方向和速度值。
    【duty】占空比值：0-100
'''

def Servo(servo,angle):
    S1.duty((angle+90)/180*10+2.5)


while True:

    Servo(S1,-4)
    time.sleep(1)

    #45度
    Servo(S1,-45)
    time.sleep(1)

    #90度
    Servo(S1,-90)
    time.sleep(1)

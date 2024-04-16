import sensor
import image
import lcd
import time

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

from fpioa_manager import fm
from machine import UART
from fpioa_manager import fm


sensor.run(1)
red_threshold =(15, 54, 4, 53, 1, 55)
red_light =(76, 100, -21, 127, -12, 40)
yellow_light =(94, 100, -23, 8, -9, 33)
green_light =(95, 100, -20, 11, -8, 13)
purple_threshold =(13, 32, 2, 36, -39, -7) #,(29, 58, 11, 36, -12, 4)
yellow_threshold =(44, 54, -23, -6, 1, 21)
brown_threshold =(12, 29, -5, 27, -9, 14)
#green_threshold =((57, 76, -70, -30, 3, 62))
black_threshold=(0, 21, -11, 6, -5, 3)# (0, 34, -12, 9, -9, 8)
while True:
    img=sensor.snapshot()
    blackthreshold=img.find_blobs([black_threshold])#识别黑线
    if blackthreshold:
        max_size=0
        for bl in blackthreshold:
            if bl[2]*bl[3] > max_size:
                mbl=bl
                max_size = bl[2]*bl[3]

        img=img.draw_rectangle(mbl[0:4],color = (255, 0, 0), thickness = 2)
        x=mbl.x()
        y=mbl.y()
        z=mbl.w()
        a=mbl.h()
        b=mbl.cx()
        c=mbl.cy()


        print('mb[1]',x)
        print('mb[2]',y)
        print('mb[3]',z)
        print('mb[4]',a)
        print('mb[5]',b)
        print('mb[6]',c)

    lcd.display(img)

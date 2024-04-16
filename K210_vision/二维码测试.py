import image
import sensor
import lcd
import time
clock = time.clock()
#lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
lcd.rotation(2)
sensor.skip_frames(30)
while True:
    #clock.tick()
    img = sensor.snapshot()
    res = img.find_qrcodes() #识别二维码
    if res:
        for b in res:
            tmp=img.draw_rectangle(b[0:4])
            img.draw_string(2,2, res[0].payload(), color=(0,128,0), scale=2)#将二维码框出
            print(res[0].payload())
    lcd.display(img)




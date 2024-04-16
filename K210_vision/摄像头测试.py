import sensor
import image
import lcd

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

while True:
    img=sensor.snapshot()
    lcd.display(img)

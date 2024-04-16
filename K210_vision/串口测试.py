from fpioa_manager import fm
from machine import UART
from fpioa_manager import fm
import time

fm.register(15, fm.fpioa.UART1_TX, force=True)
fm.register(16, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)


while True:
    '''
    read_data = uart_A.read()
    write_str = read_data
    if read_data:
        uart_A.write(write_str)
        uart_A.write(' 1 ')
        uart_A.write(write_str)
        read_str = read_data.decode('utf-8')
        print("string = ", read_str)
     '''
    i=0
    while( i < 500) :
        uart_A.write('2')
        time.sleep(0.01)
        i=i+1
    time.sleep(2)
    i=0
    while( i < 500) :
        uart_A.write('3')
        time.sleep(0.01)
        i=i+1
    time.sleep(2)
    i=0
    while( i < 500) :
        uart_A.write('4')
        time.sleep(0.01)
        i=i+1
    time.sleep(2)
    i=0
    while( i < 500) :
        uart_A.write('5')
        time.sleep(0.01)
        i=i+1
    time.sleep(2)
    i=0
    while( i < 500) :
        uart_A.write('6')
        time.sleep(0.01)
        i=i+1
    time.sleep(2)


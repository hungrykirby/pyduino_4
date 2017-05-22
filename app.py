import serial
import re
import threading
import sys

import arrange

c = "1025"
is_calibration = False
console_input = sys.argv
print(len(console_input))
if len(console_input) == 2:
    MODE = console_input[1]
else:
    sys.exit()


def serial_loop():
    global is_calibration
    with serial.Serial('COM3',9600,timeout=0.1) as ser:
        arra = arrange.Arrange(ser, MODE)
        try:
            while True:
                s = ser.readline()
                de = s.decode('utf-8')
                m = re.match("\-*[\w]+", str(de))
                #print(m)
                if(m != None):
                    #print(is_calibration)
                    is_calibration = arra.fetch_three_numbers(m.group(), is_calibration, c)
                else:
                    pass
                    #print(type(m))
        except:
             print("Unexpected error:", sys.exc_info()[0])
             raise
        ser.close()

ser_loop = threading.Thread(target=serial_loop,name="ser_loop",args=())
ser_loop.setDaemon(True)
ser_loop.start()

def main():
    global c
    global is_calibration
    while True:
        tmp = input()
        if tmp == "s":
            sys.exit()
        elif tmp == "r":
            is_calibration = True
        elif c != tmp:
            c = tmp
            print("c =", c)
        else:
            print("else")

if __name__ == "__main__":
    main()

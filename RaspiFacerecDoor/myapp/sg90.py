import RPi.GPIO as GPIO
import time
# import signal
import atexit

atexit.register(GPIO.cleanup)  

servopin = 38#橙色线PWM调制接38脚
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(servopin, GPIO.OUT, initial=False)


opentime=2#开放时间
angle=90#打开角度
startpos=7.8#确定舵机的初始位置
currentpos=0#当前位置
endpos=startpos+10*angle/180#完全打开状态的位置

def OpenDoor():
    print("Open the door")
    p = GPIO.PWM(servopin,50) #50HZ
    p.start(startpos)
    time.sleep(0.02)
    for i in range(0,(angle+1),1):
        currentpos=startpos+10*i/180
        p.ChangeDutyCycle(currentpos)
        time.sleep(0.02)
    for i in range(angle,-1,-1):
        currentpos=startpos+10*i/180
        p.ChangeDutyCycle(currentpos)
        time.sleep(0.02) 
    time.sleep(opentime)
    p.stop()
#OpenDoor()

#OpenDoor()

#atexit.register(GPIO.cleanup)
#导入GPIO库
import RPi.GPIO as GPIO
import time
 
#有关GPIO引脚的设备类,包括蜂鸣器\LED\超声波测距
class mygpio:

    #定义GPIO引脚,按照board

    #超声波测距引脚
    trig = 13
    echo = 11

    #各led引脚
    blueio=31
    yellowio=33
    greenio=35
    redio=37
    
    

    buzzerio=40
    
    def __init__(self):

        self.stopSign=0#需要多线程的方法加入此标识位用于杀死线程

        GPIO.setwarnings(False)
        #编号方式统一按照BOARD
        GPIO.setmode(GPIO.BOARD) 
  
        #设置各个引脚GPIO工作方式(IN/OUT)

        #超声波测距引脚
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        #蜂鸣器引脚
        GPIO.setup(self.buzzerio, GPIO.OUT)
        #LED引脚
        GPIO.setup(self.redio, GPIO.OUT)
        GPIO.setup(self.greenio, GPIO.OUT)
        GPIO.setup(self.blueio, GPIO.OUT)
        GPIO.setup(self.yellowio, GPIO.OUT)

  
    #超声波测距函数
    def distance(self):
        #发送高电平信号到Trig引脚
        GPIO.output(self.trig, True)
        #高电平需要持续10us 
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start_time = time.time()
        stop_time = time.time()
  
        #超声波发出的时刻
        while GPIO.input(self.echo) == 0:
            start_time = time.time()
  
        #收到返回的超声波时刻
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()
  
        #超声波的往返时间=返回-发出
        time_elapsed = stop_time - start_time
        #声速343m/s＝34300cm/s
        distance = (time_elapsed*34300) / 2
        print("Distance : "+str(distance))
        
        return distance
        


    #蓝灯闪烁t秒钟
    def blue(self,t=5):#t为闪烁的秒数
        self.stopSign=0
        while t>0:
            if self.stopSign == 1:
                GPIO.output(self.blueio, 0)   #引脚设低电平LED灭
                return
            else:
                GPIO.output(self.blueio, 1)   #引脚设高电平LED亮
                time.sleep(0.5)   #LED亮1秒
                GPIO.output(self.blueio, 0)   #引脚设低电平LED灭
                time.sleep(0.5)   #LED灭1秒
                t-=1

    #黄灯闪烁t秒钟
    def yellow(self,t=5):#t为闪烁的秒数
        self.stopSign=0
        while t>0:
            if self.stopSign == 1:
                GPIO.output(self.yellowio, 0)   #引脚设低电平LED灭
                return
            else:
                GPIO.output(self.yellowio, 1)   #引脚设高电平LED亮
                time.sleep(0.5)   #LED亮1秒
                GPIO.output(self.yellowio, 0)   #引脚设低电平LED灭
                time.sleep(0.5)   #LED灭1秒
                t-=1

    #红灯闪烁t秒钟
    def red(self,t=5):#t为闪烁的秒数
        self.stopSign=0
        while t>0:
            if self.stopSign == 1:
                GPIO.output(self.redio, 0)   #引脚设低电平LED灭
                return
            else:
                GPIO.output(self.redio, 1)   #引脚设高电平LED亮
                time.sleep(0.5)   #LED亮1秒
                GPIO.output(self.redio, 0)   #引脚设低电平LED灭
                time.sleep(0.5)   #LED灭1秒
                t-=1

    #绿灯闪烁t秒钟
    def green(self,t=5):#t为闪烁的秒数
        self.stopSign=0
        while t>0:
            if self.stopSign ==1:
                GPIO.output(self.greenio, 0)   #引脚设低电平LED灭
                return
            else:
                GPIO.output(self.greenio, 1)   #引脚设高电平LED亮
                time.sleep(0.5)   #LED亮1秒
                GPIO.output(self.greenio, 0)   #引脚设低电平LED灭
                time.sleep(0.5)   #LED灭1秒
                t-=1

    #结束led闪烁
    def killLED(self):
        self.stopSign=1

    #蜂鸣器急促鸣叫t秒钟
    def buzzer(self,t=5):
        while t>0 :
            GPIO.output(self.buzzerio, 1)   #将引脚的状态设置为高电平，此时蜂鸣器发声
            time.sleep(0.2)
            GPIO.output(self.buzzerio, 0)   #将引脚状态设置为低电平，此时蜂鸣器静默
            time.sleep(0.2)
            GPIO.output(self.buzzerio, 1)   #将引脚的状态设置为高电平，此时蜂鸣器发声
            time.sleep(0.2)
            GPIO.output(self.buzzerio, 0)   #将引脚状态设置为低电平，此时蜂鸣器静默
            time.sleep(0.4)
            t-=1

#mydev=mygpio()
#mydev.blue(5)
#mydev.yellow(3)
#mydev.green(3)
#mydev.red(3)

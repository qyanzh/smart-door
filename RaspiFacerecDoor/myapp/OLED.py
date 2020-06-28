import os
import sys
import random
import time

#oled驱动相关
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class OLEDshow:
    def __init__(self):
        """
        在需要以多线程形式调用的方法中，加入此stopSoge变量作为控制，
        在方法开始处将它初始化为0(方便关闭一个使用该方法的线程后再次开启一个同样使用该方法的线程),
        在循环中通过stopSign变量被cleanscreen方法置0来控制这个线程的结束
        """
        self.stopSign=0

        #获取设备
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial)

        #字体ttf文件放在font文件夹中
        #name是字体文件名,size为生成字体大小
        def make_font(name, size):
            font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', name))
            return ImageFont.truetype(font_path, size)

        #字体生成
        self.font32 = make_font("simhei.ttf", 32)
        self.font16 = make_font("simhei.ttf", 16)

    #显示姓名和测温提示
    def showname(self,namestr):
        strlen=len(namestr)
        pos=(int((128-strlen*32)/2),0)
        t=3
        while t>=0:
            with canvas(self.device) as draw:
                draw.text(pos, namestr, font=self.font32, fill="white")
            time.sleep(0.5)
            with canvas(self.device) as draw:
                draw.text((27,15), "请在"+str(t)+"秒内", font=self.font16, fill="white")
                draw.text((0,33), "将手腕移至探头前", font=self.font16, fill="white")
            time.sleep(0.5)
            t-=1
    #显示开始人脸检测
    def beginRec(self):
        self.stopSign=0
        t=5
        originstr=""
        while t>0:
            if self.stopSign==1:
                return
            with canvas(self.device) as draw:
                draw.text((0,15), "人脸检测", font=self.font32, fill="white")
                originstr=originstr+"＊"
                draw.text((23,46), originstr, font=self.font16, fill="white")
            time.sleep(0.5)
            t-=1
    #显示测温结果
    def showtemperature(self,namestr,temperature):
        strlen=len(namestr)
        pos=(int((128-strlen*32)/2)-1,0)
        strHigh="体温异常"
        strNormal="体温正常"
        if temperature > 37.2 :
            strTip=strHigh
        else:
            strTip=strNormal
        t=6
        while t>=0:
            with canvas(self.device) as draw:
                draw.text(pos, namestr, font=self.font32, fill="white")
                draw.text((20,32), "体温:"+str(temperature)+"℃", font=self.font16, fill="white")
                draw.text((20,48), strTip, font=self.font16, fill="white")
                time.sleep(0.5)
            t-=1
    
    #显示识别错误为非登记人员或者提示拍摄角度
    def showunkown(self):
        t=6
        while t>=0:
            with canvas(self.device) as draw:
                draw.text((31,0), "识别失败", font=self.font16, fill="white")
                draw.text((23,16), "您尚未注册", font=self.font16, fill="white")
                draw.text((55,32), "或", font=self.font16, fill="white")
                draw.text((0,48), "调整与摄像头距离", font=self.font16, fill="white")
                time.sleep(0.5)
            t-=1
    
    #显示测温失败提示
    def showtempError(self):
        t=6
        while t>=0:
            with canvas(self.device) as draw:
                draw.text((31,0), "测温异常", font=self.font16, fill="white")
                draw.text((0,16), "调整与测温头距离", font=self.font16, fill="white")
                draw.text((7,32), "请将手腕放置于", font=self.font16, fill="white")
                draw.text((7,48), "距测温头约2cm处", font=self.font16, fill="white")
                time.sleep(0.5)
            t-=1

    #显示失败提示
    def showError(self):
        t=6
        while t>=0:
            with canvas(self.device) as draw:
                draw.text((0,15), "测温失败", font=self.font32, fill="white")
                time.sleep(0.5)
            t-=1

    def cleanscreen(self):
        self.stopSign=1#杀死方法中包含这个变量的线程
        self.device.clear()
        
#OLED=OLEDshow()
#OLED.beginRec()
#OLED.showunkown()
#OLED.showtemperature("朱庆章",36.58)
#OLED.showtempError()
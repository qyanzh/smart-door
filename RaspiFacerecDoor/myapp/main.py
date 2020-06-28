#import待补充
import os
import cv2
import face_recognition
import numpy as np
import json
import time
import requests

#zqz
import threading
import OLED
import MyDev
import MLX90614BAA
import sg90

#全局变量
token=""
#获取当前文件路径，用于保存拍摄的图片
#图片保存路径在该py文件的下一级 pic 目录中

base_path = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(base_path,'pic/')
#需同步内容
number_list = []
name_list = []
imgencode_list = []

#zqz
#初始化OLED类
print("设备类初始化")
oled=OLED.OLEDshow()
mydev=MyDev.mygpio()
sensor=MLX90614BAA.MLX90614()

#main函数，无限循环
def main():
    #登录
    global token
    token=login()
    #在人脸加成之前进行数据同步
    sync()

    #循环testing检测函数
    while(1):
        testing()

#检测循环
def testing(): 
    #初始化检到符合要求距离的次数
    dis_cnt=0
    #超声波测距开始
    while(1):
        distance= mydev.distance()
        #判定距离是否在合适拍照的范围
        if(distance<50 and distance>30):
            dis_cnt+=1
        else:
            dis_cnt=0
        #连续检测到三次符合距离要求，跳出循环准备开始人脸检测
        if (dis_cnt==3):
            break
        #每隔0.5秒钟进行一次测距
        time.sleep(0.5)
    
    #开始人脸检测提示
    print("开始采集人脸数据进行识别")
    
    oled.cleanscreen()
    threadRec = threading.Thread(target=oled.beginRec)
    threadBlue=threading.Thread(target=mydev.blue)
    
    threadRec.start()
    threadBlue.start()
    
    #人脸识别循环
    #控制拍照识别次数 i
    i = 1
    name = "" #识别到的姓名
    number = "" #识别到的学号

    #如果使用本地图片测试去掉下一行注释
    #picpath = base_path + 'test3.jpg'
    
    while(1):
        #循环次数大于3，重新开始检测程序
        if(i == 4):
            #提示人脸检测失败,未发现人物头像,或为未注册陌生人
            oled.cleanscreen()
            oled.showunkown()
            oled.cleanscreen()      
            return
        #控制变量+1
        i = i + 1 

        #使用摄像头拍摄
        picpath = pic_take()
        #print(picpath)
        #检测
        name,number = face_re(picpath)
        print("RecName:"+name)
        if(name != "Unknown person"):
            #姓名正确
            #检测成功,跳出人脸检测循环,转接显示姓名和测温
            break
        else:
            #识别到未录入的陌生人或者无人
            #删除图片
            if os.path.exists(picpath):
                os.remove(picpath)

    #人脸检测通过
    #在小屏幕显示当前姓名
    oled.cleanscreen()
    mydev.killLED()
    oled.showname(name)
    oled.cleanscreen()
    print("识别成功,姓名为：" + name +" 下面进行温度检测")
    
    threadYellow=threading.Thread(target=mydev.yellow)
    threadYellow.start()

    #温度检测 循环
    #控制次数 j
    j = 1
    temperature = ""
    while(1):
        #循环次数大于3，结束温度检测循环
        if j == 4:
            oled.showtempError()
            oled.cleanscreen()
        if j==7:
            oled.showError()
            oled.cleanscreen()
            mydev.killLED()
            return
        #控制变量+1
        j = j + 1
        #测量温度
        temperature = sensor.getObjTemp()
        time.sleep(0.8)
        if(temperature >35):
            #测温正常结束循环
            mydev.killLED()
            break

    #显示温度
    oled.cleanscreen()
    oled.showtemperature(name,temperature)
    oled.cleanscreen()
    
    #温度判断
    if(temperature >35 and temperature < 37.2):
        #温度正常
        print("温度正常，姓名为：" + name + " 温度为：" + str(temperature))
        #绿灯闪烁5s
        threadGreen=threading.Thread(target=mydev.green)
        threadGreen.start()
        #舵机模拟开门
        sg90.OpenDoor()

    else:
        #温度异常
        print("温度异常，姓名为：" + name + " 温度为：" + str(temperature))
        #红灯闪烁+蜂鸣器警报5s
        threadRed=threading.Thread(target=mydev.red)
        threadRed.start()
        mydev.buzzer()

    #向后端发送本次检测信息
    test_message(number,temperature,picpath)
    
    #删除识别到的人脸图片
    if os.path.exists(picpath):
        os.remove(picpath)
    #硬件还原
    oled.cleanscreen()
    #总检测程序程序结束，return
    return

#登录
def login():
    url = "http://122.112.159.211/api/login"
    data = {
        "username": "zqz",
        "password": "zqz"
    }
    r = requests.post(url=url, data=data)
    r=r.json()
    if(len(r)!=0):
        print("登录成功")
    return str(r["token"])
#数据同步 
def sync():
    print("开始从后端同步人脸数据")
    global number_list,name_list,imgencode_list
    number_list = []
    name_list = []
    imgencode_list = []
    url = "http://122.112.159.211/api/sync"
    headers={"Authorization" : "Bearer "+token}
    r = requests.get(url=url,headers=headers)
    datalist = r.json()
    if(len(datalist)!=0):
        print("同步成功")
    for item in datalist:
        name_list.append(item['name'])
        number_list.append(item['number'])
        imgencode_list.append(json.loads(item['vector']))
    return

#调用摄像头拍照
def pic_take():
    #用cv2实现，具体效果有待测试
    nowtime = str(int(time.time()))
    pic_path = base_path + nowtime + ".jpg"
    cap = cv2.VideoCapture(0) #自带摄像头改为0
    if(cap.isOpened()):
        ret,frame = cap.read()
        cv2.imwrite(pic_path,frame)
    cap.release()
    #返回图片保存地址
    return pic_path

#人脸检测 参数图片路径
def face_re(pic_path):
    name = "Unknown person"
    number = ""
    #返回姓名
    #如果未能匹配正确姓名 name = "Unknown person"
    unknown_image = face_recognition.load_image_file(pic_path)
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(imgencode_list, face_encoding)
        face_distances = face_recognition.face_distance(imgencode_list, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = name_list[best_match_index]
            number = number_list[best_match_index]
    return name,number

#向后端发送检测信息  参数 学号，温度，图像图片
def test_message(number,temperature,pic_path):
    url = "http://122.112.159.211/api/sign"
    files = {'photo': open(pic_path, 'rb')}           
    data = {'temperature':temperature,'number':number}  
    headers={"Authorization" : "Bearer "+token}
    response = requests.post(url, files=files, data=data,headers=headers)
    print(response.text)
    return

main() #调用main函数

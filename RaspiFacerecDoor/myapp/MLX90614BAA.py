import smbus
from time import sleep

class MLX90614():
    
    address=0x5a#传感器的默认地址是0x5a
    MLX90614_Ta=0x06#环境温度地址
    MLX90614_Tobj1=0x07#测量对象温度地址Tobj1
    #因为BAA是单IR版本故测量对象温度仅有Tobj1

    #自动重试读取次数,自动重试超过此次数则报错
    retry = 5
    #读取失败休眠时间
    sleeptime = 0.1

    #初始化函数
    def __init__(self, address=0x5a):
        self.bus = smbus.SMBus(1)#4B的i2c位于/dev/I2C-1

    def readRegister(self, regAddress):
        err = None
        for i in range(self.retry):
            try:
                return self.bus.read_word_data(self.address, regAddress)
            except IOError as e:
                err = e
                sleep(self.sleeptime)
        raise err

    #寄存器数据转摄氏度
    def toCelsius(self, data):
        temp = (data*0.02) - 273.15
        return temp
    
    #传感器自身温度
    def getSelfTemp(self):
        data = self.readRegister(self.MLX90614_Ta)
        return self.toCelsius(data)
    
    #测量对象温度
    def getObjTemp(self):
        data = self.readRegister(self.MLX90614_Tobj1)
        res=round(self.toCelsius(data),2)
        print("ObjTemp = "+str(res))
        return res


#if __name__ == "__main__":
#    sensor = MLX90614()
#    print("Self: %.2f"%(sensor.getSelfTemp()))
#    print("Object: %.2f"%(sensor.getObjTemp()))

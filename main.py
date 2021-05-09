from machine import SoftI2C, Pin, PWM
from mpu6050 import MPU6050
from time import sleep
from tvc import TVC


class test():
    
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.accel = MPU6050(self.i2c)
        self.cal_coeff = self.accel.calibrate(threshold=5)
        print('----------Calibration Complete----------')
        self.p4 = Pin(18)
        self.p5 = Pin(19)
        self.servo = PWM(self.p4, freq=50)
        self.servo2 = PWM(self.p5, freq=50)
        self.tvc = TVC((87,35,110),(87,55,110),self.servo,self.servo2)
        #self.initialize_servo()
    
    def run(self):

        self.to_csv(filename='data.txt')
        #file = open('data.txt','w')
        #for i in range(1000):
            #file.write(str(accel.get_values()))
        #    file.write(str(accel.get_smoothed_values(calibration=True))+'\n')
            #print(accel.get_smoothed_values(calibration=True))
            
        #file.close()

    def to_csv(self, filename, iterations=1000):
        
        result = self.accel.get_smoothed_values(calibration=self.cal_coeff)
        with open(filename,'w') as file:
            file.write(','.join(result.keys())+'\n')
            for _ in range(iterations):
                result = self.accel.get_smoothed_values(calibration=self.cal_coeff)
                vals = []
                for key, value in result.items():
                    vals.append(str(value))
                print(vals)
                file.write(','.join(vals)+'\n')
                
    def move(self,duty1=87,duty2=87):
        self.servo.duty(duty1)
        self.servo2.duty(duty2)
    
    def loop(self):
        for _ in range(1000):
            pos = self.accel.get_filtered_values(calibration=self.cal_coeff)
            ac_x = pos['aX']
            ac_y = pos['aY']
            self.move(self.constrain_x(ac_x),self.constrain_y(ac_y))
            #print(ac_x, self.cal_coeff['AcX'])
        
    def initialize_servo(self):
        INIT_STATE_X = 87
        MAX_X = 110
        MIN_X = 35
        
        INIT_STATE_Y = 87
        MAX_Y = 110
        MIN_Y = 55
        
        self.move(MIN_X,MIN_Y)
        sleep(1)
        self.move(MAX_X,MAX_Y)
        sleep(1)
        self.move(INIT_STATE_X,INIT_STATE_Y)
        
    def constrain_x(self, x):
        val = 87 + int(x//10)
        
        if val > 110:
            return 110
        elif val < 35:
            return 35
        elif val - 87 < 3:
            return 87
        else:
            return val
        
    def constrain_y(self, y):
        val = 87 + int(y//10)
        
        if val > 110:
            return 110
        elif val < 55:
            return 55
        elif val - 87 < 3:
            return 87
        else:
            return val


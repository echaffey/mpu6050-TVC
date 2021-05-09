from machine import SoftI2C, Pin, PWM
from mpu6050 import MPU6050
from time import sleep
from tvc import TVC


class test():
    
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.mpu = MPU6050(self.i2c)
        self.cal_coeff = self.mpu.calibrate(threshold=10)

        self.p4 = Pin(18)
        self.p5 = Pin(19)
        self.servo = PWM(self.p4, freq=50)
        self.servo2 = PWM(self.p5, freq=50)
        self.tvc = TVC((87,55,110),(87,35,110),(self.servo2,self.servo))
        #self.initialize_servo()
    
    def run(self):

        self.to_csv(filename='data.txt')

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
    
    def loop(self):
        for _ in range(1000):
            pos = self.accel.get_filtered_values(calibration=self.cal_coeff)
            ac_x = pos['aX']
            ac_y = pos['aY']
            self.tvc.move(axis=0,duty_value=ac_x)
            self.tvc.move(axis=1,duty_value=ac_y)
            #print(ac_x, self.cal_coeff['AcX'])


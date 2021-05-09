from machine import SoftI2C, Pin
import MPU6050
from time import sleep


class test():
    
    def __init__(self):
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.accel = MPU6050.accel(self.i2c)
        self.accel.calibrate()
        print('----------Calibration Complete----------')
    
    def run(self):

        self.to_csv(filename='data.txt')
        #file = open('data.txt','w')
        #for i in range(1000):
            #file.write(str(accel.get_values()))
        #    file.write(str(accel.get_smoothed_values(calibration=True))+'\n')
            #print(accel.get_smoothed_values(calibration=True))
            
        #file.close()

    def to_csv(self, filename, iterations=10):
        
        result = self.accel.get_smoothed_values(calibration=True)
        with open(filename,'w') as file:
            file.write(','.join(result.keys())+'\n')
            for _ in range(iterations):
                result = self.accel.get_smoothed_values(calibration=True)
                vals = []
                for key, value in result.items():
                    vals.append(str(value))
                print(vals)
                file.write(','.join(vals)+'\n')



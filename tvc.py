from time import sleep
from machine import PWM
from mpu6050 import MPU6050


class TVC():

    def __init__(self, x_params:tuple, y_params:tuple, motors):

        # Initialize servo duty starting and range values.
        self.POS_X_INIT, self.POS_X_MIN, self.POS_X_MAX = x_params
        self.POS_Y_INIT, self.POS_Y_MIN, self.POS_Y_MAX = y_params

        # Assign servo motors.
        self.AXIS_X  = 0
        self.AXIS_Y  = 1
        self.MOTOR   = [m for m in motors]
        self.MOTOR_X = self.MOTOR[0]#motor_x
        self.MOTOR_Y = self.MOTOR[1]#motor_y

        # Initialize sensors.

        # Start motion sweep across servo functional range.
        self._motion_check()

    def add_sensor(self, sensor=None):
        pass

    def _motion_check(self)->None:
        '''Runs a motion check to the end ranges of each axis motor individually before
        returning them to thier initial states.'''
        
        for time in list((1.5,0.5)):
            # Check X range.
            self.MOTOR_X.duty(self.POS_X_MIN)
            sleep(time)
            self.MOTOR_X.duty(self.POS_X_MAX)
            sleep(time)
            self.MOTOR_X.duty(self.POS_X_INIT)
            sleep(time)

            # Check Y range.
            self.MOTOR_Y.duty(self.POS_Y_MIN)
            sleep(time)
            self.MOTOR_Y.duty(self.POS_Y_MAX)
            sleep(time)
            self.MOTOR_Y.duty(self.POS_Y_INIT)
            sleep(time)

    def move(self, axis:int=None, duty_value:int=None)->None:
        '''Moves the servo specified by `axis` to the position assigned by `duty_value`'''
        self.MOTOR[axis].duty(self._constrain(axis,duty_value))
        
        #if axis == 0:
        #    self.MOTOR_X.duty(self._constrain(self.AXIS_X,duty_value))
        #elif axis == 1:
        #    self.MOTOR_Y.duty(self._constrain(self.AXIS_Y,duty_value))

    def _constrain(self,axis:int=None,val:int=0)->int:
        '''Confine the position of the motor to its defined working range.
            :axis: X=0, Y=1.
            :val: Duty value for desired motor position.
        '''
        # X axis.
        if axis == 0:
            pos = self.POS_X_INIT + int(val//10)
            if pos > self.POS_X_MAX:
                return self.POS_X_MAX
            elif pos < self.POS_X_MIN:
                return self.POS_X_MIN
            elif pos - val < 3:
                return self.POS_X_INIT
            else:
                return pos
        # Y axis.
        elif axis == 1:
            pos = self.POS_Y_INIT - int(val//10)
            if pos > self.POS_Y_MAX:
                return self.POS_Y_MAX
            elif pos < self.POS_Y_MIN:
                return self.POS_Y_MIN
            elif pos - val < 3:
                return self.POS_Y_INIT
            else:
                return pos

    def run(self)->None:
        pass

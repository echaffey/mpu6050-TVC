import machine


class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.iic.stop()
        self.vals = {}

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self,accel=True,gyro=True,temp=True):
        raw_ints = self.get_raw_values()
        vals = {}
        if accel:
            vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
            vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
            vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        if temp:
            vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        if gyro:
            vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
            vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
            vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        self.vals = vals
        return vals  # returned in range of Int16
        # -32768 to 32767
        
    def get_accel(self):
      _ = self.get_values(gyro=None,temp=None)
      return self.vals
    #   return {self.vals["AcX"], self.vals["AcY"], self.vals["AcZ"]}
    
    def get_gyro(self):
        _ = self.get_values(accel=None,temp=None)
        return self.vals
        # return {self.vals['GyX'], self.vals['GyY'], self.vals['GyZ']}

    def get_temp(self):
        _ = self.get_values(accel=None,gyro=None)
        return self.vals
        # return self.vals['Tmp']

    def calibrate(self, threshold=10):
        """
        Get calibration date for the sensor, by repeatedly measuring
        while the sensor is stable. The resulting calibration
        dictionary contains offsets for this sensor in its
        current position.
        """
        while True:
            a_val1 = self.get_accel()
            a_val2 = self.get_accel()
            # Check all consecutive measurements are within
            # the threshold. We use abs() so all calculated
            # differences are positive.
            if all(abs(a_val1[key] - a_val2[key]) < threshold for key in a_val1.keys()):
                self.calibration = a_val1
                return a_val1  # Calibrated.
    
    def get_smoothed_values(self, n_samples=20, calibration=None):
        """
        Get smoothed values from the sensor by sampling
        the sensor `n_samples` times and returning the mean.

        If passed a `calibration` dictionary, subtract these
        values from the final sensor value before returning.
        """
        result = {}
        for _ in range(n_samples):
            data = self.get_values()

            for key in data.keys():
                # Add on value / n_samples to produce an average
                # over n_samples, with default of 0 for first loop.
                result[key] = result.get(key, 0) + (data[key] / n_samples)

        if calibration:
            # Remove calibration adjustment.
            for key in calibration.keys():
                result[key] -= calibration[key]

        return result

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)


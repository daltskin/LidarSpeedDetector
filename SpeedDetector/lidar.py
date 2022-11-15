import time

class SpeedDetector:
    def __init__(self, serial):
        self.serial = serial

    def setup_serial(self):
        ser = self.serial
        ser.write(0x42)
        ser.write(0x57)
        ser.write(0x02)
        ser.write(0x00)
        ser.write(0x00)
        ser.write(0x00)
        ser.write(0x01)
        ser.write(0x06)
        return ser

    def calc_distance(self, distances):
        total_distance = 0

        if len(distances) > 0:
            total_distance = max(distances) - min(distances)
        return total_distance

    def calc_speed(self, distance, interval):
        speed_cms = distance / (interval / 1000)
        return speed_cms

    def convert_cms_mph(self, speed_cms):
        return speed_cms / 44.704
    
    def convert_cms_kmh(self, speed_cms):
        return speed_cms * 0.036

    def read_sensor(self, interval):
        distances = []

        # read serial data over given interval
        end_time = time.time() + interval / 1000
        while time.time() < end_time:
            # Sensor readings contain 9 data frames
            while self.serial.in_waiting >= 9:
                # First 2 bytes are header
                if (b'Y' == self.serial.read()) and ( b'Y' == self.serial.read()):
                    distance_l = self.serial.read()
                    distance_h = self.serial.read()
                    distance_total = (ord(distance_h) * 256) + (ord(distance_l))
                    strength_l = self.serial.read()
                    strength_h = self.serial.read()
                    credibility = self.serial.read()
                    checksum = self.serial.read()
                    # for i in range (0,5):
                    #     self.serial.read()
                        
                    if ord(credibility) == (7 or 8):
                        distances.append(distance_total)
                    # else:
                    #     print(f"Sensor data not credible: {ord(credibility)}" )
        return distances
    
import datetime
import time
import serial
import pyfiglet
from SpeedDetector import lidar

# WSL
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 1)

# Windows
#ser = serial.Serial('COM5', 115200, timeout = 1)

sensor = lidar.SpeedDetector(ser)

SAMPLE_MS = 50
REFRESH_MS = 1000

while True:
    top_kmh = []
    # read serial data over given period
    end_time = time.time() + REFRESH_MS / 1000
    while time.time() < end_time:
        distances = sensor.read_sensor(SAMPLE_MS)
        total_distance = sensor.calc_distance(distances)
        cms = sensor.calc_speed(total_distance, SAMPLE_MS)
        mph = sensor.convert_cms_mph(cms)
        kmh = sensor.convert_cms_kmh(cms)
        # Store all speeds
        top_kmh.append(kmh)
        if kmh != 0:
            # Display sensor outputs
            print(f"{datetime.datetime.now()} Speed: {round(kmh, 2)} kmh Distance: {total_distance} cms Current: {distances[-1]} cm Max: {max(distances)} cm Min: {min(distances)} cm Datapoints: {len(distances)} ")
    if max(top_kmh) >0:
        pyfiglet.print_figlet(f"Top: {round(max(top_kmh),2)} kmh", colors = "GREEN")
        pyfiglet.print_figlet(f"Avg: {round(sum(top_kmh)/len(top_kmh),2)} kmh", colors = "GREEN")
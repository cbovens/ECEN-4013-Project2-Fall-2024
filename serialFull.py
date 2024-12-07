import serial
import time
import re
import os

#BNO055 IMU lib
import board
import adafruit_bno055

#Pigpio import (for GPS)
import pigpio

#CSV import
import csv
from collections import deque

# Define the CSV file name
csv_file = 'sensor_data.csv'

# Write the CSV header if the file doesn't exist
if os.path.exists(csv_file):
    os.remove(csv_file)
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    header = ["Timestamp", "Longitude", "Latitude", "Altitude", "Satellites", "AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ", "MagX", "MagY", "MagZ"]
    writer.writerow(header)  # File already exists, no need to write the header again

#IMU Setup
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

#GPS Setup
SOFT_UART_TX = 27  # GPIO pin for TX (connect to GPS RX)
SOFT_UART_RX = 17  # GPIO pin for RX (connect to GPS TX)
BAUD_RATE = 9600

# Define the UART port and baud rate
uart_port = '/dev/serial0'  # Default UART port on Raspberry Pi
baud_rate = 9600            # Baud rate

usb_port = '/dev/ttyGS0'  # Default UART port on Raspberry Pi

# Create a serial connection
ser = serial.Serial(uart_port, baud_rate)
usb = serial.Serial(usb_port, baud_rate)

# Set up software serial (UART) using pigpio
pi = pigpio.pi()
pi.bb_serial_read_open(SOFT_UART_RX, BAUD_RATE)  # Open RX pin for reading

# Initialize a deque to store the last 50 data points
buffer_size = 50
data_buffer = deque(maxlen=buffer_size)


def nmea_to_decimal(coord, direction):
    if coord == '':
        return 'No Data'
    try:
        degrees = float(coord[:2])
        minutes = float(coord[2:]) / 60
        decimal = degrees + minutes
        return decimal if direction in ['N', 'E'] else -decimal
    except ValueError:
        return 'No Data'

# Write the message to the UART
long =  0
height = 0
ay = 0
lat = 0
ax = 0
az = 0
sat= 0
gx= 0
gy= 0
gz= 0
mx= 0
my= 0
mz= 0
try:
   
    while (True):
        print("gps test")
        (count, data) = pi.bb_serial_read(SOFT_UART_RX)
        print(count)
        if count > 0:
            # Decode and process GPS data (NMEA sentences)
            nmea_data = data.decode('ascii', errors='ignore').splitlines()
            for line in nmea_data:
                if line.startswith("$GPGGA"):  # Parse GGA sentences
                    parts = line.split(',')
                    if len(parts) >= 10:
                        lat = nmea_to_decimal(parts[2], parts[3])
                        long = nmea_to_decimal(parts[4], parts[5]) - 76.3337783333
                        height = float(parts[9]) if parts[9] else 0
                        lat = 0 if lat == 'No Data' else lat
                        long = 0 if long == 'No Data' else long        

                elif line.startswith("$GPGSV"):  # Parse GSV sentences for satellite data
                    parts = line.split(',')
                    if len(parts) > 3:
                        old_sat = sat
                        sat = re.sub(r"\D", "", parts[3])
                        sat = int(sat) if int(sat) <= 20 else old_sat
        ax = sensor.acceleration[0]
        ay = sensor.acceleration[1]
        az = sensor.acceleration[2]
        gx = sensor.gyro[0]
        gy = sensor.gyro[1]
        gz = sensor.gyro[2]
        mx = sensor.magnetic[0]
        my = sensor.magnetic[1]
        mz = sensor.magnetic[2]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        time.sleep(0.5)
        
        # Append the new data point to the deque
        data_point = [timestamp, long or 0, lat or 0, height or 0, sat or 0, ax or 0, ay or 0, az or 0, gx or 0, gy or 0, gz or 0, mx or 0, my or 0, mz or 0]
        data_buffer.append(data_point)

        # Write the data point to the CSV file
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)  # Write the header again
            writer.writerows(data_buffer)  # Write the contents of the deque
            
        # Message syntax each being 8 bytes:
        #   Longitude, Latitiude, Altitude, AccX, AccY, AccZ
        print(lat, long, height)
        #print(type(long), type(lat), type(height), type(sat), type(ax), type(ay), type(az), type(gx), type(gy), type(gz), type(mx), type(my), type(mz))
        message = "%8f %8f %8f %8f %8f %8f %8f %8f %8f %8f %8f %8f %8f\n" % (long or 0, lat or 0, height or 0, sat or 0, ax or 0, ay or 0, az or 0, gx or 0, gy or 0, gz or 0, mx or 0, my or 0, mz or 0)
        ser.write(message.encode('utf-8'))
        print("after long")
        usb.write(message.encode('utf-8'))
        print("After usb")
        #print(type(long), type(lat), type(height), type(sat), type(ax), type(ay), type(az), type(gx), type(gy), type(gz), type(mx), type(my), type(mz))

# Close the serial connection
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    # Clean up
    pi.bb_serial_read_close(SOFT_UART_RX)
    pi.stop()
    ser.close()
    print("Closed software UART and cleaned up resources.")
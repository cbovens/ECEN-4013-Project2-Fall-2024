import serial
import time

#BNO055 IMU lib
import board
import adafruit_bno055

#Pigpio import (for GPS)
import pigpio

#IMU Setup
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

#GPS Setup
SOFT_UART_TX = 17  # GPIO pin for TX (connect to GPS RX)
SOFT_UART_RX = 27  # GPIO pin for RX (connect to GPS TX)
BAUD_RATE = 9600



# Define the UART port and baud rate
uart_port = '/dev/serial0'  # Default UART port on Raspberry Pi
baud_rate = 9600            # Baud rate

# Create a serial connection
ser = serial.Serial(uart_port, baud_rate)

# Set up software serial (UART) using pigpio
pi = pigpio.pi()
pi.bb_serial_read_open(SOFT_UART_RX, BAUD_RATE)  # Open RX pin for reading


# Write the message to the UART
count = 0
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
        count = count + 1
        long = 0
        height = 0
        lat = 0
        sat = 0
        ax = sensor.acceleration[0]
        ay = sensor.acceleration[1]
        az = sensor.acceleration[2]
        gx = sensor.gyro[0]
        gy = sensor.gyro[1]
        gz = sensor.gyro[2]
        mx = sensor.magnetic[0]
        my = sensor.magnetic[1]
        mz = sensor.magnetic[2]
        time.sleep(0.5)
        # Message syntax each being 8 bytes:
        #   Longitude, Latitiude, Altitude, AccX, AccY, AccZ
        message = "%8f %8f %8f %8f %8f %8f %8f %8f %8f %8f %8f %8f %8f\n" % (long,lat,height,sat,ax,ay,az,gx,gy,gz,mx,my,mz)
        ser.write(message.encode('utf-8'))
        long2 = "%08f\r" % (long)
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
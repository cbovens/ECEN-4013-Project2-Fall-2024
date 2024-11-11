import serial
import time

# Define the UART port and baud rate
uart_port = '/dev/serial0'  # Default UART port on Raspberry Pi
baud_rate = 9600            # Baud rate

# Create a serial connection
ser = serial.Serial(uart_port, baud_rate)

# Message to send

# Write the message to the UART
count = 0
long = 100
height = 100
ay = 100
lat = 0
ax = 0
az = 0
while (True):
    count = count + 1
    
    # Message syntax each being 8 bytes:
    #   Longitude, Latitiude, Altitude, AccX, AccY, AccZ
    message = "%8f%8f%8f%8f%8f%8f\n" % (long,lat,height,ax,ay,az)
    ser.write(message.encode('utf-8'))
    long2 = "%08f\r" % (long)
    print(long2, end="")
    long -= 0.1
    height -= 0.1
    ay -= 0.1
    lat += 0.1
    ax += 0.1
    az += 0.00001
    time.sleep(0.5)

# Close the serial connection
ser.close()
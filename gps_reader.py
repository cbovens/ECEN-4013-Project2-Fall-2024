import pigpio
import serial
import time

# Configuration for pigpio and the GPS
SOFT_UART_TX = 17  # GPIO pin for TX (connect to GPS RX)
SOFT_UART_RX = 27  # GPIO pin for RX (connect to GPS TX)
BAUD_RATE = 9600   # Default baud rate for the PA1616S GPS module

# Initialize pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Unable to connect to pigpio daemon. Is it running?")

# Set up software serial (UART) using pigpio
pi.bb_serial_read_open(SOFT_UART_RX, BAUD_RATE)  # Open RX pin for reading

print("Software UART initialized. Reading GPS data...")

# Initialize variables for parsing GPS data
last_nSat = 'No Data'

# Function to safely convert NMEA coordinates to decimal degrees
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

try:
    while True:
        # Read data from the software UART
        (count, data) = pi.bb_serial_read(SOFT_UART_RX)
        if count > 0:
            # Decode and process GPS data (NMEA sentences)
            nmea_data = data.decode('ascii', errors='ignore').splitlines()
            for line in nmea_data:

                if line.startswith("$GPGGA"):  # Parse GGA sentences
                    parts = line.split(',')
                    if len(parts) >= 10:
                        latitude = parts[2]
                        longitude = parts[4]
                        elevation = parts[9]

                        latitude = nmea_to_decimal(latitude, parts[3])
                        longitude = nmea_to_decimal(longitude, parts[5])
                        elevation = float(elevation) if elevation else 'No Data'

                        # Print GPS data
                        print(f"Latitude: {latitude}")
                        print(f"Longitude: {longitude}")
                        print(f"Elevation: {elevation} meters")
                        print(f"Number of locked satellites: {last_nSat}")
                    else:
                        print("Invalid GGA sentence received.")

                elif line.startswith("$GPGSV"):  # Parse GSV sentences for satellite data
                    parts = line.split(',')
                    if len(parts) > 3:
                        last_nSat = parts[3]  # Update the number of locked satellites
                    else:
                        print("Invalid GSV sentence received.")
                    print(f"Number of Satellites: {last_nSat}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up
    pi.bb_serial_read_close(SOFT_UART_RX)
    pi.stop()
    print("Closed software UART and cleaned up resources.")

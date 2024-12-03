"""
This code recieves data via Bluetooth connectivity
Libraries needed: serial, tkinter
PC must be paired with HC-06
To pair on Win11, in bluetooth settings>bluetooth&devices>devices>bluetooth devices discovery>advanced
    then pair like normal, selecting HC-06 from options
Ensure the COM port is corect. To check, settings>bluetooth&devices>devices>more bluetooth settings>COM ports>find the one with "HC-06 'Serial Port'"
    Put that number in the com_port variable
Baud rate is 9600 which is hardcoded to HC-06 module
Data will be automatically put into GUI, provided the data is shared in the below format
"%8f%8f%8f%8f%8f%8f" % (longitude, latitude, altitude, accelerationX, accelerationY, acceleration Z)
Run code, and hit "Start" to begin data updating. Press "Stop" to have the data stop updating. "Close" to exit the GUI and program.
"""
import serial
import serial.tools.list_ports as port_list
import tkinter as tk

# List available ports
ports = list(port_list.comports())
for p in ports:
    print(p)

# Initialize variables
(
    longVal, latVal, heightVal, axVal, ayVal, azVal,
    satVal, gxVal, gyVal, gzVal, mxVal, myVal, mzVal
) = [0] * 13

# Define the COM port and baud rate
com_port = 'COM3'  # Replace with your COM port
baud_rate = 9600   # Default baud rate for HC-06

# Create a window
window = tk.Tk()
window.title("Live Variable Values")
window.geometry("400x500")

# Define variables to display
variables = {
    "Latitude": tk.StringVar(),
    "Longitude": tk.StringVar(),
    "Height": tk.StringVar(),
    "Sat": tk.StringVar(),
    "Ax": tk.StringVar(),
    "Ay": tk.StringVar(),
    "Az": tk.StringVar(),
    "Gx": tk.StringVar(),
    "Gy": tk.StringVar(),
    "Gz": tk.StringVar(),
    "Mx": tk.StringVar(),
    "My": tk.StringVar(),
    "Mz": tk.StringVar(),
}

# Initialize GUI variables
for key in variables:
    variables[key].set(f"{key}: N/A")

# Create a serial connection
try:
    ser = serial.Serial(com_port, baud_rate, timeout=1)
    print(f"Connected to {com_port}")
except serial.SerialException as e:
    print(f"Error: {e}")
    ser = None

# Flag to control displaying
displaying = False

# Function to start displaying
def start_displaying():
    global displaying
    displaying = True

# Function to stop displaying
def stop_displaying():
    global displaying
    displaying = False

# Function to close window
def close_window():
    if ser:
        ser.close()
    window.destroy()

# Function to read and update serial data
def update_values():
    global displaying
    if ser and ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received Data: {data}\r", end = "")
            # Parse the space-separated data
            values = list(map(float, data.split()))
            if len(values) == 13:
                (
                    longVal, latVal, heightVal, satVal, axVal, ayVal, azVal,
                    gxVal, gyVal, gzVal, mxVal, myVal, mzVal
                ) = values
                
                # Update GUI variables
                if displaying:
                    variables["Longitude"].set(f"Longitude: {longVal:.6f}")
                    variables["Latitude"].set(f"Latitude: {latVal:.6f}")
                    variables["Height"].set(f"Height: {heightVal:.6f}")
                    variables["Sat"].set(f"Sat: {satVal}")
                    variables["Ax"].set(f"Ax: {axVal:.6f}")
                    variables["Ay"].set(f"Ay: {ayVal:.6f}")
                    variables["Az"].set(f"Az: {azVal:.6f}")
                    variables["Gx"].set(f"Gx: {gxVal:.6f}")
                    variables["Gy"].set(f"Gy: {gyVal:.6f}")
                    variables["Gz"].set(f"Gz: {gzVal:.6f}")
                    variables["Mx"].set(f"Mx: {mxVal:.6f}")
                    variables["My"].set(f"My: {myVal:.6f}")
                    variables["Mz"].set(f"Mz: {mzVal:.6f}")
            else:
                print(f"Invalid data length: {len(values)} (expected 13)")
        except (ValueError, UnicodeDecodeError) as e:
            print(f"Error parsing data: {e}")
    
    # Schedule the next update
    window.after(400, update_values)

# Create labels to display variable values
for key in variables:
    tk.Label(window, textvariable=variables[key]).pack()

# Create buttons to start and stop displaying
start_button = tk.Button(window, text="Start", command=start_displaying)
stop_button = tk.Button(window, text="Stop", command=stop_displaying)
close_button = tk.Button(window, text="Close", command=close_window)

start_button.pack()
stop_button.pack()
close_button.pack()

# Start updating values and displaying values
window.after(400, update_values)

# Run the Tkinter event loop
window.mainloop()
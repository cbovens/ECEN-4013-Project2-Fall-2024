"""
This code recieves data via Bluetooth connectivity
Libraries needed: serial, tkinter

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

longVal = 0
latVal = 0
heightVal = 0
axVal = 0
ayVal = 0
azVal = 0

# Define the COM port and baud rate
com_port = 'COM8'  # Replace with your COM port
baud_rate = 9600   # Default baud rate for HC-06

# Create a window
window = tk.Tk()
window.title("Live Variable Values")
window.geometry("244x244")

# Define variables to display
lat = tk.StringVar()
long = tk.StringVar()
height = tk.StringVar()
ax = tk.StringVar()
ay = tk.StringVar()
az = tk.StringVar()

# Initialize variables with default values
lat.set("Latitude: N/A")
long.set("Longitude: N/A")
height.set("Height: N/A")
ax.set("Ax: N/A")
ay.set("Ay: N/A")
az.set("Az: N/A")

# Create a serial connection
ser = serial.Serial(com_port, baud_rate)

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
    window.destroy()


# Function to read and update serial data
def update_values():
    value_length = 9
    global longVal, latVal, heightVal, axVal, ayVal, azVal, displaying
    while ser.in_waiting >= 0:
        data = ser.readline().decode('utf-8').strip()
        print(f"\rReceived Data: {data}")
        if len(data) >= 53:
            # Slice the data into 6 parts
            values = [
                float(data[0:value_length]),   # First value
                float(data[value_length:2*value_length]),  # Second value
                float(data[2*value_length:3*value_length]),  # Third value
                float(data[3*value_length:4*value_length]),  # Fourth value
                float(data[4*value_length:5*value_length]),  # Fifth value
                float(data[5*value_length:6*value_length])   # Sixth value
            ]
            longVal, latVal, heightVal, axVal, ayVal, azVal = values
        break
    # Schedule the next update
    window.after(400, update_values)

# Function to update the displayed values on the GUI
def display_values():
    if displaying:
        long.set(f"Longitude: {longVal}")
        lat.set(f"Latitude: {latVal}")
        height.set(f"Height: {heightVal}")
        ax.set(f"Ax: {axVal}")
        ay.set(f"Ay: {ayVal}")
        az.set(f"Az: {azVal}")
    
    # Schedule the next update of the display
    window.after(500, display_values)

# Create labels to display variable values
label1 = tk.Label(window, textvariable=lat)
label2 = tk.Label(window, textvariable=long)
label3 = tk.Label(window, textvariable=height)
label4 = tk.Label(window, textvariable=ax)
label5 = tk.Label(window, textvariable=ay)
label6 = tk.Label(window, textvariable=az)

# Create buttons to start and stop displaying
start_button = tk.Button(window, text="Start", command=start_displaying)
stop_button = tk.Button(window, text="Stop", command=stop_displaying)
close_button = tk.Button(window, text="Close", command=close_window)

# Pack the labels and buttons into the window
label1.pack()
label2.pack()
label3.pack()
label4.pack()
label5.pack()
label6.pack()
start_button.pack()
stop_button.pack()
close_button.pack()

# Start updating values and displaying values
window.after(400, update_values)
window.after(500, display_values)

# Run the Tkinter event loop
window.mainloop()

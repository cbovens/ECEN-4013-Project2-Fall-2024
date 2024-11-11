# ECEN-4013-Project2-Fall-2024
Repo intended for housing programs &amp; code for the second project of design of engineering systems.

# Total libraries needed
pyserial, tkinter

# serial_BT.py
Code to send Bluetooth data  
Libraries needed: serial  
Send format: "%8f%8f%8f%8f%8f%8f" % (longitude, latitude, altitude, accelerationX, accelerationY, acceleration Z)  

# readBT.py
Code to receive Bluetooth data and show GUI.  
Libraries needed: serial, tkinter  
PC must be paired with HC-06  
To pair on Win11, in bluetooth settings>bluetooth&devices>devices>bluetooth devices discovery>advanced then pair like normal, selecting HC-06 from options  
Ensure the COM port is corect. To check, settings>bluetooth&devices>devices>more bluetooth settings>COM ports>find the one with "HC-06 'Serial Port'" Put that number in the com_port variable  
Baud rate is 9600 which is hardcoded to HC-06 module  
Data will be automatically put into GUI, provided the data is shared in the below format  
"%8f%8f%8f%8f%8f%8f" % (longitude, latitude, altitude, accelerationX, accelerationY, acceleration Z)  
Run code, and hit "Start" to begin data updating. Press "Stop" to have the data stop updating. "Close" to exit the GUI and program.  

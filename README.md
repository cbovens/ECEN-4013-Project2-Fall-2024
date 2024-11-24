# ECEN-4013-Project2-Fall-2024
Repo intended for housing programs &amp; code for the second project of design of engineering systems.

# For final build
Add 'dtoverlay=dwc2' to config.txt file (serial_USB.py). Add 'modules-load=g_serial' to cmdline file (serial_USB.py)  
To have commands run on startup: edit /etc/rc.local file. Add command (ex: 'python /path/to/code/serial_BT.py') right before the ending line. Ensure a new line between added code and end of flie statement.  

# Total libraries needed
pip install pyserial
pip install serial
pip install tk

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

# serial_USB.py
Code to send USB data  
Libraries needed: serial, time  
Send format: "%8f%8f%8f%8f%8f%8f" % (longitude, latitude, altitude, accelerationX, accelerationY, acceleration Z)  
To connect to Win11 PC: in /boot/firmware/config.txt file, add 'dtoverlay=dwc2' to the bottom of the file. Then go to /boot/firmware/cmdline.txt and add 'modules-load=g_serial' at the end of the line. Reboot Pi.  
Greg's Win11 PC would randomly select a COM port for the Pi at each reconnection. The numbers ranged from 'COM5' to 'COM8.' To check port run the code, and it will output a list of COM ports active on your device. Find the one that says 'Universal Serial Device" as that will be the Pi. Put that COM# into the code and re-start the code.  
Hit "Start" to begin data updating. Press "Stop" to have the data stop updating. "Close" to exit the GUI and program.  

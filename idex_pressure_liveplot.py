import matplotlib.pyplot as plt
import matplotlib.animation as animation
from   matplotlib import style 
import numpy as np
import time
import os, sys
import time, sys
import math
import serial
import os.path

plt.style.use('ggplot')
fig = plt.figure()
again = True
z = 0
x = 0
data = []
again = True
plt.ion()


#Attach IDXEX sensor and then type 'dmesg' in terminal for device dev path
ser = serial.Serial('/dev/ttyUSB0', 115200, 8, 'N', 1, 0.1, 0, 0, 0)


#Start button
raw_input('\nPRESS [ENTER] TO START DATA COLLECTION\n')


#Ask user to input name for result plot
name = raw_input("Please enter a name for your result file: ")
print ("\nNow creating %s.txt..." %name)
time.sleep(1)
text_file = open("%s.txt" %name, "w")


print ("\nData collection begins...")
time.sleep(2)


#Operation
while (again==True): 

    #This def has to be places outside of try:
    def animate(i):
    
        data = np.genfromtxt("%s.txt" %name, delimiter=',')
        count = np.count_nonzero(data)
        xarray = np.arange(count)
        true_xarray = np.divide(xarray,10.0)
        plt.clf()
        plt.plot(true_xarray, data, label = 'Default')
        plt.savefig("%s.png" %name)

            
    try:
        ser.write('RB404\r\n')
        r = ser.readline()
        x = int(r[2:9],16)
        print 'int value: ',x
        z = ((x*1000)/(4194304))*0.0145038
        print z
        data.append(z)
        with open("%s.txt" %name,"w")as output:	  output.write(str(data))


        
        #Makes an animation by repeatedly calling a function func->def animate
        #Interval = Frequency of udpate = How often does the graph update: 10 = update per 10ms
        #blit = True: Only update data points that have changes
        
        ani = animation.FuncAnimation(fig, animate, frames = 100, interval = 100000, blit=True) 
        plt.title('Pressure Sensor Code Test')
        plt.xlabel('Time (s)')
        plt.ylabel('Pressure (PSI)')
        plt.grid(True)
        plt.legend()
        plt.pause(0.3)
        plt.draw()
        plt.savefig("%s.png" %name)
        again = True        
   
    #Stop Button = KeyboardInterrupt = Ctrl + C
    except (KeyboardInterrupt):
        
        print('\nInterruptted')
        time.sleep(2)
        print'\nProgram will exit in 10 seconds...'
        time.sleep(5)
        print'\nProgram will exit in 5 seconds...'
        time.sleep(5)
        break

    else:
        print('no exception')
        

#To pump: 
#1) fly to bin
#2) ipython 
#3) import lib_pump_dh as p
#4) p.flow(250,50,2)

#To connect to politoed
#ssh -Y genia@politoed 

#To copy from politoed 
#Ask them 

# get X,Y,Vel data from HLK-LD2450 person-sensing radar
# JBeale 4/13/2024

import serial_protocol
import serial
import time, datetime
import os
# ------------------------------------------------

#port = "/dev/ttyUSB0"
port = "COM5"
logDir =  r"C:\Users\beale\Documents\Tiltmeter"

# ----------------------------------------------------------
def printL(buf):
    print(buf,end="")            
    logF.write(buf)

def printEOL():
    print("")
    logF.write(EOL)

# indicate start or stop time, depending on parameter p: 1=start, 0=stop
def doStartStop(p):
    epoch = time.time()
    dtime = datetime.datetime.fromtimestamp(epoch)
    dstr = dtime.strftime("%Y-%m-%d %H:%M:%S")
    buf=("# %.3f,%d,%s" % (epoch,p,dstr))
    printL(buf+EOL)

EOL = "\n"
now = datetime.datetime.now()
date_time_str = now.strftime("%Y%m%d_%H%M%S")
logFname = date_time_str + "_posLog.csv"
logPath = os.path.join(logDir, logFname)
logF =  open(logPath, "w")

# header
printL("x1,y1,v1,x2,y2,v2,x3,y3,v3")
printEOL()

# Open the serial port
ser = serial.Serial(port, 256000, timeout=1)

old1x = 0
old1y = 0
run=False
try:
    while True:
        # Read a line from the serial port
        serial_port_line = ser.read_until(serial_protocol.REPORT_TAIL)

        all_target_values = serial_protocol.read_radar_data(serial_port_line)
        
        if all_target_values is None:
            run=False
            continue

        target1_x, target1_y, target1_speed, target1_distance_res, \
        target2_x, target2_y, target2_speed, target2_distance_res, \
        target3_x, target3_y, target3_speed, target3_distance_res \
            = all_target_values

        if (target1_x == old1x) and (target1_y == old1y):
            if run:
                doStartStop(0)
                run=False
            continue
        old1x = target1_x
        old1y = target1_y
        if (abs(target1_y) > 2800):
            if run:
                doStartStop(0)
                run=False
            continue

        if (not run):
            if (target1_y == 0) and (target1_x == 0):
                continue
            doStartStop(1)
            run=True
        buf=("%05d, %05d, %05d" % (target1_x, target1_y, target1_speed))
        printL(buf)

        if (target2_x ==0) and (target2_y ==0):                        
            printEOL()
            continue

        buf=(", %05d, %05d, %05d" % (target2_x, target2_y, target2_speed))
        printL(buf)

        if (target3_x ==0) and (target3_y ==0):     
            printEOL()                   
            continue

        buf=(", %05d, %05d, %05d" % (target3_x, target3_y, target3_speed))
        printL(buf)
        printEOL()

except KeyboardInterrupt:
    # Close the serial port on keyboard interrupt
    ser.close()
    print("Serial port closed.")
    logF.close()

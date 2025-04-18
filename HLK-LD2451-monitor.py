# monitor serial packets from HLK-LD2451 speed sensor
# based on HLK LD2451 serial protocol manual pdf
# Version:  V1.03  Modification  date:  2024-7-1
# JPB 4/16/2025

import serial
import time
import datetime
import os

# port = "/dev/ttyUSB0"  # port with HLK-LK2451 sensor
port = "COM11"
logdir = r"C:\Users\beale\Documents\radar"

def sendCmd(ser, enacfg):
    ser.write(enacfg)  # command to enter config mode
    time.sleep(0.1)
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        print(data.hex())


timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"LD2451_log_{timestamp}.csv"
logfile = os.path.join(logdir, filename)

ser = serial.Serial(port, 115200, timeout=1) # connect to the serial device
print("Serial port %s opened." % port)

header = b'\xf4\xf3\xf2\xf1'  # normal status packet start/end
trailer = b'\xf8\xf7\xf6\xf5'

cheader = b'\xfd\xfc\xfb\xfa' # control packet start/end
ctrailer = b'\x04\x03\x02\x01'

cstart = b'\x04\x00\xff\x00\x01\x00'  # enter config mode
cend = b'\x02\x00\xfe\x00'            # leave config mode
cset1 = b'\x05\x00\x02\x00\x64\x01\x05\x02' # max 0x64 m, toward only, min 0x05 km/h 2s delay
cset2 = b'\x05\x00\x02\x00\x64\x02\x02\x01' # max 0x64 m, either dir, min 0x02 km/h 1s delay

noTarget = b'\x00\x00'
enacfg = cheader + cstart + ctrailer
discfg = cheader + cend + ctrailer
doset2 = cheader + cset2 + ctrailer

if ser.in_waiting > 0:
    data = ser.read(ser.in_waiting)

print("Sending config mode cmd")
sendCmd(ser, enacfg) # enter config mode
sendCmd(ser, doset2)      # set configuration
sendCmd(ser, discfg)      # exit config mode
print("Entering monitor mode")

try:
    with open(logfile, "w") as fout:
        fout.write("epoch,len,x,num,alm,deg,m,dir,kmh,SNR\n")

        quiet = True  # no signal detected
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                bytes = len(data)
                if (data[0:4] == header) and (data.endswith(trailer)) and (bytes > 8):
                    payload = data[4:-4]
                    if (payload == noTarget):
                        print('.',end="")
                        quiet=True
                    else:
                        if quiet:
                            print()
                            quiet = False
                        tnow = time.time()      
                        payload = data[4:-4]
                        # hex_string = ' '.join([f'{byte:02x}' for byte in payload])                  
                        values = ', '.join([f'{byte:03d}' for byte in payload])                  
                        buf = ("%.3f, %s\n" % (tnow, values))
                        print(buf,end="")
                        fout.write(buf)
                          
except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")

"""
epoch time      pktlen #  Alm deg  m  dir km/h SNR
1744862509.425, 07 00  01  01  88  04  01  03  d6
"""

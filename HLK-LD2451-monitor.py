# monitor serial packets from HLK-LD2451 speed sensor
# JPB 4/16/2025

import serial
import time

port = "/dev/ttyUSB0"  # port with HLK-LK2451 sensor
ser = serial.Serial(port, 115200, timeout=1) # connect to the serial device
print("Serial port %s opened." % port)

# idle packet: f4 f3 f2 f1  00 00  f8 f7 f6 f5

header = b'\xf4\xf3\xf2\xf1'
trailer = b'\xf8\xf7\xf6\xf5'

cheader = b'\xfd\xfc\xfb\xfa'
ctrailer = b'\x04\x03\x02\x01'
cstart = b'\xff\x00\x01\x00'

noTarget = b'\x00\x00'
enacfg = cheader + cstart + ctrailer
"""
for i in range(2):
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        print(data.hex())
    time.sleep(0.6)

print()
ser.write(enacfg)  # command to enter config mode
time.sleep(0.1)
if ser.in_waiting > 0:
    data = ser.read(ser.in_waiting)
    print(data.hex())
"""
if ser.in_waiting > 0:
    data = ser.read(ser.in_waiting)

print("Entering monitor mode")

quiet = True  # no signal detected
try:
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
                    hex_string = ' '.join([f'{byte:02x}' for byte in payload])                  
                    print("%.3f, %s" % (tnow, hex_string))
                          
 

except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")

"""
epoch time      pktlen #  Alm deg  m  dir kmh SNR
1744862509.425, 07 00  01  01  88  04  01  03  d6
...................
1744862522.835, 07 00 01 01 6f 04 01 10 ff
1744862522.950, 07 00 01 01 80 04 01 0e c0
1744862522.970, 07 00 01 01 6f 04 01 0e c0
1744862524.295, 07 00 01 01 82 02 01 03 ab

"""

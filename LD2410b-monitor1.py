# read serial data from LD2410b 24GHz FMCW radar presence sensor
# 4/6/2025 J.Beale

import serial
import time
from datetime import datetime
import os

def showDat(data, logF):
    # print("Pkt:(%d) %s" % (len(data), data.hex()))
    s = "f4f3f2f1" # four-byte header
    pktHeader = bytes.fromhex(s)
    s = "f8f7f6f5" # four-byte trailer
    pktTrailer = bytes.fromhex(s)
    if len(data) != 45:
        return
    if (data[0:4] == pktHeader) and (data[-4:] ==  pktTrailer):
        dat = data[8:-4] # actual sensor data  len(dat)==33
        # print("G:", end="")
        buf=""
        for b in dat:  # print each byte as integer            
            buf = buf + ("%d," % b)
        buf = buf[:-1]            
        print(buf)            
        logF.write(buf+"\n")

def read_packets_from_serial(port, baudrate, logF):
    try:
        ser = serial.Serial(port, baudrate, timeout=0.09)        
        print(f"Connected to {ser.name}")        
        
        str = "FDFCFBFA0400FF00010004030201"
        pktEnCfg = bytes.fromhex(str) # enter config mode
        str= "FDFCFBFA0200620004030201"
        pktEnEng = bytes.fromhex(str) # enable Engineering Mode
        str = "FDFCFBFA0200FE0004030201"
        pktEndCfg = bytes.fromhex(str) # exit config mode

        data = ser.read(52)  # get any existing data
        print(f"Initial datat: {data.hex()}")

        ser.write(pktEndCfg)
        data = ser.read(46)  # get reply
        print(f"EndCfg Reply packet: {data.hex()}")
        data = ser.read(46)  # get another reply
        print(f"Add'll Reply packet: {data.hex()}")

        ser.write(pktEnCfg)
        data = ser.read(46)  # get reply
        print(f"EnCfg Reply packet: {data.hex()}")
        pktEnEng = bytes.fromhex(str)
        ser.write(pktEnEng)
        data = ser.read(46)  # expect 14 byte reply
        print(f"EngMode Reply packet: {data.hex()}")
        #time.sleep(0.1)

        while True:
            data = ser.read(45)  # get reply
            showDat(data, logF)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    serial_port = "COM10"     # sensor serial port
    serial_baudrate = 256000  # default sensor baud rate

    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d_%H%M%S")

    logDir =  r"C:\Users\beale\Documents\Tiltmeter"
    logFname = date_time_str + "_distLog.csv"
    logPath = os.path.join(logDir, logFname)
    columnHeader = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,1,2,3,4,5,6,7"

    with open(logPath, "w") as logF:                
        logF.write(columnHeader+"\n")
        read_packets_from_serial(serial_port, serial_baudrate, logF)

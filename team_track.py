#!/usr/bin/env python
# -*- coding: utf8 -*-


import RPi.GPIO as GPIO
import MRFC522TeamTrack
import signal
import time
import mysql

read_time_gap    = 20 # Number of seconds to elapse before a particular NFC chip can be registered again
success_leds     = [7, 11] # [GPIO 4, GPIO 17]
failure_leds     = [13, 15] # [GPIO 27, GPIO 22]
buzzers          = [18, 18] # [GPIO 18 (12), GPIO 24] # Hack, rely on one buzzer.
chip_uids        = {}

continue_reading = True

# Indicate that the script has started running successfully
def StartUpSuccess():
    for x in range(0, 2):
        time.sleep(0.5)
        GPIO.output(buzzers[0], True)
        GPIO.output(buzzers[1], True)
        GPIO.output(success_leds[0], True)
        GPIO.output(success_leds[1], True)
        
        time.sleep(0.8)
        GPIO.output(buzzers[0], False)
        GPIO.output(buzzers[1], False)
        GPIO.output(success_leds[0], False)
        GPIO.output(success_leds[1], False)

# Capture SIGINT & SIGTERM for cleanup when the script is aborted
def EndRead(signal,frame):
    global continue_reading
    print "Interrupt caught, ending program."
    continue_reading = False

# Do any necessary extra GPIO setup
def PostGPIOInit():
    GPIO.setup(success_leds[0], GPIO.OUT)
    GPIO.setup(success_leds[1], GPIO.OUT)
    GPIO.setup(failure_leds[0], GPIO.OUT)
    GPIO.setup(failure_leds[1], GPIO.OUT)
    GPIO.setup(buzzers[0], GPIO.OUT)
    GPIO.setup(buzzers[1], GPIO.OUT)

def TakeReading(MIFAREReader):
    device = None
    uid    = None

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        #print "Card detected"
    
        # Get the UID of the card
        (status,device, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            #print str(device)+" - Card read UID: "+str(uid)
        
            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status != MIFAREReader.MI_OK:
                device = None
                uid    = None

    return (device, uid)

def ConvertUIDListToString(uid):
    uid_string = ""
    
    if len(uid) > 3:
        uid_string = str(uid[0])+'-'+str(uid[1])+'-'+str(uid[2])+'-'+str(uid[3])

    return uid_string

def RecordChipReading(device, uid_string):
    fullname = mysql.InsertReading(device, uid_string)
    if fullname is not None:
        WriteSuccess(device)
        chip_uids[uid_string] = time.time()
        print "Name: "+fullname+" ("+str(device)+"); Card: "+uid_string
    else:
        WriteFailure(device)
        print "Failed to get Name back from DB ("+str(device)+"); Card: "+uid_string

def WriteSuccess(device):
    # print "Green LED - device: "+str(device)
    GPIO.output(buzzers[device], True)
    GPIO.output(success_leds[device], True)
    time.sleep(0.8)
    GPIO.output(buzzers[device], False)
    GPIO.output(success_leds[device], False)

def WriteFailure(device):
    # print "Red LED - device: "+str(device)
    GPIO.output(failure_leds[device], True)
    time.sleep(0.1)
    GPIO.output(failure_leds[device], False)

# React if the user interrupts the script with Ctrl-C
signal.signal(signal.SIGINT, EndRead)
# React if our service is stopped
signal.signal(signal.SIGTERM, EndRead)

# Create an object of the class MFRC522 - this initialises GPIO
MIFAREReader = MRFC522TeamTrack.MRFC522TeamTrack(dev_list=['/dev/spidev0.0', '/dev/spidev0.1'])

# Do any necessary extra GPIO setup
PostGPIOInit()

# Welcome message
print "Team Track started."
print "Press Ctrl-C to stop."

# Indicate the script is ready
StartUpSuccess()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # See if any chips are ready to be read
    (device, uid) = TakeReading(MIFAREReader)


    valid_uid     = False
    time_gap_good = False
    # A lot of 'ifs' to try and make sure that uid wasn't corrupted in transmission
    #    and that enough time had elapsed since it was last scanned
    if (uid is not None) and (type(uid) is list):
        uid_string = ConvertUIDListToString(uid)
        if mysql.GetNameForTag(uid_string) is not None:
            valid_uid = True

            # Now check whether this chip has already been checked recently
            if chip_uids.has_key(uid_string): # This tag has been checked before
                if time.time() - chip_uids[uid_string] >= read_time_gap:
                    time_gap_good = True
            else: # This is the first time this tag has been checked
                time_gap_good = True

        if valid_uid:
            if time_gap_good:
                #print "("+str(device)+"); Card: "+uid_string # HACK - remove and uncomment
                RecordChipReading(device, uid_string)
        else:
            print "Invalid UID: ("+str(device)+"); Card: "+uid_string

    # Switch to the next RFID reader
    MIFAREReader.MRFC522_AdvanceDevice() # HACK - uncomment

# Finally clean everything up
GPIO.cleanup()

#!/usr/bin/env python

from MFRC522 import MFRC522
import spi

class MRFC522TeamTrack(MFRC522):

    curr_device_id = 0
    curr_speed     = 0
    device_list    = []

    def __init__(self, dev_list=[], dev_id=0, spd=1000000):
        # Sanitise our parameters
        # Ensure we have at least one device in device_list
        if not dev_list:
            self.device_list = ['/dev/spidev0.0']
        else:
        	self.device_list = dev_list

        # Ensure that dev_id is a valid index into device_list
        if (dev_id < 0) or (dev_id >= len(dev_list)):
            dev_id = 0

        curr_device = dev_list[dev_id]

        self.curr_device_id = dev_id
        self.curr_speed     = spd

        # Call MRFC522's initialiser
        super(MRFC522TeamTrack, self).__init__(curr_device, spd)

    def MRFC522_GetDeviceID(self):
        return self.curr_device_id

    def MRFC522_AdvanceDevice(self):
        # Advance to the next device in device_list
        #    (wrapping back to the first device after we reach the end)
        self.curr_device_id = self.curr_device_id + 1;
        if ( self.curr_device_id >= len(self.device_list) ):
            self.curr_device_id = 0;
            
        # Close the current SPI device, and open the next
        spi.closeSPI()
        spi.openSPI(device=self.device_list[self.curr_device_id], speed=self.curr_speed)

        # Finally call MFRC522's MFRC522_Init() method
        super(MRFC522TeamTrack, self).MFRC522_Init()

    def MFRC522_Anticoll(self):
        (status, backData) = super(MRFC522TeamTrack, self).MFRC522_Anticoll()

        # Add the curr_device_id into the return value
        return (status,self.curr_device_id, backData)

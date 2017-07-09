import usb.core
import usb.util
import sys
 
# find our device
dev = usb.core.find(idVendor=0x046d, idProduct=0xc21c)
 
# was it found?
if dev is None:
    raise ValueError('Device not found')
 
# Linux kernel sets up a device driver for USB device, which you have
# to detach. Otherwise trying to interact with the device gives a
# 'Resource Busy' error.
try:
    dev.detach_kernel_driver(0)
except Exception, e:
    pass # already unregistered


# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()
 
# Let's fuzz around! 
 
# Lets start by Reading 1 byte from the Device using different Requests
# bRequest is a byte so there are 255 different values
#for bRequest in range(255):
#    try:
#        ret = dev.ctrl_transfer(0x80, bRequest, 0, 0, 1)
#        print "bRequest ",bRequest
#        print ret
#    except:
#        # failed to get data for this request
#        pass

interface = 0
endpoint = dev[0][(0,0)][0]
usb.util.claim_interface(dev, interface)

collected = 0
attempts = 100
# byte 0 always =1
# bytes 1,2 Joystick control
# bytes 3,4,5 are GKeys 
# byte 5 msb, 128 = LCD Light on, 0 = LCD Light off
# byte 6 LCD Control Keys & M1-3
# byte 7 Joystick Keys & MR Key
#array('B', [1, 134, 130, 1, 0, 128, 0, 128])
while collected < attempts :
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        collected += 1
        print data
        #if data[3] != 0 or data[4] != 0:
        #    print "GKey 1-16 Pressed"
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue

# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)



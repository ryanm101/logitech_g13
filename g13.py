import usb.core
import usb.util
import sys

class g13(object):
    def __init__(self):
        self.dev = None
        self.interface = 0
        self.getDevice(0x046d,0xc21c)
        self.detachKernelDriver(self.dev)
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.dev.set_configuration()
        self.claimInterface(self.dev, self.interface)
        self.endpoint = self.dev[0][(0,0)][0]
        self.listenfordata(self.dev,self.endpoint)

    def getDevice(self, vendorid, prodid):
        # find our device
        self.dev = usb.core.find(idVendor=vendorid, idProduct=prodid)
        if self.dev is None:
            raise ValueError('Device not found')

    def detachKernelDriver(self, dev):
        # Linux kernel sets up a device driver for USB device, which you have
        # to detach. Otherwise trying to interact with the device gives a
        # 'Resource Busy' error.
        try:
            dev.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered

    def claimInterface(self, dev, interface):
        usb.util.claim_interface(dev, interface)

    def listenfordata(self,dev,endpoint):
        while(1):
            try:
                data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
                print data
            except usb.core.USBError as e:
                data = None
                if e.args == ('Operation timed out',):
                    continue

    def cleanup(self,dev, interface):
        # release the device
        usb.util.release_interface(dev, interface)
        # reattach the device to the OS kernel
        dev.attach_kernel_driver(interface)

# byte 0 always =1
# bytes 1,2 Joystick control
# bytes 3,4,5 are GKeys
# byte 5 msb, 128 = LCD Light on, 0 = LCD Light off
# byte 6 LCD Control Keys & M1-3
# byte 7 Joystick Keys & MR Key
#array('B', [1, 134, 130, 1, 0, 128, 0, 128])
if __name__ == "__main__":
    g = g13()

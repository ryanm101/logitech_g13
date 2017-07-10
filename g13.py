import usb.core
import usb.util
import sys

class g13(object):
    def __init__(self):
        self.dev = None
        self.interface = 0
        self.vendorid = 0x046d
        self.prodid = 0xc21c
        self.endpoint = None
        self.maskdic = {
            "1": 1,
            "2": 2,
            "4": 3,
            "8": 4,
            "16": 5,
            "32": 6,
            "64": 7,
            "128": 8
        }

    def setup(self):
        self.getDevice(self.vendorid,self.prodid)
        self.detachKernelDriver(self.dev)
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.dev.set_configuration()
        self.claimInterface(self.dev, self.interface)
        self.endpoint = self.dev[0][(0,0)][0]

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

    def getLCDKeys(self,byte):
        matches = list()
        binary = long(hex(byte),16)
        for k in self.maskdic.keys():
            mask = long(hex(int(k)),16)
            if binary & mask != 0:
                if int(k) > 31:
                    continue
                _str = "LCDK{}".format(self.maskdic[k])
                matches.append(_str)
        return matches

    def getGKeys(self, bytelst):
        matches = list()
        for idx,byte in enumerate(bytelst):
            _mod = idx * 8
            binary = long(hex(byte),16)
            for k in self.maskdic.keys():
                mask = long(hex(int(k)),16)
                if binary & mask != 0:
                    if idx == 2 and int(k) > 63:
                        continue
                    _str = "G{}".format(self.maskdic[k] + _mod)
                    matches.append(_str)
        return matches

    def isLCDLightOn(self,byte):
        if long(hex(byte),16) & 0x80:
            return True
        return False

    def listenfordata(self,dev,endpoint):
        while(1):
            try:
                data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
                #print data
                print "[{0},{2},{4},{6},{8},{10},{12},{14}]::::[{1},{3},{5},{7},{9},{11},{13}]".format(
                        hex(data[0]),data[0],
                        hex(data[1]),data[1],
                        hex(data[2]),data[2],
                        hex(data[3]),data[3],
                        hex(data[4]),data[4],
                        hex(data[5]),data[5],
                        hex(data[6]),data[6],
                        hex(data[7]),data[7]
                    )

            except usb.core.USBError as e:
                data = None
                if e.args == ('Operation timed out',):
                    continue

    def cleanup(self):
        # release the device
        try:
            usb.util.release_interface(self.dev, self.interface)
        except:
            pass
        # reattach the device to the OS kernel
        try:
            self.dev.attach_kernel_driver(self.interface)
        except:
            pass

# byte 0 always =1
# bytes 1,2 Joystick control (x,y) coordinates
# bytes 3,4,5 are GKeys
# byte 5 msb, 128 = LCD Light on, 0 = LCD Light off
# byte 6 LCD Control Keys & M1-3
# byte 7 Joystick Keys & MR Key
#array('B', [1, 134, 130, 1, 0, 128, 0, 128])
if __name__ == "__main__":
    g = g13()
    g.setup()
    g.listenfordata(g.dev,g.endpoint)

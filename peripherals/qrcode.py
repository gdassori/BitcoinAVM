# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM


# many thanks to the awesome zbarcam, which makes us able to recognize QRCode
# with a 3$ chinese usb cam :-)

import zbar

class QRCode():
    def __init__(self, device):
        self.device = device
        self.address = ''
        self.processor = zbar.Processor()
        self.processor.parse_config('enable')
        self.processor.init(self.device)

    def read_address(self):
        output = dict()
        output['address'] = ''
        def my_handler(proc, image, closure):
            for symbol in image:
                output['address'] = symbol.data

        self.processor.set_data_handler(my_handler)
        self.processor.visible = True
        self.processor.active = True
        self.processor.process_one(5)
        self.processor.visible = False
        self.processor.active = False
        address = output['address']
        pos = address.find('1')
        self.address = address[pos:]
        return self.address


    def kill_reader(self):
        self.processor.active = False
        self.processor.visible = False
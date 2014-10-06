# Bitcoin AVM, an open source Django base Bitcoin ATM
# https://github.com/mn3monic/BitcoinAVM
#
#  ccTalk basic implementation
# Credits:
# Balda - https://github.com/Baldanos/ccTools
# David Schryer - https://bitbucket.org/schryer/cctalk
#



import serial, time
from struct import unpack, pack

def set_tty(tty):
    ser = serial.Serial(port="/dev/%s" % tty,
                           baudrate=9600,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE,
                           bytesize=serial.EIGHTBITS,
                           xonxoff=True,
                           )
    return ser

def make_msg(code, data=None, slave_addr=40, host_addr=1):
    if not data:
        seq = [slave_addr, 0, host_addr, code]
    else:
        seq = [slave_addr, len(data), host_addr, code] + data
    packet_sum = 0
    for i in seq:
        packet_sum += i
    end_byte = 256 - (packet_sum%256)
    packet = seq + [end_byte]
    return packet

def send_msg(tty, handler, delay=0.2, timeout=1):
    packet = handler.packet
    int_msg = handler.integer_message
    now = time.time()
    tty.write(packet)
    print int_msg
    time.sleep(delay)
    while 1:
        t = time.time() - now
        if t > timeout :
            break
    raw = tty.read(tty.inWaiting())
    if len(raw) > 1:
        len_raw = len(raw)
        out_byte = unpack('={0}c'.format(int(len_raw)), raw)
        offs = 4 + handler.bytes_sent
        packet = out_byte[offs:]
        reply_msg = reply_handler(packet, handler)
        if reply_msg:
            return reply_msg
        else:
            print 'no reply msg'
            return False
    print 'empty reply'
    return False

def reply_handler(packet, handler):
    reply_length = handler.bytes_returned
    reply_type = handler.type_returned
    reply_int = map(ord, packet)
    if len(reply_int) < 2:
        return False
    msg_length = reply_int[1]
    if msg_length != reply_length:
        pass    # safety feature?
    if handler.request_code == 254:
        expected_reply = [1, 0, 40, 0, 253]
        if reply_int != expected_reply:
            raise UserWarning('unexpected reply', (reply_int, expected_reply))
    reply_msg_int = reply_int[:-1]
    reply_msg_byte = packet[:-1]
    if reply_type is str:
        print ''.join(reply_msg_byte)
        return ''.join(reply_msg_byte)
    elif type(reply_type) in (int, bool):
        print reply_msg_int
        return reply_msg_int
    else:
        print reply_msg_int
        return reply_msg_int

class Handler(object):
    """
    Pseudo-dictionary - Packet handler
    """
    def __init__(self, item=None):
        if item:
            self.add(item)

    def add(self, item):
        if isinstance(item, dict):
            self.__dict__.update(item)

        elif isinstance(item, Handler):
            self.__dict__.update(item.__dict__)

        else:
            raise UserWarning('unsupported item', (item, type(item)))

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def get(self, key, alternate=None):
        return self.__dict__.get(key, alternate)

    def has_key(self, key):
       return self.__dict__.has_key(key)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

class NV10(object):
    r_info = dict(reset_device=(1, 0, bool),
                  product_type=(244, 0, str),
                  enable=(10, 0, str),
                  read_events_buffer=(159, 0, int),
                  hardware_type=(245, 0, str),
                  request_inhibit_status=(230, 0, int),
                  self_check=(232, 0, bool),
                  test_lamps=(151,[0,], 0, str),
                  operate_bidirectional_motors=(149, 0, str),
                  up_to_5=(231, [1, 0], 0, str),
                  up_to_10=(231, [3, 0], 0, str),
                  up_to_20=(231, [7, 0], 0, str),
                  up_to_50=(231, [15, 0], 0, str),
                  uhinhibit_all=(231, [255, 0], 0, str),
                  inhibit_all=(231, [0, 0], 0, str),
                  modify_master_inhibit_status=(228, [1], 0, str),
                  request_base_year=(170, 0, str),
                  simple_poll=(254, 0, bool),
                  request_bill_id=(157, 0, str),
                  route_bill=(154, [1], 0, bool))

    def __init__(self, tty):
        self.tty = tty
        self.events = 0
        self.request_data = {}
        for k, v in self.r_info.items():
            if len(v) == 3:
                int_msg = make_msg(v[0])
            else:
                int_msg = make_msg(v[0],v[1])
            byte_msg = map(chr, int_msg)
            if type(v[1]) is type(list()):
                packet = pack('='+'c'*(1+len(v)+len(v[1])), *byte_msg)
            else:
                packet = pack('='+'c'*(2+len(v)), *byte_msg)
            self.request_data[k] = Handler(dict(packet=packet,
                                                integer_message=int_msg,
                                                byte_message=byte_msg,
                                                request_code=v[0],
                                                bytes_returned=v[1],
                                                bytes_sent=0,
                                                type_returned=v[2],
                                                user_message=k))

    def request(self, request_key):
        r_dic = self.request_data.get(request_key, None)
        if not r_dic:
            raise NotImplementedError('not implemented', (request_key))
        print 'requesting: %s' % r_dic.user_message
        reply_msg = send_msg(self.tty, r_dic)
        return reply_msg

    def reset(self):
        self.request('reset_device')

    def accept_notes(self, max_amount):
        """
        Usage: self.accept_notes(max_amount)
        """
        if max_amount == 50:
            self.request('up_to_50')
            self.expected_mask = [15, 0]
        elif max_amount == 20:
            self.request('up_to_20')
            self.expected_mask = [7, 0]
        elif max_amount == 10:
            self.request('up_to_10')
            self.expected_mask = [3, 0]
        elif max_amount == 5:
            self.request('up_to_5')
            self.expected_mask = [1, 0]
        else:
            return "unrecognized amount, accepted values: 5, 10, 20, 50"
        status = self.request('request_inhibit_status')
        if status == self.expected_mask:
            self.request('modify_master_inhibit_status')
            return 'max amount set: ' + str(max_amount)
        else:
            return 'somenthing went wrong, cannot check if inhibit status is matching'
        pass

    def events_manager(self, event):
        """
        Events:
        1 : some kind if error
        2 : note in
        3 : note routed
        """
        res = {'error': '', 'message': ''}
        if event[0] == 0:
            res['error'] = 1
            res['message'] = 'error n %s' % event[1]
        if event[0] in (1, 2, 3, 4):
            notes = {1: 5, 2: 10, 3: 20, 4: 50}
            res['error'] = 0
            res['message'] = 'banknotes event, banknote: %s' % notes[event[0]]
            if event[1] == 1:





    def check_queue(self):
        queue = self.request('read_events_buffer')
        buffer = {}
        if queue[0] != self.events:
            print 'new event(s)'
            new_events = (int(queue[0]) - int(self.events))
            self.events = queue[0]
            if new_events > 5:
                new_events = 5
            for event in new_events:








def test_job():
    """
    0.1 - 0.2 - 0.3 = Errori - 0.1 Foglio bianco rifiutato, 0.2 e 0.3 avvengono con banconota straniera
    0.4 - Errore se inserita banconota non disinibita.
    1.1 = Banconota inserita canale.bool (2.1 = 10eur, 3.1 = 20eur, 4.1 = 50eur)
    1.2 = Banconosta smistata correttamente (2.0, 3.0, 4.0)
    0.0 = In attesa? Arriva dopo expire - Verificare se avviene anche con inhibits
    formato: [Tot_Eventi, a, a, b, b, c, c, d, d, e, e,] = Buffer 5 eventi
    """
    while 1:
        try:
            ser = set_tty('ttyUSB0')
            cm = NV10(ser)
            cm.request('reset_device')
            time.sleep(2)
            cm.request('modify_master_inhibit_status')
            cm.request('up_to_50')
            while 1:
                events = cm.request('read_events_buffer')
                #print events
                if events[1] and events[2]:
                    if type(events) is type(list()):
                        print "event happened"
                        time.sleep(1)
                        print "routing bill"
                        cm.request('route_bill')
                        time.sleep(1)
                        print "read event 10 seconds later - probably notes accept disabled"
                        cm.request('read_events_buffer')
                        time.sleep(1)
                        cm.request('modify_master_inhibit_status')
                        cm.request('up_to_50')
                        cm.request('read_events_buffer')
                        print "read event 10 seconds later - notes accept just enabled"
                    else:
                        print 'error catching events: expected list, got %s' % type(events)
                        print events
                time.sleep(0.1)
        except KeyboardInterrupt:
            print 'Quitting...'
            break
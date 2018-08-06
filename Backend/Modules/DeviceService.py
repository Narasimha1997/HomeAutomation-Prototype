from threading import Thread
import datetime


class Devices():

    def __init__(self):
        self.dev = {
            'fan_1' : 'fan_1.txt',
            'light_1' : 'light_1.txt',
            'light_2' : 'light_2.txt',
            'valve' : 'valve.txt',
            'temp_sensor' : 'temp_sensor.txt'
        }

    def getKnownDevices(self):
        return self.dev
    
    def getDeviceFileName(self, dev_type):
        print(dev_type)
        return self.dev[dev_type]

class SaveDeviceData(Thread):

    def __init__(self, websocket,  data):
        Thread.__init__(self)
        self.dev_id = data['id']
        self.dev_type = data['dev_type']
        self.device_data = data['device_data']
        #self.websocket = websocket
    
    def run(self):
        #idientify device type:
        f_name = Devices().getDeviceFileName(dev_type = self.dev_type)
        with open('DATA/'+f_name, 'a') as append:
            print('Wrote data')
            timestamp = str(datetime.datetime.utcnow())
            append.write(str(self.device_data)+'???'+timestamp+'\n')
        append.close()
        #self.websocket.emit('storage_ack'+str(self.dev_id), {'success' : True})

def get_last_temperature():
    f_name = Devices().getDeviceFileName('temp_sensor')
    t = open('DATA/'+f_name, 'r').readlines()[-1]
    temp = t.split('???')[0]
    return temp

def get_last_valve():
    f_name = Devices().getDeviceFileName('valve')
    t = open('DATA/'+f_name, 'r').readlines()[-1]
    vavle = t.split('???')[0]
    return vavle

class SendToDevice(Thread):

    def __init__(self, websocket, data, id_):
        Thread.__init__(self)
        self.websocket = websocket
        self.data = data
        self.id_ = id_
    
    def run(self):
        print(self.data)
        self.websocket.emit('req_resp', {'success' : True})
        self.websocket.emit('backend_to_device', self.data)
        print('Sent success')
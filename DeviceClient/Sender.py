import requests
from threading import Thread


class SendPostData():
    
    def __init__(self, dev_type, rand_id, host, port):
        self.dev_type = dev_type
        self.rand_id = rand_id
        self.host = host
        self.port = port
    
    def send(self, data):
        data = {
            'dev_type' : self.dev_type,
            'id' : self.rand_id,
            'device_data' : data
        }

        requests.post('http://'+self.host+':'+str(self.port)+'/dev_event', json=data)
        print('posted')

class EvenLoop(Thread):

    def __init__(self, socketIO, callback):
        Thread.__init__(self)
        self.socketIO = socketIO
        self.callback = callback
    
    def run(self):
        while True:
            self.socketIO.on('backend_to_device', self.callback)
            self.socketIO.wait()
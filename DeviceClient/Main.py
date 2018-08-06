from Sender import SendPostData, EvenLoop
import time
from threading import Thread
from socketIO_client import SocketIO, LoggingNamespace
from DeviceControllers import controller_main, getTemperature, getValveValue

def callback(*args):
    print(args)

class Send(Thread):

    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            sendrt = SendPostData(dev_type = 'valve', rand_id = 10, host = '0.0.0.0', port = 4000)
            sendrt.send(data = getTemperature())

            sendrt2 = SendPostData(dev_type = 'temp_sensor', rand_id = 10, host = '0.0.0.0', port = 4000)
            sendrt2.send(data = getValveValue())
            
            time.sleep(2)


#Send().start()

print('Established a socket connection')

#create a callback function to handle backend-to-device events
def action_callback(*args):
    data = args[0]
    if not data['success']:
        return

    print('Request to access device type : ', data['data']['dev_type'])
    device_type = data['data']['dev_type']
    action = data['data']['action']

    #call made to main controller here:
    controller_main(device_type, action)
    

sock = SocketIO('0.0.0.0', 4000, LoggingNamespace)
sock.emit('ack', {
    'dev' : True
})

#create an event loop, so socket always listens to events from backend
EvenLoop(sock, action_callback).start()

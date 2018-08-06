from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from Modules import crypt
from Modules.DeviceService import SaveDeviceData, get_last_temperature, SendToDevice, get_last_valve



app = Flask(__name__)
CORS(app = app)

key = crypt.Crpyt(text =  'project123').getKey()
socket_client = SocketIO(app = app)

@socket_client.on('auth')
def connection(msg):
    id_ = msg['id']
    password = msg['password']
    print('Socket connected')
    if crypt.password_check(password):
        socket_client.emit('auth_event'+id_, {
            'success' : True,
            'key' : str(key.decode('utf-8'))
       })

    else:
        socket_client.emit('auth_event'+id_, {
            'success' : False,
            'key' : 'no-key'
        })

@socket_client.on('connect')
def connect():
    print('Client connected')

@app.route('/dev_event', methods = ['POST'])
def device_event():
    msg = request.get_json()
    if msg!= None:
        SaveDeviceData(websocket = socket_client, data = msg).start()
        return 'ok'


@socket_client.on('temp_query')
def temp_query(msg):
    print(msg)
    key1 = bytes(msg['key'].encode('utf-8'))
    id_ = msg['id']
    if crypt.key_check(key, key1):
        socket_client.emit('temp_response'+id_, {
            'success' : True,
            'temp' : get_last_temperature()
        })
    else:
        socket_client.emit('temp_response'+id_,{
            'success' : False,
            'temp' : 'no-temp'
        })

@socket_client.on('request_dev_on_off')
def request_dev_on_off(msg):
    key1 = bytes(msg['key'].encode('utf-8'))
    id_ = msg['id']
    if crypt.key_check(key, key1):
        socket_client.emit('backend_to_device', {
            'success' : True,
            'data' : msg['payload']
        })
    else:
        socket_client.emit('backend_to_deivce', {
            'success' : False,
            'data' : 'no-payload'
        })

@socket_client.on('ack')
def ack(msg):
    print('received ack')

@socket_client.on('valve_request')
def valve_request(msg):
    id_ = msg['id']
    key1 = bytes(msg['key'].encode('utf-8'))

    if crypt.key_check(key, key1):
        socket_client.emit('valve_response'+id_, {
            'success' : True,
            'value' : get_last_valve()
        })
    else:
        socket_client.emit('valve_response'+id_, {
            'success' : False,
            'value' : 'no-value'
        })

print( 'Creating server' ) 
socket_client.run( app,  '0.0.0.0')


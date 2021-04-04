import _thread
import utime
import machine
import urequests
from machine import Timer

print('Starting ESP32 script.')
print('Machine Freq: ', machine.freq())


# TODO replace this with real data
headers = {'Content-Type': 'application/json'}
payload_move = ujson.dumps({'time':800, 'move':1})
payload_rms = ujson.dumps({'time':800, 'acc_x_rms':1.23, 'acc_y_rms': 3.313, 'acc_z_rms':6.21111})

def post_request_move():
    res = urequests.post(
        'http://10.0.0.5:8081/api/write-move',
        data=payload_move,
        headers=headers)
    print(response.json())
    response.close()

def post_request_rms():
    res = urequests.post(
        'http://10.0.0.5:8081/api/write-rms',
        data=payload_rms,
        headers=headers)
    print(response.json())
    response.close()
    
while True:
    post_request()
    utime.sleep(5)
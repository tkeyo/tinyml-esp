import utime
import ujson
import machine
import urequests
from machine import Timer

from dummy_data import ACC_X, ACC_Y, ACC_Z

print('Starting ESP32 script.')
unix_base = 946681200 # utime.gmtime(0) - epoch 0 - (2000, 1, 1, 0, 0, 0, 5, 1)


# TODO replace this with real data
headers = {'Content-Type': 'application/json'}

def post_request_move():
    time = unix_base + utime.time()

    payload_move = ujson.dumps({'time':time, 'move':1})
    res = urequests.post(
        'http://10.0.0.5:8081/api/write-move',
        data=payload_move,
        headers=headers)
    print(res.json())
    res.close()

def post_request_rms():
    time = unix_base + utime.time()

    payload_rms = ujson.dumps({'time':time, 'acc_x_rms':1.23, 'acc_y_rms': 3.313, 'acc_z_rms':6.21111})
    res = urequests.post(
        'http://10.0.0.5:8081/api/write-rms',
        data=payload_rms,
        headers=headers)
    print(response.json())
    response.close()
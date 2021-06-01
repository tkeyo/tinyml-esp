import ujson
import urequests
import utime
import uasyncio

from micropython import const
from secret.secret import URL, AUTHORIZATION

unix_base = const(946681200) # utime.gmtime(0) - epoch 0
headers = {
    'Content-Type': 'application/json',
    'Authorization': AUTHORIZATION
    }

def post_request_move(time, move):
    payload = ujson.dumps({'device_id':1,'time':time, 'move':move})

    try:
        res = urequests.post('{}/api/write-move'.format(URL), data=payload, headers=headers)
        print(res.content)
        res.close()
    except OSError:
        print('Server unreachable')

def post_request_rms(time,x,y,z):
    payload = ujson.dumps({'device_id':1, 'time':time, 'acc_x_rms':x, 'acc_y_rms':y, 'acc_z_rms':z})

    try:
        res = urequests.post('{}/api/write-rms'.format(URL), data=payload, headers=headers)
        print(res.content)
        res.close()
    except OSError as e:
        print('Error: {}'.format(e))

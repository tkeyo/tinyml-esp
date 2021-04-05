import ujson
import urequests
import utime
import uasyncio

from micropython import const
from secret.secret import URL

unix_base = const(946681200) # utime.gmtime(0) - epoch 0
headers = {'Content-Type': 'application/json'}

def post_request_move(move: int=1):
    time = unix_base + utime.time()
    payload = ujson.dumps({'time':time, 'move':move})

    try:
        res = urequests.post('{}/api/write-move'.format(URL), data=payload, headers=headers)
        print(res.content)
        res.close()
    except OSError:
        print('Server unreachable')

def post_request_rms(x,y,z):
    time = unix_base + utime.time()
    payload = ujson.dumps({'time':time, 'acc_x_rms':x, 'acc_y_rms':y, 'acc_z_rms':z})

    try:
        res = urequests.post('{}/api/write-rms'.format(URL), data=payload, headers=headers)
        print(res.content)
        res.close()
    except OSError as e:
        print('Error: {}'.format(e))

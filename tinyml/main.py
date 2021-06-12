import gc

gc.collect()
import utime
import machine
import _thread
from machine import Timer, Pin, SoftI2C
from mpu6500 import MPU6500, SF_DEG_S, SF_M_S2

gc.collect()
from data import Data
from http_api import post_request_rms, post_request_move

# from model import random_forest_cd3e41b as rf
from model import random_forest_a8c9ff5 as rf

print('Starting ESP32 script.')

gc.collect()
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)

gc.collect()
data = Data(freq=50, n_signals=5)
data.buffer = [0] * 51 * 5

pred_tuples = []
send_buffer = []

unix_base = const(946681200)
start_time = utime.ticks_ms()

def get_time():
    return (utime.mktime(utime.gmtime()) + unix_base + 3600) * 1000

def read(timer):
    gc.collect()
    acc = mpu6500.acceleration
    gyro = mpu6500.gyro
    data.collect([acc[0], acc[1], acc[2]], [gyro[1], gyro[2]])
    # print("Measurement: {}".format(utime.ticks_ms()))
    # print('Alloc: {} | Free: {}'.format(gc.mem_alloc(), gc.mem_free()))

def score(timer):
    gc.collect()
    # score_start = utime.ticks_ms()
    global start_time
    global predictions
    global send_buffer

    gc.collect()
    res = rf.predict(data.get())
    if res != 0:
        predictions.append(res)
  
    now = utime.ticks_ms()
    diff = utime.ticks_diff(now, start_time)

    gc.collect()
    if len(predictions) > 8 and diff > 450:
        start_time = utime.ticks_ms()
        result = max(set(predictions), key=predictions.count)
        print('{} -> {}'.format(predictions, result))
        send_buffer.append({
            'type': 'move',
            'pred': result,
            'time': get_time()})
        predictions = []
        print(send_buffer)

    if len(predictions) < 6 and diff > 1500:
        print(predictions)
        predictions = []
        print('Pred cleaned')
    # print("Score: ", utime.ticks_diff(utime.ticks_ms(), score_start))

def rms(timer):
    gc.collect()
    global send_buffer
    rms = data.rms
    send_buffer.append({
        'type': 'rms',
        'rms': [rms(0),rms(1),rms(2)],
        'time': get_time()
        })
    print(send_buffer)


def http(timer):
    gc.collect()
    global send_buffer
    for message in send_buffer:
        send_start = utime.ticks_ms()
        if message['type'] == 'move':
            print('Sending Move: ', message)
            post_request_move(message['time'], message['pred'])
        if message['type'] == 'rms':
            print('Sending RMS:', message)
            post_request_rms(message['time'], message['rms'][0], message['rms'][1], message['rms'][2])
        print("Post: {}".format(utime.ticks_diff(utime.ticks_ms(), send_start)))
        send_buffer = []

def read_sensor():
    Timer(0).init(freq=50, mode=Timer.PERIODIC, callback=read)

def run_score():
    Timer(1).init(freq=50, mode=Timer.PERIODIC, callback=score)

def run_rms():
    Timer(2).init(period=10_000, mode=Timer.PERIODIC, callback=rms)
    
def run_http():
    Timer(3).init(period=3_000, mode=Timer.PERIODIC, callback=http)

if __name__ == '__main__':
    read_sensor()
    run_score()
    # run_rms()
    # run_http()
import gc

gc.collect()
import utime
import machine
import _thread
from machine import Timer, Pin, SoftI2C
from mpu6500 import MPU6500, SF_DEG_S, SF_M_S2

gc.collect()
from data import Data
from util import get_time, get_time_diff, get_final_inf_res, reduce_infs, debounce
from http import request_post

from model import random_forest_a8c9ff5 as rf

print('Starting ESP32 script.')

gc.collect()
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)

gc.collect()
data = Data(freq=50, n_signals=5)
data_cap = data.capacity

inf_tuples = []
send_buffer = []

start_time = utime.ticks_ms()

def read(timer):
    gc.collect()
    acc = mpu6500.acceleration
    gyro = mpu6500.gyro
    data.collect([acc[0], acc[1], acc[2]], [gyro[1], gyro[2]])
    # print("Measurement: {}".format(utime.ticks_ms()))
    # print('Alloc: {} | Free: {}'.format(gc.mem_alloc(), gc.mem_free()))

def score(timer):
    gc.collect()
    score_start = utime.ticks_ms()
    global inf_tuples
    global send_buffer

    gc.collect()
    now = utime.ticks_ms()

    input_data = data.data

    if len(input_data) == data_cap:
        res = rf.run(data.data)
        if res in [1,2,3] :
            inf_tuples.append((now, res))
    
    time_diff = get_time_diff(inf_tuples)

    gc.collect()
    result, reduced_infs = debounce(inf_tuples, time_diff)
    
    if result:
        print('{} -> {}'.format(reduced_infs, result))
        send_buffer.append({
            'type': 'move',
            'pred': result,
            'time': get_time()})
        inf_tuples = []
        print(send_buffer)
        # print("Score: ", utime.ticks_diff(utime.ticks_ms(), score_start))
    
    if len(inf_tuples) <= 8 and time_diff >= 1_000:
        inf_tuples = []
        

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
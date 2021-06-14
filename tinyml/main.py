import gc

gc.collect()
import utime
import machine
from ucollections import deque

gc.collect()
from machine import Timer, Pin, SoftI2C
from mpu6500 import MPU6500, SF_DEG_S, SF_M_S2

gc.collect()
from data import Data
from util import (get_time, get_time_diff,
                  get_final_inf_res, reduce_infs, 
                  clean_inf_tuples, debounce)
from http import request_post

from model import random_forest_a8c9ff5 as rf

print('[Main] Starting ESP32 script.')

gc.collect()
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)

gc.collect()
data = Data(freq=50, n_signals=5)
data_cap = data.capacity
print('[Main] Data store initiated. Capacity: {}'.format(data_cap))

inf_tuples = []
send_queue = deque((),10)

start_time = utime.ticks_ms()


def read(timer):
    '''Collects acceleration and gyroscope values from MPU6500 sensor.'''
    gc.collect()
    acc = mpu6500.acceleration
    gyro = mpu6500.gyro
    data.collect([acc[0], acc[1], acc[2]], [gyro[1], gyro[2]])
    # print("Measurement: {}".format(utime.ticks_ms()))
    # print('Alloc: {} | Free: {}'.format(gc.mem_alloc(), gc.mem_free()))


def score(timer):
    '''Runs scoring on collected data.'''
    gc.collect()
    score_start = utime.ticks_ms()
    global inf_tuples
    global send_queue

    gc.collect()
    now = utime.ticks_ms()
    input_data = data.data

    if len(input_data) == data_cap:
        res = rf.run(data.data)
        if res in [1,2,3] :
            inf_tuples.append((now, res))
    
    time_diff = get_time_diff(inf_tuples)
    result, reduced_infs = debounce(inf_tuples, time_diff)
    
    gc.collect()
    if result:
        print('{} -> {}'.format(reduced_infs, result))
        send_queue.append({
            'type': 'move',
            'payload': {
                'device_id':1,
                'move': result,
                'time': get_time()
                }})
        inf_tuples = []
        # print("Score: ", utime.ticks_diff(utime.ticks_ms(), score_start))
    
    if len(inf_tuples) <= 8 and time_diff >= 1_000:
        inf_tuples = []
        

def rms(timer):
    '''Adds RMS data to send queue.'''
    gc.collect()
    global send_queue
    
    rms = data.get_rms
    send_queue.append({
        'type': 'rms',
        'payload':{
            'device_id':1,
            'acc_x_rms':rms(0),
            'acc_y_rms':rms(1),
            'acc_z_rms':rms(2),
            'time': get_time()
        }})


def send_data(timer):
    '''Sends queued data to API endpoint.'''
    gc.collect()
    send_counter = 1
    
    global send_queue
    while send_queue:
        send_start = utime.ticks_ms()
        data_to_send = send_queue.popleft()
        request_post(data_to_send['type'], data_to_send['payload'])
        print('Payload {}: {}'.format(send_counter, data_to_send['payload']))
        print('Data send time: {}'.format(utime.ticks_diff(utime.ticks_ms(), send_start)))
        send_counter += 1


def read_sensor():
    '''Timer to periodically read sensor values.'''
    Timer(0).init(freq=50, mode=Timer.PERIODIC, callback=read)


def run_score():
    '''Timer to periodically run scoring on collected data.'''
    Timer(1).init(freq=50, mode=Timer.PERIODIC, callback=score)


def run_rms():
    '''Timer to periodically run RMS calculation on collected data.'''
    Timer(2).init(period=10_000, mode=Timer.PERIODIC, callback=rms)

    
def run_send_data():
    '''Timer to periodically send data to API endpoint.'''
    Timer(3).init(period=5_000, mode=Timer.PERIODIC, callback=send_data)


if __name__ == '__main__':
    read_sensor()
    run_score()
    run_rms()
    run_send_data()
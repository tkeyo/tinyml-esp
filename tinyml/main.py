import gc

gc.collect()
import utime
import machine
from ucollections import deque

gc.collect()
from machine import Timer, Pin, SoftI2C
from mpu6500 import MPU6500, SF_DEG_S, SF_M_S2

gc.collect()
from config import config
from data import Data
from util import (get_time, get_time_diff,
                    get_final_inf_res, reduce_infs, 
                    clean_inf_tuples, debounce)
from http import request_post

from model import random_forest_a8c9ff5 as rf


print('[Main] Starting ESP32 script')

# initialize IMU connection
gc.collect()
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)


# Initialize data store
gc.collect()
data = Data(freq=50, n_signals=5)
data_cap = data.capacity
print('[Main] Data store initiated. Capacity: {}\n\n'.format(data_cap))


# initialize inference collection tuples
inf_tuples = []

# intialize send queue
send_queue = deque((),10)

# initialize start time
start_time = get_time()


def read(timer):
    '''Collects acceleration and gyroscope values from MPU6500 sensor.'''
    gc.collect()
    acc = mpu6500.acceleration
    gyro = mpu6500.gyro
    data.collect([acc[0], acc[1], acc[2]], [gyro[1], gyro[2]])


def score(timer):
    '''Runs scoring on collected data.'''
    gc.collect()
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
    result = debounce(inf_tuples, time_diff, 
                      config.MIN_INF_TUPLES, config.TIME_DIFF)
    
    gc.collect()
    if result:
        send_queue.append({
            'type': 'move',
            'payload': {
                'device_id':1,
                'move': result,
                'time': get_time()
                }})
        inf_tuples = [] # cleans inference tuple buffer after inference
    
    inf_tuples = clean_inf_tuples(inf_tuples, time_diff,
                                  config.CLEAN_MAX_TUPLES, config.CLEAN_MAX_TIME_DIFF)
        

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
    message_counter = 1
    global send_queue
    
    while send_queue:
        send_start = utime.ticks_ms()
        data_to_send = send_queue.popleft()
        request_post(data_to_send['type'], data_to_send['payload'])
        
        print('Payload {}: {}'.format(
            message_counter, data_to_send['payload']))
        print('Data send time: {}'.format(
            utime.ticks_diff(utime.ticks_ms(), send_start)))
        message_counter += 1


def read_sensor():
    '''Timer to periodically read sensor values.'''
    Timer(0).init(freq=config.READ_SENSOR_FREQ,
                  mode=Timer.PERIODIC, 
                  callback=read)


def run_score():
    '''Timer to periodically run scoring on collected data.'''
    Timer(1).init(freq=config.RUN_SCORE_FREQ, 
                  mode=Timer.PERIODIC, 
                  callback=score)


def run_rms():
    '''Timer to periodically run RMS calculation on collected data.'''
    Timer(2).init(period=config.RUN_RMS_CALC_MS,
                  mode=Timer.PERIODIC,
                  callback=rms)

    
def run_send_data():
    '''Timer to periodically send data to API endpoint.'''
    Timer(3).init(period=config.RUN_SEND_DATA_MS,
                  mode=Timer.PERIODIC,
                  callback=send_data)


if __name__ == '__main__':
    read_sensor()
    run_score()
    run_rms()
    run_send_data()
import gc

gc.collect()
import utime
import machine
import uasyncio
import _thread
from machine import Timer, Pin, SoftI2C
from mpu6500 import MPU6500, SF_G, SF_DEG_S, SF_M_S2

gc.collect()
from data import Data
from http_api import post_request_rms, post_request_move

# from model import random_forest_6475891_esp as rf
# from model import random_forest_1c2c037_esp as rf
from model import random_forest_cd3e41b as rf

print('Starting ESP32 script.')

gc.collect()
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)

gc.collect()
data = Data(freq=20, n_signals=5)
data.buffer = [0] * 21 * 5

predictions = []


def read_mpu6500(timer):
    gc.collect()
    # print('T {}'.format(utime.ticks_ms()))
    acc = mpu6500.acceleration
    gyro = mpu6500.gyro
    data.collect([acc[0], acc[1], acc[2]], [gyro[1]])
    # print('T Collected {}'.format(utime.ticks_ms()))
    # print(data.get_buffer())
    # print('Alloc: {} | Free: {}'.format(gc.mem_alloc(), gc.mem_free()))

def score(timer):
    gc.collect()
    # start = utime.ticks_us()
    res = rf.predict(data.get())
    if res != 0:
        predictions.append(res)
    # print(utime.ticks_us() - start, 'us')
    # print('Alloc: {} | Free: {}'.format(gc.mem_alloc(), gc.mem_free()))

def read_sensor():
    Timer(0).init(freq=20, mode=Timer.PERIODIC, callback=read_mpu6500)

def run_inference():
    Timer(1).init(freq=20, mode=Timer.PERIODIC, callback=score)

_thread.start_new_thread(read_sensor,())
_thread.start_new_thread(run_inference,())
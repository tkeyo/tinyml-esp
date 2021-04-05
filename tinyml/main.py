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
from http_api import post_request_rms

print('Starting ESP32 script.')

gc.collect()
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)

gc.collect()
global data
data = Data(samples=60)
data.init(['acc'])

def read_mpu6500(timer):
    gc.collect()
    print('T {}'.format(utime.ticks_ms()))
    data.collect_acc(mpu6500.acceleration)
    # data.collect_gyro(mpu6500.gyro)
    # print('Alloc: {} | Free: {}'.format(gc.mem_alloc(), gc.mem_free()))

def process_move(interval):
    import urandom
    while True:
        gc.collect()
        utime.sleep(interval)
        print('Movement detected: {}'.format(urandom.getrandbits(2)))

def read_sensor():
    Timer(0).init(period=100, mode=Timer.PERIODIC, callback=read_mpu6500)

def send_rms_data(interval):
    while True:
        gc.collect()
        utime.sleep(interval)
        post_request_rms(data.get_rms_acc_x(), data.get_rms_acc_y(), data.get_rms_acc_z())


_thread.start_new_thread(read_sensor,())
_thread.start_new_thread(send_rms_data,(3,))
_thread.start_new_thread(process_move, (3,))
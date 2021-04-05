import gc

gc.collect()
import utime
import machine
import uasyncio
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
data = Data()
data.init(['acc'])

def read_mpu6500(timer):
    gc.collect()
    start = utime.ticks_us()
    data.collect_acc(mpu6500.acceleration)
    print(utime.ticks_ms())
    # data.collect_gyro(mpu6500.gyro)
    # print('Collect: {}'.format(utime.ticks_us() - start))

def process_rms(timer):
    gc.collect()
    start = utime.ticks_us()
    # print(data.get_rms_acc_x())
    # print(data.get_rms_acc_y())
    # print(data.get_rms_acc_z())
    post_request_rms(data.get_rms_acc_x(), data.get_rms_acc_y(), data.get_rms_acc_z())
    print('RMS Process: {}'.format((utime.ticks_us() - start)/1000))
    # print(gc.mem_alloc())
    # print(gc.mem_free())

def process_move(timer):
    gc.collect()
    import urandom
    print('Movement detected: {}'.format(urandom.getrandbits(2)))

timer_mpu6500 = Timer(0)
timer_rms = Timer(1)
timer_move = Timer(2)

timer_mpu6500.init(period=10, mode=Timer.PERIODIC, callback=read_mpu6500)
timer_rms.init(period=2_000, mode=Timer.PERIODIC, callback=process_rms)
timer_move.init(period=1_000, mode=Timer.PERIODIC,callback=process_move)
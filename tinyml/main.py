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

print('Starting ESP32 script.')

gc.collect()
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_M_S2, gyro_sf=SF_DEG_S)

gc.collect()
global data
data = Data(freq=25, n_signals=3)

def read_mpu6500(timer):
    gc.collect()
    print('T {}'.format(utime.ticks_ms()))
    acc = mpu6500.acceleration # collect x,y acceleration
    gyro = mpu6500.gyro
    data.collect([acc[0],acc[1]], [gyro[2]])
    print('Alloc: {} | Free: {}'.format(gc.mem_alloc(), gc.mem_free()))
    # print(utime.ticks_ms(),mpu6500.acceleration, mpu6500.gyro)

def read_sensor():
    Timer(0).init(freq=25, mode=Timer.PERIODIC, callback=read_mpu6500)

# def send_rms_data(interval):
#     while True:
#         gc.collect()
#         utime.sleep(interval)
#         post_request_rms(data.get_rms_acc_x(), data.get_rms_acc_y(), data.get_rms_acc_z())

# def send_move_data(interval):
#     import urandom
#     while True:
#         gc.collect()
#         utime.sleep(interval)
#         post_request_move(urandom.getrandbits(2))


_thread.start_new_thread(read_sensor,())
# _thread.start_new_thread(send_rms_data,(3,))
# _thread.start_new_thread(process_move, (3,))
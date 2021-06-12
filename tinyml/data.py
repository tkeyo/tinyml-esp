import math
# %%

class Data:
    def __init__(self, freq, n_signals):
        self.n_signals = n_signals
        self.capacity = (freq * self.n_signals) + self.n_signals
        self.buffer = []
    
    def _scale(self, vals, xmin, xmax, resolution):
        return [int((x-xmin)/(xmax-xmin)*resolution) for x in vals]

    def _round(self, vals, places=4):
        return [round(x, places) for x in vals]

    def _is_full(self):
        return len(self.buffer) > self.capacity

    def _calc_rms(self, vals: list) -> float:
        pow = math.pow
        l = len(vals)
        return math.sqrt(sum([pow(x,2) for x in vals]) / l)
 
    def collect(self, acc=None, gyro=None):
        while self._is_full():
            self.buffer.pop(0)
        if acc:
            self.buffer.extend(acc)
        if gyro:
            self.buffer.extend(gyro)

    def get(self):
        return self.buffer

    def rms(self, signal: int):
        """Params: signal index"""
        return self._calc_rms(self.buffer[signal:][0::3])

    def size(self):
        return len(self.buffer)


# data = Data(20, 5)

# data.buffer = [2] * 200

# for i in range(100):
#     data.collect([1,2,3],[1,2])
#     print(len(data.get()))

# import utime

# start = utime.ticks_ms()
# for i in range(10_000):
#     data.collect([i*0.00002, i*0.0000025], [i*0.00002, i*0.0000025])
# print(utime.ticks_ms() - start, 'ms')


### testing
# for i in range(200):
#     data.collect([i*0.00002, i*0.0000025], [i*0.00002, i*0.0000025])

# start = utime.ticks_us()
# # for _ in range(1):
# data.rms(0)
# data.rms(1)
# data.rms(2)
# print(utime.ticks_us() - start, 'us')

# dt = data.get_buffer()
# print(len(dt))

# print(dt)
# print(data.get_rms(0))
# print(data.get_rms(1))
# print(data.get_rms(2))

# print(dt)
# print(dt[0:][0::3], len(dt[0::3]))
# print(dt[1:][0::3], len(dt[1:][0::3]))
# print(dt[2:][0::3], len(dt[1:][0::3]))

# %%

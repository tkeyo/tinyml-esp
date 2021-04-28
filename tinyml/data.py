import math
# %%

class Data:
    def __init__(self, freq, n_signals):
        self.n_signals = n_signals
        self.capacity = (freq + 1) * self.n_signals
        self.buffer = list()
    
    def _scale(self, vals, xmin, xmax, resolution):
        return [int((x-xmin)/(xmax-xmin)*resolution) for x in vals]

    def _is_full(self):
        return len(self.buffer) >= self.capacity
 
    def collect(self, acc=None, gyro=None):
        if self._is_full():
            for _ in range(self.n_signals):
                self.buffer.pop(0)
        if acc:
            self.buffer.extend(self._scale(acc, -19.6, 19.6, 255))
        if gyro:
            self.buffer.extend((self._scale(gyro, -250, 250, 255)))

    def get_buffer(self):
        return self.buffer

    def _calc_rms(self, vals: list) -> float:
        pow = math.pow
        return math.sqrt(sum([pow(x,2) for x in vals]) / len(vals))

    def get_rms(self, pos):
        return self._calc_rms(self.buffer[pos:][0::3])



# data = Data(25, 4)

# import utime

# start = utime.ticks_us()
# for i in range(100):
#     data.collect([i*0.02, i*0.025])
# print(utime.ticks_us() - start)

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

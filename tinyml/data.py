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

    @property
    def data(self):
        return self.buffer
    

    def get_rms(self, signal: int):
        """Params: signal index"""
        return self._calc_rms(self.buffer[signal:][0::3])

    @property
    def size(self):
        return len(self.buffer)

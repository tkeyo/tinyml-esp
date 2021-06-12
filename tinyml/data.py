import math

class Data:
    def __init__(self, freq, n_signals):
        self.n_signals = n_signals
        self.capacity = (freq * self.n_signals) + self.n_signals
        self.buffer = []
        
    @property
    def size(self) -> int:
        return len(self.buffer)
    
    @property
    def data(self) -> list:
        return self.buffer

    def _scale(self, vals: list, xmin: int, xmax: int, resolution:) -> list:
        return [int((x-xmin)/(xmax-xmin)*resolution) for x in vals]

    def _round(self, vals: list, places: int=4) -> list:
        return [round(x, places) for x in vals]

    def _is_full(self) -> bool:
        return len(self.buffer) > self.capacity

    def _calc_rms(self, vals: list) -> float:
        pow = math.pow
        l = len(vals)
        return math.sqrt(sum([pow(x,2) for x in vals]) / l)
 
    def collect(self, acc: list=None, gyro:list=None) -> None:
        while self._is_full():
            self.buffer.pop(0)
        if acc:
            self.buffer.extend(acc)
        if gyro:
            self.buffer.extend(gyro)

    def get_rms(self, signal: int) -> float:
        """Params: signal index"""
        return self._calc_rms(self.buffer[signal:][0::3])

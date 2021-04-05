import math

class Data:
    def __init__(self, samples=100):
        self.samples = samples

    def init(self, collect=['acc']):
        print('Variables initialized: {}'.format(collect))
        if 'acc' in collect:
            self._init_acc()
        if 'gyro' in collect:
            self._init_gyro()

    def _init_acc(self):
        self.acc_x = list()
        self.acc_y = list()
        self.acc_z = list()

    def _init_gyro(self):
        self.gyro_x = list()
        self.gyro_y = list()
        self.gyro_z = list()

    def collect_acc(self, val):
        if len(self.acc_x) == self.samples:
            self.acc_x.pop(0)
            self.acc_y.pop(0)
            self.acc_z.pop(0)
        else:
            self.acc_x.append(val[0])
            self.acc_y.append(val[1])
            self.acc_z.append(val[2])

    def collect_gyro(self, val):
        if len(self.gyro_x) == self.samples:
            self.gyro_x.pop(0)
            self.gyro_y.pop(0)
            self.gyro_z.pop(0)
        else:
            self.gyro_x.append(val[0])
            self.gyro_y.append(val[1])
            self.gyro_z.append(val[2])

    @micropython.native
    def _calc_rms(self, vals: list) -> float:
        pow = math.pow
        return math.sqrt(sum([pow(x,2) for x in vals]) / self.samples)

    def get_rms_acc_x(self):
        return self._calc_rms(self.acc_x)
    
    def get_rms_acc_y(self):
        return self._calc_rms(self.acc_y)

    def get_rms_acc_z(self):
        return self._calc_rms(self.acc_z)

    def get_rms_gyro_x(self):
        return self._calc_rms(self.gyro_x)
    
    def get_rms_gyro_y(self):
        return self._calc_rms(self.gyro_y)

    def get_rms_gyro_z(self):
        return self._calc_rms(self.gyro_z)


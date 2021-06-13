import math


class Data:
    '''
        Class to process data collected from accelerometer.
        
        Attributes:
            n_signals: Number of unique signals that will be stored.
            cap: Calculated capacity needed to have 1 second of signal data.
            buffer: Collected data is stored in buffer.
    '''

   
    def __init__(self, freq, n_signals):
        '''Initializes Data class with `n_signals`,`cap`, `buffer`.'''
        self.n_signals = n_signals
        self.cap = (freq * self.n_signals) + self.n_signals
        self.buffer = []


    @property
    def size(self) -> int:
        '''Returns the size of the collected data buffer.'''
        return len(self.buffer)

 
    @property
    def capacity(self) -> int:
        '''Returns the capacity of Data class.'''
        return self.cap

   
    @property
    def data(self) -> list:
        '''Returns collected data.'''
        return self.buffer


    def _scale(self, vals: list, xmin: int, xmax: int, f_range: int) -> list:
        '''
            Rescales data from 0 to defined value.
            
            Args:
                vals: List of values to rescale.
                xmin: Min value refernce.
                xmax: Max value reference.
                f_range: Feature range from 0 to defined value.
            Returns:
                List of scales values.
        '''
        return [int((x-xmin)/(xmax-xmin)*f_range) for x in vals]


    def _round(self, vals: list, places: int=4) -> list:
        '''
            Rounds float values int a list to defined decimal points.
            
            Args:
                vals: List of values to round.
                places: Number of decimal places for rounding.   
            Returns:
                List of rounded floats.
        '''
        return [round(x, places) for x in vals]


    def _is_full(self) -> bool:
        '''
            Verifies if buffer has capacity to add new values.
            (self.capacity - self.n_signals) - number of signals must be 
            subtracted as new values will be added after check.
            
            Returns:
                True if buffer is larger than capacity - # of signals
        '''
        return len(self.buffer) > (self.cap - self.n_signals)


    def _calc_rms(self, vals: list) -> float:
        '''
            Calculates the root mean square of a signal.
            
            Args:
                vals: List of ints or floats.
            Returns:
                Root mean square of input values.
        '''
        pow = math.pow # method preloading for speedup
        l = len(vals)
        return math.sqrt(sum([pow(x,2) for x in vals]) / l)
 
 
    def collect(self, acc: list=None, gyro:list=None) -> None:
        '''
            Collects and regulates data in buffer.
            
            Args:
                acc: List of acceleration sensor reading values.
                gyro: List of gyroscope sensor reading values.
        '''
        while self._is_full():
            self.buffer.pop(0)
        if acc:
            self.buffer.extend(acc)
        if gyro:
            self.buffer.extend(gyro)


    def get_rms(self, signal: int) -> float:
        '''
            Gets root mean square (RMS) of defined signal.
            
            Args:
                signal: Number of signal in order as collected.
                        Depends on how signals are defined in `collect` method.
                        Given `Data.collect([acc_x, acc_y],[gyro_x])` and 
                        `get_rms(1)` - this method will return the RMS of `acc_y`.
            Returns:
                RMS of a signal.
        '''
        return self._calc_rms(self.buffer[signal:][0::3])

import utime
from micropython import const


unix_base = const(946681200) # utime.gmtime(0) - epoch 0


def get_time() -> int:
    '''
        Gets current time in ms format. Time must be synced with ntp 
        in order to be accurate.
    '''
    return (utime.mktime(utime.gmtime()) + unix_base + 3600) * 1000


def get_time_diff(inf_tuples: list) -> int:
    '''
        Calculates the time difference between the first and last 
        inference in a list of inference tuples.
        
        Args:
            inf_tuples: List of tuples containing time and inference data.
        Returns:
            Time difference between first and last inference.
    '''
    if len(inf_tuples) >= 2:
        return utime.ticks_diff(inf_tuples[-1][0], inf_tuples[0][0])
    else:
        return 0


def get_final_inf_res(infs: list) -> int:
    '''
        Gets the most frequent inference result in a list of inferences.

        Args:
            infs: List of inference results.   
        Returns:
            Returns the most frequent value in a list.
    '''
    return max(set(infs), key=infs.count)


def reduce_infs(inf_tuples: list) -> list:
    '''
        Returns the first defined number of inferences in a list inference tuples.
        
        Args:
            inf_tuples: List of inference tuples. Format of tuple `(time, inference).`
        Returns:
            List of first n inferences.
    '''
    return [x[1] for x in inf_tuples[:9]]


def debounce(inf_tuples: list, time_diff: int) -> (int, list):
    '''
        Debounces inferences - returns the most prevalent
        score from the collected inference results.
        
        Args:
            inf_tuples: List of inference tuples. Format `(time,inference)`.
            time_diff: Difference between first and last inference in a list.
        Returns:
            result: Most prevalent inference result.
            reduced_infs: List of first n collected inference values.
    '''
    if len(inf_tuples) >= 9 and time_diff > 450:
    #     # start_time = utime.ticks_ms()
        reduced_infs = reduce_infs(inf_tuples)
        result = get_final_inf_res(reduced_infs)
        return result, reduced_infs
    else:
        return None


def clean_inf_tuples(inf_tuples: list, time_diff: int) -> list:
    '''
        Purges inference tuples buffer.
        
        Args:
            inf_tuples: List of inference tuples. Format `(time,inference)`.
            time_diff: Difference between first and last inference in a list.
        Returns:
            List of inference tuples.
    '''
    if len(inf_tuples) <= 8 and time_diff >= 1_000:
        return []
    else:
        return inf_tuples
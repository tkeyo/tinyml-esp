import utime
from micropython import const


unix_base = const(946681200) # utime.gmtime(0) - epoch 0


def get_time() -> int:
    '''
        Gets current time in ms format. Time must be synced with ntp 
        to be accurate.
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


def reduce_infs(inf_tuples: list, min_tuples: int) -> list:
    '''
        Returns the first defined number of inferences in a list inference tuples.
        
        Args:
            inf_tuples: List of inference tuples. Format of tuple `(time, inference).`
            min_tuples: Number of inferences to return from list of tuples.
        Returns:
            List of first n inferences.
    '''
    return [x[1] for x in inf_tuples[:min_tuples]]


def debounce(inf_tuples: list, time_diff: int, 
             min_tuples: int, min_t_diff: int) -> int:
    '''
        Debounces inferences - returns the most prevalent
        score from the collected inference results.
        
        Args:
            inf_tuples: List of inference tuples. Format `(time,inference)`.
            time_diff: Difference between first and last inference in a list.
            min_tuples: Number of inferences to return from list of tuples.
            min_t_diff: Min. time difference between first and last inference.
        Returns:
            result: Most prevalent inference result.
            reduced_infs: List of first n collected inference values.
    '''
    if len(inf_tuples) >= min_tuples and time_diff > min_t_diff:
        reduced_infs = reduce_infs(inf_tuples, min_tuples)
        result = get_final_inf_res(reduced_infs)
        print('{} -> {}'.format(reduced_infs, result))
        return result
    else:
        return None


def clean_inf_tuples(inf_tuples: list, time_diff: int,
                     max_tuples: int, max_t_diff: int) -> list:
    '''
        Purges inference tuples buffer.
        
        Args:
            inf_tuples: List of inference tuples. Format `(time,inference)`.
            time_diff: Difference between first and last inference in a list.
        Returns:
            List of inference tuples.
    '''
    if len(inf_tuples) <= max_tuples and time_diff >= max_t_diff:
        return []
    else:
        return inf_tuples

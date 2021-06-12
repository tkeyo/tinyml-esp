import utime
from micropython import const

unix_base = const(946681200) # utime.gmtime(0) - epoch 0

def get_time():
    return (utime.mktime(utime.gmtime()) + unix_base + 3600) * 1000

def get_time_diff(inf_tuples):
    """List of tuples"""
    if len(inf_tuples) >= 2:
        return utime.ticks_diff(inf_tuples[-1][0], inf_tuples[0][0])
    else:
        return 0

def get_final_inf_res(infs):
    return max(set(infs), key=infs.count)


def reduce_infs(inf_tuples):
    return [x[1] for x in inf_tuples[:9]]

def debounce(inf_tuples, time_diff):
    if len(inf_tuples) >= 9 and time_diff > 450:
    #     # start_time = utime.ticks_ms()
        reduced_infs = reduce_infs(inf_tuples)
        result = get_final_inf_res(reduced_infs)
        return result, reduced_infs
    else:
        return None, None
import pytest
from tinyml.data import Data

@pytest.fixture
def data():
    return Data(freq=3, n_signals=3)

def test_capacity(data):
    assert data.capacity == 12 

@pytest.mark.parametrize(
    'acc_x, acc_y, gyro_x, expected_buffer_size',
    [
        ([1,2,3], [1,2,3], [1,2,3], 9),
        (
            [1,2,3,4,5,6],
            [11,12,13,14,15,16],
            [21,22,23,24,25,26],
            12
        )
    ]
)
def test_collect_buffer_size(data, acc_x, acc_y, gyro_x, expected_buffer_size): 
    for i in range(len(acc_x)):
        a_x = acc_x[i]
        a_y = acc_y[i]
        g_x = gyro_x[i]

        data.collect(acc=[a_x, a_y],gyro=[g_x])
    assert data.size == expected_buffer_size


@pytest.mark.parametrize(
    'acc_x, acc_y, gyro_x, expected_buffer',
    [
        ([1,2,3], [1,2,3], [1,2,3], [1,1,1,2,2,2,3,3,3]),
        (
            [1,2,3,4,5,6],
            [11,12,13,14,15,16],
            [21,22,23,24,25,26],
            [3,13,23,4,14,24,5,15,25,6,16,26]
        )
    ]
)
def test_collect_buffer_data(data, acc_x, acc_y, gyro_x, expected_buffer):
    for i in range(len(acc_x)):
        a_x = acc_x[i]
        a_y = acc_y[i]
        g_x = gyro_x[i]

        data.collect(acc=[a_x, a_y],gyro=[g_x])
    assert data.data == expected_buffer


@pytest.mark.parametrize(
    'signal, acc_x, acc_y, gyro_x, expected_rms',
    [
        (0,[1,2,3], [11,12,13], [21,22,23], 2.160),
        (1,[1,2,3], [11,12,13], [21,22,23], 12.027),
        (2,[1,2,3], [11,12,13], [21,22,23], 22.015)
    ]
)
def test_get_rms_x(data, signal, acc_x, acc_y, gyro_x, expected_rms):
    for i in range(len(acc_x)):
        a_x = acc_x[i]
        a_y = acc_y[i]
        g_x = gyro_x[i]

        data.collect(acc=[a_x, a_y],gyro=[g_x])
    
    assert pytest.approx(data.get_rms(signal), rel=0.01) == expected_rms

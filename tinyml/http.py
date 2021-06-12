import ujson
import urequests
from micropython import const
from secret.secret import URL, AUTHORIZATION, MOVE_ENDPOINT, RMS_ENDPOINT


headers = {
    'Content-Type': 'application/json',
    'Authorization': AUTHORIZATION
    }


def get_api_endpoint(t):
    '''Maps REST API endpoints to target.'''
    endpoint_mapping = {
        'rms':RMS_ENDPOINT,
        'move':MOVE_ENDPOINT
    }
    return endpoint_mapping.get(t, 'missing')


def request_post(time, api_target, payload):
    '''Sends POST requests to REST API endpoints.'''
    data = ujson.dumps(payload)
    endpoint = get_api_endpoint(api_target)
    try:
        res = urequests.post(
                '{}/{}'.format(URL, endpoint),
                data=data,
                headers=headers
                )
        res.close()
    except OSError as e:
        print('Error: {}'.format(e))

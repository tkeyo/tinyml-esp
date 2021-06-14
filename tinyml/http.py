import ujson
import urequests
from micropython import const
from config.secret import (URL, 
                           AUTHORIZATION, 
                           MOVE_ENDPOINT, 
                           RMS_ENDPOINT,
                           IS_CONNECT_WIFI)


headers = {
    'Content-Type': 'application/json',
    'Authorization': AUTHORIZATION
    }


def get_api_endpoint(t: str) -> str:
    '''
        Maps REST API endpoints to target.
        
        Args:
            t: Target endpoint key.
        Returns:
            API endpoint string.
    '''
    endpoint_mapping = {
        'rms':RMS_ENDPOINT,
        'move':MOVE_ENDPOINT
    }
    endpoint = endpoint_mapping.get(t, '')
    
    if endpoint:
        return endpoint
    else:
        raise KeyError('Endpoint {} key is not defined.'.format(endpoint))


def request_post(api_target: str, payload: dict):
    '''
        Sends POST requests to REST API endpoints.
        
        Args:
            api_target: Target of data - `move` or `rms`
            payload: Data to be sent to the endpoint.
    '''
    endpoint = get_api_endpoint(api_target)
    data = ujson.dumps(payload)
    
    if IS_CONNECT_WIFI:
        try:
            res = urequests.post(
                    '{}/{}'.format(URL, endpoint),
                    data=data,
                    headers=headers)
            res.close()
        except OSError as e:
            print('Error: {}'.format(e))
    else:
        print('Not connected to WiFi. Running in Offline mode.')

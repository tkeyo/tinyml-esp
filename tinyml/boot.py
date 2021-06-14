def do_connect():
    '''Creates connection to WiFi based on configuration in `secrets.py`.'''
    import network
    from config import secret

    if secret.IS_CONNECT_WIFI:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('[Boot] Connecting to WiFi...')
            wlan.connect(secret.SSID, secret.PASS)
            while not wlan.isconnected():
                pass
        print('[Boot] Connected to WiFI. Config: {}'.format (wlan.ifconfig()))
    else:
        print('[Boot] Not connecting to WiFi. Running in Offline mode.')


def sync_time():
    '''Synchronizes time with ntptime host.'''
    import ntptime
    import utime
    import sys
    from config import secret
    if secret.IS_CONNECT_WIFI:
        try:
            ntptime.host = '0.europe.pool.ntp.org'
            ntptime.settime()
            print('[Boot] Time synced: {}'.format(str(utime.gmtime())))
        except OSError as e:
            print('[Boot] Error while syncing time: {}'.format(e))
            sys.exit()
    else:
        print('[Boot] Running in Offline mode. Time is note synced.')

      
def set_frequency():
    '''Sets CPU frequency of ESP32.'''
    import machine
    machine.freq(240000000)
    print('[Boot] Machine freq set to: {} MHz'.format(int(machine.freq() / 1_000_000)))


if __name__ == '__main__':
    do_connect()
    sync_time()
    set_frequency()
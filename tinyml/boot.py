def do_connect():
    import network
    from secret import secret

    if secret.IS_CONNECT_WIFI:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('Connecting to WiFi...')
            wlan.connect(secret.SSID, secret.PASS)
            while not wlan.isconnected():
                pass
        print('Network config: ', wlan.ifconfig())
    else:
        print('WiFi Connect OFF')

def set_time():
    import ntptime
    import utime
    import sys
    from secret import secret
    if secret.IS_CONNECT_WIFI:
        try:
            ntptime.host = '0.europe.pool.ntp.org'
            ntptime.settime()
            print("Time after synchronization：%s" %str(utime.gmtime()))
        except OSError as e:
            print('Error: {}'.format(e))
            sys.exit()
    else:
        print('Time not synchronized')
        
def set_frequency():
    import machine
    print('Machine freq: {} MHz'.format(int(machine.freq() / 1_000_000)))
    machine.freq(240000000)
    print('Machine freq set to: {} MHz'.format(int(machine.freq() / 1_000_000)))

do_connect()
set_time()
set_frequency()
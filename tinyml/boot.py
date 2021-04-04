def do_connect():
    import network
    from secret import wifi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(wifi.SSID, wifi.PASS)
        while not wlan.isconnected():
            pass
    print('Network config: ', wlan.ifconfig())

def set_time():
    import ntptime
    import utime
    ntptime.host = '0.europe.pool.ntp.org'
    ntptime.settime()
    print("Time after synchronization：%s" %str(utime.gmtime()))

def set_frequency():
    import machine
    print('Machine freq: {} MHz'.format(int(machine.freq()/1_000_000)))
    machine.freq(240000000)
    print('Machine freq set to: {} MHz'.format(int(machine.freq()/1_000_000)))

do_connect()
set_time()
set_frequency()
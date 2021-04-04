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
    print('Network config:', wlan.ifconfig())

do_connect()
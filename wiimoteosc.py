#! /usr/bin/python

import cwiid
import time
import OSC

def setup_wiimote(ip):
    while not wm:
        try:
            wm = cwiid.Wiimote()
        except RuntimeError:
            msg.clear()
            msg.setAddress("/wiimote")
            msg.append("Error Opening Wiimote Connection")
            client.send(msg)
            print("Error Opening Wiimote Connection")

    wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_EXT

    led = 0
    if ip & 1: led += 8
    if ip & 2: led += 4
    if ip & 4: led += 2
    if ip & 8: led += 1
    wm.led = led

def get_ip():
    network_interfaces = open("/etc/network/interfaces", "r")
    for line in network_interfaces:
        if line.startswith("static ip_address") or line.startswith("address"):
            return line[-2:-1]
    return None



wm = None

client = OSC.OSCClient()

ip = getIP()
if not ip:
    print("Fatal Error")
    exit(-1)

ip = (ord(ip) - ord('0')) & 0xf

while client.client_address == None:
    try:
        client.connect(("10.0.1.1", 7000 + ip))
    except OSC.OSCClientError:
        continue

msg = OSC.OSCMessage()

while True:
    if not wm:
        setup_wiimote(ip)
    msg.clear()
    msg.setAddress("/wiimote/buttons")
    msg.append(str(wm.state['buttons']))
    client.send(msg)
    msg.clear()
    msg.setAddress("/wiimote/acc")
    msg.append(str(wm.state['acc']))
    client.send(msg)
    msg.clear()
    if 'nunchuk' in wm.state.keys():
        msg.setAddress("/wiimote/nunchuk/buttons")
        msg.append(str(wm.state['nunchuk']['buttons']))
        client.send(msg)
        msg.clear()
        msg.setAddress("/wiimote/nunchuk/acc")
        msg.append(str(wm.state['nunchuk']['acc']))
        client.send(msg)
    time.sleep(0.1)

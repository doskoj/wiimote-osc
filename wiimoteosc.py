#! /usr/bin/python

import cwiid
from python-osc import udp_client
from python-osc import osc_message_builder
import time
import socket

wm = None
client = udp_client.SimpleUDPClient("10.0.0.1", 8008)
while not wm:
    try:
        wm = cwiid.Wiimote()
        host_name = socket.gethostname()
        ip = socket.gethostbyname(host_name)
        wm.led = ord(ip[-1:]) & 0xf
    except RuntimeError:
        client.send_message("/wiimote", "Error Opening Wiimote Connection")
        pritn("Error Opening Wiimote Connection")

wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

while True:
    print(wm.state)
    client.send_message("/wiimote/buttons", wm.state['buttons'])
    if (wm.state['buttons'] & cwiid.BTN_1):
        client.send_message("/wiimote/buttons/1", 1)
    client.send_message("/wiimote/acc", wm.state['acc'])
    time.sleep(0.1)

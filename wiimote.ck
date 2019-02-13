OscIn oin;
OscMsg msg;

8008 => oin.port;

oin.event("/wiimote") @=> wiimote_event;

while (true) {
  wiimote_event => now;

  while (wiimote_event.nextMsg() != 0) {
    <<< wiimote_event.address, wiimote_event.getString(0) >>>;
  }
}

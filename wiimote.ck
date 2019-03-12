OscIn oin;
OscMsg msg;

7009 => oin.port;

oin.listenAll();

while (true) {
  oin => now;

  while (oin.recv(msg)) {
    <<< msg.address, msg.getString(0) >>>;
    // msg.getSting(0);
    //if (msg.address == "/wiimote/buttons") {
    //}
  }
}

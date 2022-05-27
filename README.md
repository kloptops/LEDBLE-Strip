# LEDBLE-Strip
Ledble is a basic BLE LED RGB strip controller for a super cheap LED RGB strip.

I have used the work of [kquinsland](https://github.com/kquinsland/JACKYLED-BLE-RGB-LED-Strip-controller)'s reverse engineering efforts and decompiling the official android app for the strip to fill in the missing pieces.


Progress:
- [x] Turn on and off
- [x] Set rgb color
- [x] Set rgb color sort
- [x] Set rgb mode (pre-programmed sequences)
- [ ] On / Off timer
- [ ] DIY mode
- [x] Sequence speed
- [ ] Brightness doesnt work
- [x] Dimming works
- [x] Set "dynamic" mode (4 more pre-programmed sequences...)

TODO:
- [ ] Figure out why it disconnects so frequently when sending multiple commands, maybe sending it too fast?
- [ ] Add all the supported functions of the LED strip
- [ ] Add support for multiple LED strips
- [ ] Add scanning system



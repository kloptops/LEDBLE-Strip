# LEDBLE-Strip
Ledble is a basic BLE LED RGB strip controller for a super cheap LED RGB strip.

I have used the work of [kquinsland](https://github.com/kquinsland/JACKYLED-BLE-RGB-LED-Strip-controller)'s reverse engineering efforts and decompiling the official android app for the strip to fill in the missing pieces.


Progress:
- [x] Turn on and off
- [x] Set rgb color
- [x] Set rgb color sort
- [x] Set rgb mode (pre-programmed sequences)
- [x] Sequence speed
- [x] Dimming works
- [x] Set "dynamic" mode (4 more pre-programmed sequences...)
- [ ] On / Off timer, still cant get it to work.
- [ ] DIY mode, (pointless)
- [ ] Brightness doesnt work

TODO:
- [x] ~~Figure out why it disconnects so frequently when sending multiple commands, maybe sending it too fast?~~ It appears to be a linux bluez/bleak issue on raspberry pi.
- [x] Add all the supported functions of the LED strip
- [ ] Add support for multiple LED strips
- [ ] Add scanning system
- [ ] Format it as a module correctly and add it to pypi

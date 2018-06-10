# acestream-rpi

This project is an attempt at playing AceStreams on a Raspberry Pi 2/3 with Raspbian Lite without X.

It works with the [AceStream Engine borrowed from Android](https://github.com/ronniehd/plexus-dependencies/tree/master/Modules/Linux/arm/rpi2), coupled with a [HTTP proxy](https://github.com/AndreyPavlenko/aceproxy) and the omxplayer.

## Installation and Usage

* Install Raspbian Lite on Raspberry Pi 2/3.
* Configure the network.
* Clone the repository.
* Run `./acestream-rpi/start.sh` directly on the Raspberry Pi (no SSH).
* This downloads all the dependencies and starts the system.
* After the system is running use `./play.sh ACESTREAM_HASH` to start a stream.
* By default omxplayer outputs to the HDMI port (edit `./play.sh` for your needs).

## Kiosk mode

* Run `./acestream-rpi/start.sh [<program>]` with program parameter, this puts the system in kiosk mode and runs the program. When the program exits the system will shutdown. The program should be some kind of CLI AceStream provider. Right now you can use `./acestream-rpi/start.sh ./kiosk.sh` as an example.

## Setup lirc (IR remote control)

Run `./acestream-rpi/setup-lirc.sh` to install [lirc](http://www.lirc.org/). This can be used to control the system using a IR remote in kiosk mode. You will need some kind of IR receiver connected to GPIO18, like the [TSOP4838](https://www.google.com/search?q=TSOP4838+raspberry+pi+lirc).

### Configure a remote control

* Stop the daemons, `sudo service lircd stop`.
* Create a remote config using `irrecord` (on Raspbian Stretch you may need to use raw mode, `irrecord -f`, due to a bug).
* Register at least the keys: KEY_UP, KEY_DOWN, KEY_ENTER and KEY_BACKSPACE.
* Copy the config file to `/etc/lirc/lircd.conf.d/`.
* Start the daemons, `sudo service lircd start` and `sudo service lircd-uinput start`
* Now the remote control should emulate the keyboard keys.

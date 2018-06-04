# acestream-rpi

This project is an attempt at playing AceStreams on a Raspberry Pi 2/3 with Raspbian Lite without X.

It works with the [AceStream Engine borrowed from Android](https://github.com/ronniehd/plexus-dependencies/tree/master/Modules/Linux/arm/rpi2), coupled with a [HTTP proxy](https://github.com/AndreyPavlenko/aceproxy) and the omxplayer player.

## Installation and Usage

* Install Raspbian Lite on Raspberry Pi 2/3.
* Configure the network.
* Clone the repository.
* Run `./acestream-rpi/start.sh` directly on the Raspberry Pi (no SSH).
* This downloads all the dependencies and starts the system.
* After the system is running use `./play.sh ACESTREAM_HASH` to start a stream.
* By default omxplayer outputs to the HDMI port (edit `./play.sh` for your needs).

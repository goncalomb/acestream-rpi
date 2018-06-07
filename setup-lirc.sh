#!/bin/bash

set -e

if command -v lircd >/dev/null; then
    echo "lirc already installed, run 'sudo apt-get purge -y lirc' to remove"
    exit 1
fi

# install lirc
sudo apt-get update
sudo apt-get install -y lirc

# enable lirc-rpi module
sudo sed -i 's/^#dtoverlay=/dtoverlay=/g' /boot/config.txt

# configure lirc
sudo python3 << EOF
import configparser;

parser = configparser.ConfigParser()
with open('/etc/lirc/lirc_options.conf', 'r') as fp:
    parser.read_file(fp)

parser.set('lircd', 'driver', 'default')
parser.set('lircd', 'device', '/dev/lirc0')

if not parser.has_section('lircd-uinput'):
    parser.add_section('lircd-uinput')

parser.set('lircd-uinput', 'add-release-events', 'True')
parser.set('lircd-uinput', 'release-timeout', '150')
parser.set('lircd-uinput', 'repeat', '700,50')

with open('/etc/lirc/lirc_options.conf', 'w') as fp:
    parser.write(fp)
EOF

echo "REBOOT in 5 seconds, CTRL-C to cancel"
sleep 5
sudo reboot

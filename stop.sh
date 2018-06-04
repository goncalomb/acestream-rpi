#!/bin/bash

cd "$(dirname -- "$0")"

# kill aceproxy
killall python python2 python3

# kill acestream
./ext/acestream/stop_acestream.sh

sleep 1
clear

# kill parent process (bash)
kill -HUP $(ps -p $$ -o ppid= | tr -d " \n")

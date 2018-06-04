#!/bin/bash

omxplayer -b -o hdmi --live --timeout 30 "http://localhost:8000/pid/$1/stream.mp4"

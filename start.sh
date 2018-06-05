#!/bin/bash

set -e

if [ "$(tty)" != "/dev/tty1" ]; then
    exit 1
fi

cd "$(dirname -- "$0")"

mkdir -p ext
cd ext
# install dependencies
if ! command -v omxplayer >/dev/null; then
    sudo apt-get update
    sudo apt-get install -y git screen python-gevent python-psutil python-requests python3-requests python3-lxml python3-cssselect omxplayer
fi
# download acestream engine
if [ ! -d acestream ]; then
    wget -c "https://github.com/ronniehd/plexus-dependencies/raw/aa692759e838aeb560cd922afa5af44878d36d84/Modules/Linux/arm/rpi2/acestream-raspberry.tar.gz"
    tar -xf acestream-raspberry.tar.gz
    cat << 'EOF' > acestream.sh
#!/bin/bash
cd "$(dirname -- "$0")"
finish() {
    ./acestream/stop_acestream.sh
    echo "AceStream Engine stopped."
    trap - EXIT INT TERM
    sleep 0.5
}
trap finish EXIT INT TERM
echo "AceStream Engine started..."
./acestream/start_acestream.sh --client-console
EOF
    chmod +x acestream.sh
fi
# download acestream proxy
if [ ! -d aceproxy ]; then
    git clone "https://github.com/AndreyPavlenko/aceproxy.git"
    git -C aceproxy checkout -q 2561431d28f0b8455a156d7423b305491f1d1b0a || { rm -rf aceproxy && false; }
fi
# create console.sh
if [ ! -f console.sh ]; then
    cat << 'EOF' > console.sh
#!/bin/bash
echo
echo "  AceStream for Raspbian Lite"
echo
echo "  use './play.sh ACESTREAM_HASH' to start a stream"
echo "  use './stop.sh' to exit"
echo
bash
EOF
    chmod +x console.sh
fi
cd ..

TMP_FILE=$(mktemp)
cat << EOF > "$TMP_FILE"
startup_message off
defscrollback 10000

screen -t console ./ext/console.sh
split -v
focus right
screen -t ace-engine ./ext/acestream.sh
split
focus down
screen -t ace-proxy python ./ext/aceproxy/acehttp.py
focus left
EOF
screen -c "$TMP_FILE"
rm "$TMP_FILE"

clear

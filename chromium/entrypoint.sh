#!/bin/bash -x

export NODE_PATH=/usr/lib/node_modules:$NODE_PATH

use_squid(){
   export ftp_proxy=http://squid:3128
   export http_proxy=http://squid:3128
   export https_proxy=http://squid:3128
}

start_chromium(){
   xvfb-run chromium-browser --server-args="-screen 99 1024x768x24" --load-extension=/opt/crawler/ --remote-debugging-port=9222 --disable-gpu --no-sandbox  https://www.google.com &
}

start_vnc(){
   export XAUTHORITY=$(find /tmp -name "Xauthority")
   mkdir -p /root/.vnc/ && echo "1" > /root/.vnc/passwd
   x11vnc -passwdfile /root/.vnc/passwd -display :99.0 -usepw -forever -autoport 5900
}

if [ "$1" == "bash" ]; then
    exec $@
elif [ "$1" == "vnc" ]; then
    if [ ! -z "$USE_SQUID" ]; then
        use_squid
    fi
    start_chromium
    sleep 30
    start_vnc
elif [ "$1" == "davivienda" ]; then
    URL="https://transacciones.davivienda.com/dinamicos/ComercialServlet?item=fondos&canal=inter&consulta=dafuturo"
    cp -f /opt/crawler/davivienda/contentScript.js /opt/crawler/contentScript.js
    cp -f /opt/crawler/davivienda/manifest.json /opt/crawler/manifest.json
    start_chromium
    sleep 30
    nodejs /opt/scripts/screenshot.js $URL
    cp /root/Downloads/* /tmp/results/
elif [ "$1" == "bancolombia" ]; then
    URL="https://www.grupobancolombia.com/personas/productos-servicios/inversiones/fondos-inversion-colectiva/aplicacion-fondos?"
    for i in $(seq 0 23); do
        cp -f /opt/crawler/bancolombia/contentScript.js /opt/crawler/contentScript.js
        cp -f /opt/crawler/bancolombia/manifest.json /opt/crawler/manifest.json
        start_chromium
        sleep 30
        nodejs /opt/scripts/screenshot.js "$URL$i"
        cp -f /root/Downloads/* /tmp/results/
    done
elif [ "$1" == "mercadolibre" ]; then
    use_squid
    cp -f /opt/crawler/mercadolibre/contentScript.js /opt/crawler/contentScript.js 
    start_chromium
    sleep 30
    nodejs /opt/scripts/screenshot.js
    cp /root/Downloads/* /tmp/results/
fi







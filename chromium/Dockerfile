FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y curl xvfb chromium-browser x11vnc procps 

RUN curl -sL https://deb.nodesource.com/setup_13.x |  bash -
RUN apt-get update && apt-get install -y nodejs

RUN npm -g install chrome-remote-interface

RUN mkdir -p /opt/scripts
COPY screenshot.js /opt/scripts/screenshot.js
COPY entrypoint.sh /opt/entrypoint.sh
ADD crawler /opt/crawler

RUN chmod -R 777 /opt/scripts
RUN chmod +x /opt/entrypoint.sh
RUN chmod 777 /opt/entrypoint.sh

RUN useradd chromium && mkdir /home/chromium && chown -R chromium:chromium /home/chromium

RUN mkdir /opt/runs
WORKDIR /opt/runs

ENTRYPOINT ["/opt/entrypoint.sh"]

CMD ["vnc"]

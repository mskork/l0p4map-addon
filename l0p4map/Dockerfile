FROM ghcr.io/home-assistant/amd64-base:latest

RUN apk add --no-cache \
    nmap \
    python3 \
    py3-pip \
    git \
    libpcap \
    qt6-qtbase \
    qt6-qtwebengine \
    tzdata \
    && pip3 install --break-system-packages --no-cache-dir \
    scapy \
    requests \
    psutil \
    PyQt6 \
    PyQt6-WebEngine

WORKDIR /opt/l0p4map

RUN git clone https://github.com/HaxL0p4/L0p4Map.git . \
    && chmod +x L0p4Map.sh \
    && python3 -c "from core.scanner import scan_network; print('scanner OK')"

COPY run.sh /run.sh
COPY server.py /opt/l0p4map/server.py
COPY dashboard/ /opt/l0p4map/dashboard/
RUN chmod +x /run.sh && chmod +x /opt/l0p4map/server.py

LABEL \
    io.hass.version="1.0.0" \
    io.hass.type="addon" \
    io.hass.arch="amd64"

ENV DASHBOARD_PORT=8099
ENV L0P4MAP_INTERVAL=3600

ENTRYPOINT ["/run.sh"]
FROM debian:bookworm-slim

# Install system dependencies (Debian-based for PyQt6 compatibility)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    python3 \
    python3-pip \
    python3-pyqt6 \
    python3-pyqt6.qtwebengine \
    git \
    libpcap0.8 \
    libpcap0.8-dev \
    libgl1 \
    libegl1 \
    libxkbcommon0 \
    libdbus-1-3 \
    libfontconfig1 \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --break-system-packages \
    scapy \
    requests \
    psutil

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
    io.hass.type="app" \
    io.hass.arch="amd64"

ENV DASHBOARD_PORT=8099
ENV L0P4MAP_INTERVAL=3600

ENTRYPOINT ["/run.sh"]
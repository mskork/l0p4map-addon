FROM ghcr.io/home-assistant/amd64-addon-base:2025.01.0

# System deps: nmap, scapy (libpcap), PyQt6 libs
RUN apk add --no-cache \
    nmap \
    python3 \
    py3-pip \
    git \
    libpcap \
    qt6-qtbase \
    qt6-qtwebengine \
    && pip3 install --break-system-packages --no-cache-dir \
    scapy \
    requests \
    psutil \
    PyQt6 \
    PyQt6-WebEngine

WORKDIR /opt/l0p4map

# Clone L0p4Map source
RUN git clone https://github.com/HaxL0p4/L0p4Map.git . \
    && chmod +x L0p4Map.sh \
    && python3 -c "from core.scanner import scan_network; print('scanner OK')"

COPY run.sh /run.sh
RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
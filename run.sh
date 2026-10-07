#!/bin/bash
set -e

cd /opt/l0p4map

# Config from HA addon options
TARGET="${L0P4MAP_TARGET:-}"
INTERFACE="${L0P4MAP_INTERFACE:-}"
INTERVAL="${L0P4MAP_INTERVAL:-3600}"

# Qt headless mode (PyQt6 imports may happen even in CLI mode)
export QT_QPA_PLATFORM=offscreen
export QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox --disable-gpu --disable-software-rasterizer"
export QTWEBENGINE_DISABLE_SANDBOX=1

# Auto-detect target from local subnet if not set
if [ -z "$TARGET" ]; then
    TARGET=$(python3 -c "from core.scanner import get_local_subnet; print(get_local_subnet())" 2>/dev/null || echo "192.168.1.0/24")
    echo "Auto target: $TARGET"
fi

SCAN_ARGS="scan --target $TARGET --output json --file /data/scan_results.json"
if [ -n "$INTERFACE" ]; then
    SCAN_ARGS="$SCAN_ARGS --interface $INTERFACE"
fi

echo "L0p4Map addon starting — target: $TARGET, interval: ${INTERVAL}s"

while true; do
    echo "=== Scan started $(date) ==="
    python3 __main__.py $SCAN_ARGS 2>/tmp/l0p4map.err || {
        echo "Scan failed, see /tmp/l0p4map.err"
        cat /tmp/l0p4map.err
    }
    echo "=== Scan complete $(date) ==="
    sleep "$INTERVAL"
done
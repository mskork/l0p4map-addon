# L0p4Map HAOS Addon

Home Assistant OS addon wrapping L0p4Map network monitoring tool.

## Co robi

- Skanuje sieć (ARP + nmap) w wyznaczonym interwale
- Zapisuje wyniki jako JSON do `/data/scan_results.json`
- Home Assistant odczytuje plik przez `command_line` sensor

## Instalacja

1. Otwórz Hassio → Add-ons → ⋮ → Custom Repositories
2. URL: `https://github.com/mskork/l0p4map-addon` — kategoria: `addon`
3. Zainstaluj addon L0p4Map
4. Konfiguruj:
   - `target` — CIDR do skanowania (np. `192.168.1.0/24`), puste = auto
   - `interface` — interfejs sieciowy (puste = auto)
   - `interval` — sekundy między skanami (domyślnie 3600)

## Użycie w HA

### command_line sensor (configuration.yaml):
```yaml
sensor:
  - platform: command_line
    name: "L0p4Map Hosts"
    command: "cat /config/addon_configs/a0d7b954_l0p4map/data/scan_results.json"
    json_attributes_path: "$"
    value_template: "{{ value_json | length }} hosts"
```

### Automatyzacja — powiadomienie o nowych urządzeniach:
Porównuj bieżące wyniki z poprzednimi i wyślij Telegram, gdy pojawi się nowy MAC.

## Wymagania

- HAOS na amd64
- Uprawnienie NET_ADMIN (raw sockets dla scapy)
- Host networking (ARP broadcast)

## Ograniczenia

- Tylko amd64 (PyQt6 nie maARM wheels)
- Skan wymaga roota (addon ma privileged NET_ADMIN)
- PyQt6 na Alpine/musl — może wymagać aktualizacji base image
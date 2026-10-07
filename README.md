# L0p4Map Home Assistant Addon

Network monitoring & topology visualization for Home Assistant OS.

## Instalacja

Supervisor → Add-on Store → ⋮ → Custom Repositories:
- URL: `https://github.com/mskork/l0p4map-addon`
- Tip: `addon`

## Funkcje

- ARP discovery + nmap scan
- Interaktywna topologia sieci (vis.js)
- Wykrywanie roli urządzeń (gateway, router, switch, PC, mobile)
- Dashboard w sidebarze HA
- JSON API dla automatyzacji

## Konfiguracja

- `target` — sieć CIDR (np. `192.168.1.0/24`), puste = auto
- `interface` — interfejs sieciowy
- `interval` — sekundy między skanami (domyślnie 3600)
- `dashboard_port` — port dashboardu (domyślnie 8099)
# Fröling RS232 custom integration

This repository is structured as a Home Assistant custom integration so it can be installed through HACS or added as a custom repo.

## Required structure

```text
froelingRS232/
├── custom_components/
│   └── froeling_rs232/
│       ├── __init__.py
│       ├── manifest.json
│       └── sensor.py
├── configuration.yaml
├── README.md
├── repository.yaml
├── secrets.yaml.example
└── .gitignore
```

## Notes

- This is a skeleton integration structure.
- The actual Modbus register logic still needs to be implemented against the real Fröling device.
- The serial port must be configured to match your adapter and boiler settings.
- The repo is not intended to be a full production integration without device verification.

## HACS install

1. Push this repo to GitHub.
2. Make sure it is public or otherwise accessible to Home Assistant.
3. In HACS, add this repository as a custom repository.
4. Install the integration.
5. Configure the integration from Home Assistant.

## YAML example

```yaml
modbus:
  - name: froeling_s3200_serial
    type: serial
    port: /dev/serial/by-id/REPLACE_WITH_YOUR_USB_RS232_ADAPTER
    baudrate: 9600
    bytesize: 8
    method: rtu
    parity: E
    stopbits: 1
    timeout: 5
    message_wait_milliseconds: 30
```

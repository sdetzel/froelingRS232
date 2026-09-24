# Fröling S3200 over USB RS232

This folder contains a minimal, read-only Home Assistant Modbus configuration for a Fröling Lambdatronic S3200 connected to COM2 through an RS232-to-USB adapter.

## Hardware

The adapter must be RS232-capable. An RS485-only adapter is not suitable. Depending on the Fröling COM2 wiring, use the required null-modem/crossover cable. Do not connect or disconnect wiring while the controller is powered unless the Fröling documentation explicitly permits it.

## Controller settings

On the Lambdatronic, enable:

- `Use COM2 as MODBUS Interface`
- `Modbus Protokoll RTU = 1`
- `Use Modbus Protokoll 2014 = Yes`

Record the configured Modbus address. The example uses slave ID `2`; change every `slave: 2` entry if the controller uses another address. Protocol 2014 is especially important for later writes, although this starter configuration only reads values.

The example uses `9600 8E1`, which is a starting value only. Confirm baud rate, parity, data bits, and stop bits in the Fröling Modbus documentation for the installed controller firmware.

## Install

1. Make a full Home Assistant backup.
2. Copy the `modbus:` block from `configuration.yaml` into the Home Assistant `/config/configuration.yaml`, or use it as the basis of your existing file. Do not create a second top-level `modbus:` key.
3. Plug in the adapter and open Home Assistant's Terminal or SSH app.
4. Find the stable serial path:

   ```sh
   ha hardware info
   ```

   Look for the USB serial device. Prefer a path under `/dev/serial/by-id/`; otherwise use the detected `/dev/ttyUSB0` or `/dev/ttyACM0`.
5. Replace `REPLACE_WITH_YOUR_USB_RS232_ADAPTER` in the YAML with that path.
6. Change the slave ID if necessary.
7. Run **Settings -> Developer tools -> YAML -> Check configuration**.
8. Restart Home Assistant.

The initial entities are intentionally read-only. Check that the boiler and flue temperatures agree with the controller display before adding more registers or any write entities.

## Addressing

The Fröling register list uses addresses such as `30001` and `40001`. Home Assistant's Modbus integration uses zero-based offsets within each register family, so the starter mapping is:

| Fröling register | Home Assistant configuration |
| --- | --- |
| `30001` boiler temperature | `input_type: input`, `address: 0` |
| `30002` flue temperature | `input_type: input`, `address: 1` |
| `30004` residual oxygen | `input_type: input`, `address: 3` |
| `31001` outdoor temperature | `input_type: input`, `address: 1000` |

If the values are unavailable, verify the physical cable type, null-modem wiring, serial settings, slave ID, and COM2 settings before changing register addresses.

## Next step

Once the four readings are correct, expand the entity list from the register table matching the exact boiler model and firmware. Keep writable registers disabled until every read-only value has been checked against the controller.

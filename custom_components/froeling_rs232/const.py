"""Constants for the Fröling RS232 integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "froeling_rs232"
PLATFORMS: Final = ["sensor"]

SENSOR_DEFINITIONS: Final = [
    {
        "key": "boiler_temperature",
        "name": "Boiler temperature",
        "address": 0,
        "scale": 0.1,
        "unit": "°C",
        "device_class": "temperature",
    },
    {
        "key": "flue_temperature",
        "name": "Flue temperature",
        "address": 1,
        "scale": 0.1,
        "unit": "°C",
        "device_class": "temperature",
    },
    {
        "key": "residual_oxygen",
        "name": "Residual oxygen",
        "address": 3,
        "scale": 0.1,
        "unit": "%",
    },
    {
        "key": "outdoor_temperature",
        "name": "Outdoor temperature",
        "address": 1000,
        "scale": 0.1,
        "unit": "°C",
        "device_class": "temperature",
    },
]

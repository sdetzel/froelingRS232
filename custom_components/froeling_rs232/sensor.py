"""Sensors for the Fröling RS232 integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Fröling RS232 sensor platform from YAML."""
    add_entities([
        FroelingSensor("Boiler temperature", "boiler_temperature", UnitOfTemperature.CELSIUS),
        FroelingSensor("Flue temperature", "flue_temperature", UnitOfTemperature.CELSIUS),
        FroelingSensor("Outdoor temperature", "outdoor_temperature", UnitOfTemperature.CELSIUS),
    ])


class FroelingSensor(SensorEntity):
    """Representation of a Fröling Modbus sensor."""

    def __init__(self, name: str, key: str, unit: str) -> None:
        self._attr_name = name
        self._attr_unique_id = f"froeling_rs232_{key}"
        self._attr_native_unit_of_measurement = unit
        self._key = key

    @property
    def state(self):
        """Return the state of the entity."""
        return None

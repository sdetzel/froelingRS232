"""Sensors for the Fröling RS232 integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.exceptions import ModbusException

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SENSOR_DEFINITIONS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Fröling sensor platform from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = FroelingCoordinator(hass, data)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            FroelingSensor(
                coordinator,
                sensor_def["key"],
                sensor_def["name"],
                sensor_def["address"],
                sensor_def.get("scale", 1),
                sensor_def.get("unit", ""),
                sensor_def.get("device_class"),
            )
            for sensor_def in SENSOR_DEFINITIONS
        ]
    )


class FroelingCoordinator(DataUpdateCoordinator):
    """Coordinate polling for Fröling Modbus registers."""

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="froeling_rs232",
            update_interval=timedelta(seconds=30),
        )
        self.config = config

    async def _async_update_data(self):
        """Read the configured input registers from the Fröling controller."""
        port = self.config.get("port")
        if not port:
            raise UpdateFailed("No serial port configured")

        client = AsyncModbusSerialClient(
            port=port,
            baudrate=self.config.get("baudrate", 9600),
            bytesize=self.config.get("bytesize", 8),
            parity=self.config.get("parity", "E"),
            stopbits=self.config.get("stopbits", 1),
            timeout=self.config.get("timeout", 5),
            method="rtu",
        )

        try:
            await client.connect()
            values: dict[str, float] = {}
            slave = self.config.get("slave", 2)

            for sensor_def in SENSOR_DEFINITIONS:
                result = await client.read_input_registers(
                    address=sensor_def["address"],
                    count=1,
                    slave=slave,
                )
                if result.isError():
                    raise UpdateFailed(
                        f"Modbus read error for {sensor_def['name']}: {result}")
                raw_value = result.registers[0]
                values[sensor_def["key"]] = raw_value * sensor_def.get("scale", 1)

            return values
        except (ModbusException, OSError) as exc:
            raise UpdateFailed(f"Error communicating with Fröling device: {exc}") from exc
        finally:
            client.close()


class FroelingSensor(SensorEntity):
    """Representation of a Fröling Modbus sensor."""

    def __init__(
        self,
        coordinator: FroelingCoordinator,
        key: str,
        name: str,
        address: int,
        scale: float,
        unit: str,
        device_class: str | None,
    ) -> None:
        self.coordinator = coordinator
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"froeling_rs232_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._address = address
        self._scale = scale

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """Return the current sensor value."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self._key)
        if value is None:
            return None
        return value / self._scale if self._scale != 1 else value

    @property
    def should_poll(self) -> bool:
        return False

    async def async_update(self) -> None:
        """Update the sensor state from the coordinator."""
        await self.coordinator.async_request_refresh()

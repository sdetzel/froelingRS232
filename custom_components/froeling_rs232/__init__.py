"""The Fröling RS232 integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

DOMAIN = "froeling_rs232"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Fröling RS232 integration from YAML."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up Fröling RS232 from a config entry."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    """Unload a Fröling RS232 config entry."""
    return True

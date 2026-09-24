from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

DOMAIN = "froeling_rs232"

class FroelingRs232ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Fröling RS232",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("port", default="/dev/serial/by-id/REPLACE_WITH_YOUR_USB_RS232_ADAPTER"): str,
                    vol.Required("baudrate", default=9600): int,
                    vol.Required("slave", default=2): int,
                }
            ),
        )
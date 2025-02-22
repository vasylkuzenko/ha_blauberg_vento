import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Схема конфігурації для введення IP-адреси
CONFIG_SCHEMA = vol.Schema({
    vol.Required("host"): TextSelector(TextSelectorConfig(type="text"))
})

class BlaubergVentoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow для Blauberg Vento."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Обробка форми введення користувачем."""
        errors = {}

        if user_input is not None:
            host = user_input["host"]
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=f"Blauberg Vento ({host})", data=user_input)

        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA, errors=errors)

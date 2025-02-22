import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """init Blauberg Vento."""
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "fan"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """removing blauberg vento integration."""
    return await hass.config_entries.async_forward_entry_unload(entry, "fan")

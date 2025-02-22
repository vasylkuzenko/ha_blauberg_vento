import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Налаштування інтеграції Blauberg Vento."""
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "fan"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Видалення інтеграції."""
    return await hass.config_entries.async_forward_entry_unload(entry, "fan")

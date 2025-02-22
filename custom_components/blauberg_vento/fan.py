from homeassistant.components.fan import (
    DIRECTION_FORWARD, DIRECTION_REVERSE,
    FanEntity, FanEntityFeature
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
import socket
import math
import logging

_LOGGER = logging.getLogger(__name__)

SUPPORTED_MODE = (
    FanEntityFeature.SET_SPEED |
    FanEntityFeature.DIRECTION |
    FanEntityFeature.OSCILLATE |
    FanEntityFeature.PRESET_MODE |
    FanEntityFeature.TURN_ON |
    FanEntityFeature.TURN_OFF
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Налаштування вентилятора з конфігурації через UI."""
    host = entry.data.get("host")
    if host:
        async_add_entities([BlaubergFan(host)])

class BlaubergFan(FanEntity):
    def __init__(self, host):
        self._host = host
        self._port = 4000
        self._attr_unique_id = host
        self._attr_name = f"Blauberg Vento ({host})"
        self._state = False
        self._oscillating = True
        self._percentage = 21
        self._preset_mode = None
        self._direction = DIRECTION_FORWARD
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        self._attributes = {
            'current_humidity': 0,
            'need_clear_filter': False,
            'device_error': False
        }

    def speed_to_int(self, speed):
        if speed is None or speed == "0":
            return 0
        return int(math.floor(int(speed) / 100 * 255))

    def int_to_speed(self, speed):
        return math.floor(speed / 255 * 100)

    @property
    def is_on(self):
        return self._state

    @property
    def percentage(self) -> int:
        return self._percentage

    @property
    def supported_features(self) -> int:
        return SUPPORTED_MODE

    @property
    def speed_count(self) -> int:
        return 100

    @property
    def current_direction(self) -> str:
        return self._direction

    @property
    def oscillating(self):
        return self._oscillating

    @property
    def preset_modes(self):
        return ["reset_filter"]

    @property
    def preset_mode(self) -> str:
        return self._preset_mode

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update_status_from_response(self, res):
        self._state = res[7] == 1
        self._percentage = self.int_to_speed(res[21])
        self._preset_mode = None

        if res[23] == 0:
            self._direction = DIRECTION_FORWARD
            self._oscillating = False
        elif res[23] == 1:
            self._oscillating = True
        elif res[23] == 2:
            self._direction = DIRECTION_REVERSE
            self._oscillating = False

        self._attributes['current_humidity'] = res[25]
        self._attributes['need_clear_filter'] = res[31]
        self._attributes['device_error'] = bool(res[11])

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if preset_mode == "reset_filter":
            self.cs.sendto(bytearray([0x6D, 0x6F, 0x62, 0x69, 0x6C, 0x65, 30, 0x00, 0x0D, 0x0A]), (self._host, self._port))
            self.cs.settimeout(1.5)
            self.update_status_from_response(self.cs.recvfrom(1024)[0])

    async def async_turn_on(self, speed: str = None, percentage: int = None, preset_mode: str = None) -> None:

        self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x01, 0x01,    0x0d, 0x0a]), (self._host, self._port))
        self.cs.settimeout(1.5)
        self.update_status_from_response(self.cs.recvfrom(1024)[0])

    
        intSpeed = self.speed_to_int(speed)
       
        if self._state != True and intSpeed == 0: #power only
            self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x03, 0x00,        0x0d, 0x0a]), (self._host, self._port))
            self.cs.settimeout(1.5)
            self._state = True
           
        elif self._state != True and intSpeed != 0: #power and speed
            self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x03, 0x00,  0x05, intSpeed,       0x0d, 0x0a]), (self._host, self._port))
            self.cs.settimeout(1.5)
            self._state = True
            self._percentage = percentage

        elif intSpeed != 0: #only speed
            self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,    0x05, intSpeed,       0x0d, 0x0a]), (self._host, self._port))
            self.cs.settimeout(1.5)
            self._percentage = percentage
       
       

    async def async_turn_off(self) -> None:
  
        self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x01, 0x01,    0x0d, 0x0a]), (self._host, self._port))
        self.cs.settimeout(1.5)
        self.update_status_from_response(self.cs.recvfrom(1024)[0])
        
        if self._state != False:
            self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x03, 0x00,    0x0d, 0x0a]), (self._host, self._port))
            self.cs.settimeout(1.5)
            self._state = False
            # self.update_status_from_response(self.cs.recvfrom(1024)[0])

    async def async_set_percentage(self, percentage: int) -> None:
        self._percentage = percentage
        intSpeed = self.speed_to_int(percentage)
        self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,    0x05, intSpeed,    0x0d, 0x0a]), (self._host, self._port))
        self.cs.settimeout(1.5)



    async def async_set_direction(self, direction: str) -> None:

        if direction == DIRECTION_FORWARD:
            comand = 0
        elif direction == DIRECTION_REVERSE:
            comand = 2

        self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x06, comand,    0x0d, 0x0a]), (self._host, self._port))
        self.cs.settimeout(1.5)
        self.update_status_from_response(self.cs.recvfrom(1024)[0])
       
   

    async def async_oscillate(self, oscillating: bool) -> None:

        if oscillating != self._oscillating:

            if oscillating:
                comand = 1
            elif oscillating == False and self.direction == DIRECTION_FORWARD:
                comand = 0
            elif oscillating == False and self.direction == DIRECTION_REVERSE:
                comand = 2

            self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x06, comand,    0x0d, 0x0a]), (self._host, self._port))
            self.cs.settimeout(1.5)
            self.update_status_from_response(self.cs.recvfrom(1024)[0])
      


    async def async_update(self):
       
        self.cs.sendto(bytearray([0x6d, 0x6f, 0x62, 0x69, 0x6c, 0x65,     0x01, 0x01,    0x0d, 0x0a]), (self._host, self._port))
        self.cs.settimeout(1.5)
        self.update_status_from_response(self.cs.recvfrom(1024)[0])


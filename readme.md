[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)

# Blauberg Vento Home Assistant Integration

## Description
This integration allows you to control **Blauberg VENTO Expert A50-1 Pro** (old version) fans in Home Assistant. It supports turning the fan on/off, adjusting speed, changing rotation direction, oscillation and other functions. This integration is configurable via UI. 


## Features
- Turn the fan on/off
- Adjust speed (percentage-based)
- Set rotation direction (forward/reverse)
- Oscillation control
- Reset Filter Countdown

## Installation

The quickest way to install this integration is via [HACS][hacs-url] by clicking the button below:

[![Add to HACS via My Home Assistant][hacs-install-image]][hasc-install-url]

If it doesn't work, adding this repository to HACS manually by adding this URL:

1. Visit **HACS** → **Integrations** → **...** (in the top right) → **Custom repositories**
1. Click **Add**
1. Paste `https://github.com/vasylkuzenko/ha_blauberg_vento` into the **URL** field
1. Chose **Integration** as a **Category**
1. **Blauberg Vento** will appear in the list of available integrations. Install it normally.


### 2. Adding the Integration
1. Go to **Settings → Devices & Services**.
2. Click **Add Integration**.
3. Enter the **IP address** of the fan.
4. Save the changes.

## Usage
After setup, the fan will appear in the list of Home Assistant devices. You can control it via the UI or automation.

## UI Configuration
- **Turn On/Off**: Standard toggle button in the fan card.
- **Speed Control**: Slider to adjust speed from 0% to 100%.
- **Oscillation**: Separate toggle button.
- **Rotation Direction**: Can be changed via UI.

## License

MIT © [Vasyl Kuzenko][vasylkuzenko]


[vasylkuzenko]: https://github.com/vasylkuzenko
[hacs-url]: https://github.com/hacs/integration
[hasc-install-url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=vasylkuzenko&repository=ha_blauberg_vento&category=integration
[hacs-install-image]: https://my.home-assistant.io/badges/hacs_repository.svg
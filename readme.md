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
### 1. Copying Files
1. Download or clone the repository.
2. Copy the `blauberg_vento` folder into `custom_components/` of your Home Assistant installation.
3. Restart Home Assistant.

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
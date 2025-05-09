# EcoTracker Library by everHome

A Python library for reading energy consumption data from everHome's EcoTracker device via a local HTTP endpoint. This library is designed to work with EcoTracker devices that expose power and energy counter data via a JSON API.

## Installation

```bash
pip install ecotracker
```

## Usage

### Basic Usage

```python
from ecotracker import EcoTracker

# Initialize the EcoTracker device with the IP address of your device
meter = EcoTracker("192.168.1.100")

# Update the meter data
if meter.update():
    # Get the current power consumption
    power = meter.get_power()
    print(f"Current power consumption: {power} W")
    
    # Get the energy counter for incoming energy
    energy_in = meter.get_energy_counter_in()
    print(f"Energy counter in: {energy_in} kWh")
    
    # Get all available data
    all_data = meter.get_all_data()
    print(f"All data: {all_data}")
```

### Available Methods

The `EcoTracker` class provides the following methods:

- `update()`: Updates the electricity meter data from the HTTP endpoint
- `get_power()`: Gets the current power consumption in watts
- `get_power_phase1()`: Gets the current power consumption of phase 1 in watts
- `get_power_phase2()`: Gets the current power consumption of phase 2 in watts
- `get_power_phase3()`: Gets the current power consumption of phase 3 in watts
- `get_power_avg()`: Gets the average power consumption in watts
- `get_energy_counter_out()`: Gets the energy counter for outgoing energy in kWh
- `get_energy_counter_in()`: Gets the energy counter for incoming energy in kWh
- `get_energy_counter_in_t1()`: Gets the energy counter for incoming energy in tariff 1 in kWh
- `get_energy_counter_in_t2()`: Gets the energy counter for incoming energy in tariff 2 in kWh
- `get_all_data()`: Gets all electricity meter data as a dictionary

## Running Tests

```bash
python -m unittest discover tests
```

## License

MIT
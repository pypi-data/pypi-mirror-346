# electrical_power

electrical_power is an electrical package for power system,machines, and many more.

## Features

- Electrical cables calculations.
- AC asynch machine operations.

## Installation

You can install the package via **PyPI** or from **source**.

### Install from PyPI

```bash
pip install electrical_power
```

### Install from Source (GitHub)

```bash
git clone https://github.com/walied-alkady/electrical_power.git
cd electrical_power
pip install .
```

## Usage

After installation, you can use electrical_power .

### Example: Training and Making Predictions

```python
from electrical_power.electrical_cable import CableOperations

# Initialize new cable operations class
cable_operations = CableOperations()
# selct cable  
selected_new_cable = cable_operations.select_cable(
                            load_voltage= 400, 
                            load_current=30,
                            cable_run=100,
                            load_type='distribution_3ph',
                            installation_method='burried_direct',
                            cable_armour='sta',
                            installation_formation='flat',
                            ground_temperature=45
                            )
```

```

```

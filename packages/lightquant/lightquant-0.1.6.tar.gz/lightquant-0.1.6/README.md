# lightquant

lightquant is a lightweight Python library providing utilities for working with holidays, dates, options, and other trading-related tools. It is designed to simplify common tasks in quantitative finance and trading workflows.

---

## Features

- **Date Utilities**: Simplify date and time operations.
- **Options Pricing**: Tools for European options calculations.
- **Trading Interactions**: functions for assisting web scraping, reading and writing R files
- **Commission Calculations**: Retrieve and calculate trading commissions based on dates and configurations.
- **Config Management**: Centralized configuration management using YAML files.

---

## Installation

Install the package using pip:

```bash
pip install lightquant
```

---

## Usage

### Import the Library
```python
import lightquant
```

### Check the Version
```python
print(lightquant.__version__)
```

### Initialize Configuration
```python
from lightquant import initialize_config, get_config

# Initialize configuration with the default config path
initialize_config("path/to/config.yaml")

# Access configuration values
config = get_config()
timezone = config.get("tz")
print(f"Timezone: {timezone}")
```

### Logging Configuration
```python
from lightquant import configure_logging

# Configure logging
configure_logging(level=logging.INFO, enable_console=True)
```

## License

This project is licensed under the terms of the [MIT License](LICENSE).

---


## Links

- **Homepage**: [GitHub Repository](https://github.com/yourusername/lightquant)
- **PyPI**: [LightQuant on PyPI](https://pypi.org/project/lightquant/)
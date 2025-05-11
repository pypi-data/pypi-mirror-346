# lazy-b

Keep Slack, Microsoft Teams, or other similar applications from showing you as "away" or "inactive" by simulating key presses at regular intervals.

## Installation

Install directly from PyPI using pip or uv:

```bash
# Using pip
pip install lazy-b

# Using uv
uv pip install lazy-b
```

## Usage

### Command Line

Run `lazy-b` from the command line:

```bash
# Basic usage (will press Shift key every 60 seconds)
lazy-b

# Customize the interval (e.g., every 30 seconds)
lazy-b --interval 30

# Run in quiet mode (no console output)
lazy-b --quiet
```

Press `Ctrl+C` to stop.

### Python API

You can also use the Python API directly in your own scripts:

```python
from lazy_b import LazyB
import time

# Create an instance with a custom interval (in seconds)
lazy = LazyB(interval=45)

# Define a callback function to handle status messages (optional)
def status_callback(message):
    print(f"Status: {message}")

# Start the simulation
lazy.start(callback=status_callback)

try:
    # Keep your script running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop on Ctrl+C
    lazy.stop()
```

## Features

- Prevents "away" or "inactive" status in messaging applications
- Customizable interval between key presses
- Simple command-line interface
- Python API for integration into your own scripts
- Minimal resource usage

## Requirements

- Python 3.8 or higher
- PyAutoGUI

## License

MIT

## Disclaimer

This tool is meant for legitimate use cases like preventing timeouts during presentations or when you're actively reading but not typing. Please use responsibly and in accordance with your organization's policies.

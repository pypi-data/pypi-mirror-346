# Introduction

wavetool is a Python package providing modules and examples to interface with [Coherent optical instruments](https://www.coherent.com/networking/optical-instrumentation). 

# Supported models

WaveAnalyzer: 1500S, 200A, 400A, 1500B.

WaveShaper: to be implemented.

WaveMaker: to be implemented.

# Installation

This package is currently in beta testing.

To install from PyPi: ```pip install wavetools```
To install with GUI example: ```pip install wavetools[gui]```

Tests build package is also available on TestPyPi: ```pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple wavetools```

To install GUI: ```pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple wavetools[gui]```

(Planned) ```pip install wavetools```

# Module organization

The package is organized into submodules based on the instrument type:

*   **`wavetools.WaveAnalyzers`**: Contains the `WaveAnalyzers.py` file, which includes the base `WaveAnalyzer` class, specific implementations (`WaveAnalyzer1500S`, `WaveAnalyzer400A`, `WaveAnalyzer1500B`), and data models (`WAScan`, `WAScanInfo`) for interacting with WaveAnalyzer devices.
    *   `examples/`: Contains example scripts, including a GUI application (`wa_gui.py`) demonstrating how to use the `WaveAnalyzers` module.
    *   `tests/`: Contains unit and integration tests (`test_waveanalyzer_api_device_in_loop.py`) for the `WaveAnalyzers` module.
*   `wavetools.WaveShapers` (Planned): Will contain classes for WaveShaper devices.
    *   `examples/` (Planned): Will contain example scripts for `WaveShapers`.
    *   `tests/` (Planned): Will contain tests for `WaveShapers`.
*   `wavetools.WaveMakers` (Planned): Will contain classes for WaveMaker devices.
    *   `examples/` (Planned): Will contain example scripts for `WaveMakers`.
    *   `tests/` (Planned): Will contain tests for `WaveMakers`.

# Example code

## WaveAnalyzer
```
from wavetools import WaveAnalyzer, create_waveanalyzer

wa = create_waveanalyzer("wa000683.local", preset=True)
wa.set_scan(center=193700000, span="full") # optional if preset is used
print(wa.scan_info)
trace = wa.measure()
print(trace.frequency_THz)
print(trace.power_dBm)

```

# Running example GUI

[gui] must selected during pip installation for running example GUI scripts. 

WaveAnalyzer GUI: ```python -m wavetools.WaveAnalyzers.examples.wa_gui```

# Required Python version

python>=3.8



# Dependencies

## Mandatory

* numpy
* pydantic
* httpx

## GUI examples

* PyQt5
* PyQtGraph
* scipy
  
##  Licensing

This project is released under the MIT License.





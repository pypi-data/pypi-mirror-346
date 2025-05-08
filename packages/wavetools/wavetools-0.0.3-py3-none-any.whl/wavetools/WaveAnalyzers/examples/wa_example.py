"""
Example of using the WaveAnalyzer class to measure a trace
"""

from wavetools import WaveAnalyzer, create_waveanalyzer

wa = create_waveanalyzer("wa000683.local", preset=True)
wa.set_scan(center=193700000, span="full") # optional if preset is used
print(wa.scan_info)
trace = wa.measure()
print(trace.frequency_THz)
print(trace.power_dBm)
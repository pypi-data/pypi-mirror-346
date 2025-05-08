import pytest
import os, sys
import numpy as np
import time # Import time for sleep
from typing import Optional # Import Optional for type hinting
# Adjust path to import from the parent directory of 'tests'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import the updated API classes and models from WaveAnalyzers module
from WaveAnalyzers import create_waveanalyzer, WaveAnalyzer, WaveAnalyzer1500S, WaveAnalyzer200A, WaveAnalyzer400A, WaveAnalyzer1500B, WAScanInfo, WAScan

# Device addresses for integration testing.
WA_1500S_IP = "wa000186.local"
WA_200A_IP = "169.254.4.4" # Replace with actual 200A IP address if available
WA_400A_IP = "wa000683.local"
WA_1500B_IP = "wave_dev7.local"

pytestmark = pytest.mark.integration  # Mark all tests as integration tests.

# --- Fixtures ---
@pytest.fixture(scope="module")
def wa_1500s_api() -> WaveAnalyzer1500S:
    try:
        api = create_waveanalyzer(WA_1500S_IP)
        if not isinstance(api, WaveAnalyzer1500S):
             pytest.fail(f"Expected WaveAnalyzer1500S for {WA_1500S_IP}, but got {type(api)}")
        return api
    except Exception as e:
        pytest.fail(f"Failed to initialize WaveAnalyzer1500S({WA_1500S_IP}): {e}")

@pytest.fixture(scope="module")
def wa_200a_api() -> WaveAnalyzer200A:
    try:
        api = create_waveanalyzer(WA_200A_IP)
        if not isinstance(api, WaveAnalyzer200A):
             pytest.fail(f"Expected WaveAnalyzer200A for {WA_200A_IP}, but got {type(api)}")
        return api
    except Exception as e:
        # Use skip instead of fail if the device might not be present
        pytest.skip(f"Skipping 200A tests. Failed to initialize WaveAnalyzer200A({WA_200A_IP}): {e}")

@pytest.fixture(scope="module")
def wa_400a_api() -> WaveAnalyzer400A:
    try:
        api = create_waveanalyzer(WA_400A_IP)
        if not isinstance(api, WaveAnalyzer400A):
             pytest.fail(f"Expected WaveAnalyzer400A for {WA_400A_IP}, but got {type(api)}")
        return api
    except Exception as e:
        pytest.fail(f"Failed to initialize WaveAnalyzer400A({WA_400A_IP}): {e}")

@pytest.fixture(scope="module")
def wa_1500b_api() -> WaveAnalyzer1500B:
    try:
        api = create_waveanalyzer(WA_1500B_IP)
        if not isinstance(api, WaveAnalyzer1500B):
             pytest.fail(f"Expected WaveAnalyzer1500B for {WA_1500B_IP}, but got {type(api)}")
        return api
    except Exception as e:
        pytest.fail(f"Failed to initialize WaveAnalyzer1500B({WA_1500B_IP}): {e}")

# --- Helper ---
def _check_wascan_structure(scan: WAScan, expected_rbw: Optional[float] = None, check_pol: bool = True):
    """Helper function to validate WAScan structure and properties."""
    assert isinstance(scan, WAScan)
    assert hasattr(scan, 'scanid')
    assert scan.scanid >= 0 # Scan ID can be 0 initially or after query
    assert scan.is_valid is True
    assert scan.power_unit == "mW"
    if expected_rbw is not None:
        assert scan.rbw == expected_rbw
    else:
        assert scan.rbw > 0 # RBW should be positive

    required_fields = ["Frequency", "Absolute Power", "Power X-Polarization", "Power Y-Polarization", "Flag"]
    assert scan.data.size > 0, "Measured data array is empty"
    assert list(scan.data.dtype.names) == required_fields, f"Data fields mismatch. Expected {required_fields}, got {list(scan.data.dtype.names)}"

    # Test properties
    assert isinstance(scan.frequency_THz, np.ndarray) and scan.frequency_THz.size == scan.data.size
    assert isinstance(scan.power_mW, np.ndarray) and scan.power_mW.size == scan.data.size
    assert isinstance(scan.power_dBm, np.ndarray) and scan.power_dBm.size == scan.data.size
    if check_pol:
        # Allow for cases where polarization data might be all zeros if disabled on device
        assert isinstance(scan.power_x_pol_mW, np.ndarray) and scan.power_x_pol_mW.size == scan.data.size
        assert isinstance(scan.power_x_pol_dBm, np.ndarray) and scan.power_x_pol_dBm.size == scan.data.size
        assert isinstance(scan.power_y_pol_mW, np.ndarray) and scan.power_y_pol_mW.size == scan.data.size
        assert isinstance(scan.power_y_pol_dBm, np.ndarray) and scan.power_y_pol_dBm.size == scan.data.size
    assert isinstance(scan.flags, np.ndarray) and scan.flags.size == scan.data.size
    assert isinstance(scan.metadata, dict)

# --- 1500S Tests ---
def test_waveanalyzer_1500s_get_device_info(wa_1500s_api):
    assert wa_1500s_api.model == "1500S"
    assert wa_1500s_api.serial_number is not None and wa_1500s_api.serial_number != ""
    assert wa_1500s_api.version is not None and wa_1500s_api.version != ""
    assert wa_1500s_api.vendor is not None and wa_1500s_api.vendor != ""
    print("\nWaveAnalyzer1500S device info:")
    print(f"  Model: {wa_1500s_api.model}")
    print(f"  Serial Number: {wa_1500s_api.serial_number}")
    print(f"  Version: {wa_1500s_api.version}")
    print(f"  Vendor: {wa_1500s_api.vendor}")

def test_waveanalyzer_1500s_set_scan(wa_1500s_api):
    scan_mode_key = "HighSens" # Use a valid key from the 1500S scanmodes dict
    available_modes = wa_1500s_api.get_scan_modes()
    assert scan_mode_key in available_modes, f"Scan mode '{scan_mode_key}' not found in {available_modes}"
    success = wa_1500s_api.set_scan(center=193700000, span="full", scan_mode=scan_mode_key)
    assert success is True, f"set_scan returned False or an unexpected value"

def test_waveanalyzer_1500s_get_scan_info(wa_1500s_api):
    # Ensure set_scan runs first if needed
    # wa_1500s_api.set_scan(center=193700000, span="full", scan_mode="HighSens")
    info = wa_1500s_api.scan_info # Access as property
    assert isinstance(info, WAScanInfo)
    assert info.port is not None and info.port != ""
    print("\n1500S Scan info:", info.model_dump())

def test_waveanalyzer_1500s_measure(wa_1500s_api):
    # --- Test with force_new=True ---
    print("\nTesting 1500S measure(force_new=True)...")
    scan_new = wa_1500s_api.measure(force_new=True)
    _check_wascan_structure(scan_new, expected_rbw=150)
    assert scan_new.scanid > 0 # Should get a new scan ID > 0
    print(f"  Scan ID (force_new=True): {scan_new.scanid}")
    print(f"  Data points: {scan_new.data.size}")
    print(f"  RBW: {scan_new.rbw}") # Print RBW from WAScan object

    # --- Test with force_new=False ---
    time.sleep(0.1)
    print("\nTesting 1500S measure(force_new=False)...")
    scan_cached = wa_1500s_api.measure(force_new=False)
    _check_wascan_structure(scan_cached, expected_rbw=150)
    assert scan_cached.scanid >= scan_new.scanid # Can be same or newer
    print(f"  Scan ID (force_new=False): {scan_cached.scanid}")
    print(f"  Data points: {scan_cached.data.size}")
    print(f"  RBW: {scan_cached.rbw}") # Print RBW from WAScan object

# --- 200A Tests ---
def test_waveanalyzer_200a_get_device_info(wa_200a_api):
    assert wa_200a_api.model == "WA200A"
    assert hasattr(wa_200a_api, "firmware_version")
    assert wa_200a_api.firmware_version is not None and wa_200a_api.firmware_version != "" and wa_200a_api.firmware_version != "N/A"
    assert hasattr(wa_200a_api, "pno")
    assert wa_200a_api.pno is not None and wa_200a_api.pno != "" and wa_200a_api.pno != "N/A"
    assert isinstance(wa_200a_api.info_valid, bool)
    assert wa_200a_api.serial_number is not None # May be N/A

    print("\nWaveAnalyzer200A device info:")
    print(f"  Model: {wa_200a_api.model}")
    print(f"  Serial Number: {wa_200a_api.serial_number}")
    print(f"  Firmware Version: {wa_200a_api.firmware_version}")
    print(f"  Pno: {wa_200a_api.pno}")
    print(f"  Info Valid: {wa_200a_api.info_valid}")

def test_waveanalyzer_200a_get_scan_modes(wa_200a_api):
    modes = wa_200a_api.get_scan_modes()
    assert modes == ["Normal"]
    print("\nWaveAnalyzer200A scan modes:", modes)

def test_waveanalyzer_200a_set_scan(wa_200a_api):
    # Test valid calls (should just return True without error)
    assert wa_200a_api.set_scan() is True
    assert wa_200a_api.set_scan(span="full") is True
    assert wa_200a_api.set_scan(span=-1) is True
    assert wa_200a_api.set_scan(scan_mode="Normal") is True
    assert wa_200a_api.set_scan(span="full", scan_mode="Normal") is True

    # Test invalid scan mode
    with pytest.raises(ValueError, match="WaveAnalyzer200A only supports 'Normal' mode"):
        wa_200a_api.set_scan(scan_mode="HighRes")

    # Test invalid span
    with pytest.raises(ValueError, match="WaveAnalyzer200A only supports full scans"):
        wa_200a_api.set_scan(span=1000) # Any span other than 'full' or -1

    # Test invalid center (though ignored, check if base validation catches it - depends on implementation)
    # with pytest.raises(ValidationError): # Or potentially no error if ignored early
    #     wa_200a_api.set_scan(center="invalid")

    print("\nWaveAnalyzer200A set_scan tests passed.")

def test_waveanalyzer_200a_measure(wa_200a_api):
    # --- Test with force_new=True ---
    print("\nTesting 200A measure(force_new=True)...")
    scan_new = wa_200a_api.measure(force_new=True)
    # RBW varies, check_pol depends on device setting, so don't pass expected_rbw
    _check_wascan_structure(scan_new)
    assert "noise_power" in scan_new.metadata
    assert "polarization" in scan_new.metadata
    assert "timestamp" in scan_new.metadata

    print(f"  Scan ID (force_new=True): {scan_new.scanid}")
    print(f"  Data points: {scan_new.data.size}")
    print(f"  RBW: {scan_new.rbw}") # Print RBW from WAScan object
    print(f"  Metadata includes noise power: {scan_new.metadata.get('noise_power')}")
    print(f"  Metadata includes polarization flag: {scan_new.metadata.get('polarization')}")

    # --- Test with force_new=False ---
    time.sleep(0.1)
    print("\nTesting 200A measure(force_new=False)...")
    scan_cached = wa_200a_api.measure(force_new=False)
    _check_wascan_structure(scan_cached) # RBW varies
    assert scan_cached.scanid >= scan_new.scanid # Can be same or newer
    assert "noise_power" in scan_cached.metadata

    print(f"  Scan ID (force_new=False): {scan_cached.scanid}")
    print(f"  Data points: {scan_cached.data.size}")
    print(f"  RBW: {scan_cached.rbw}") # Print RBW from WAScan object
    print(f"  Metadata includes noise power: {scan_cached.metadata.get('noise_power')}")

# --- 400A Tests ---
def test_waveanalyzer_400a_get_device_info(wa_400a_api):
    assert wa_400a_api.model == "WA400A"
    assert hasattr(wa_400a_api, "firmware_version")
    assert wa_400a_api.firmware_version is not None and wa_400a_api.firmware_version != "" and wa_400a_api.firmware_version != "N/A"
    assert hasattr(wa_400a_api, "pno")
    assert wa_400a_api.pno is not None and wa_400a_api.pno != "" and wa_400a_api.pno != "N/A"
    assert isinstance(wa_400a_api.info_valid, bool)
    assert wa_400a_api.serial_number is not None # May be N/A

    print("\nWaveAnalyzer400A device info:")
    print(f"  Model: {wa_400a_api.model}")
    print(f"  Serial Number: {wa_400a_api.serial_number}")
    print(f"  Firmware Version: {wa_400a_api.firmware_version}")
    print(f"  Pno: {wa_400a_api.pno}")
    print(f"  Info Valid: {wa_400a_api.info_valid}")

def test_waveanalyzer_400a_set_scan(wa_400a_api):
    scan_mode_key = "HighRes" # Use a valid key from the 400A scanmodes dict
    available_modes = wa_400a_api.get_scan_modes()
    assert scan_mode_key in available_modes, f"Scan mode '{scan_mode_key}' not found in {available_modes}"
    success = wa_400a_api.set_scan(center=193700000, span="full", scan_mode=scan_mode_key)
    assert success is True, f"set_scan returned False or an unexpected value"

# No get_scan_info test for 400A as it uses the base property which might not reflect the new API state accurately after set_scan

def test_waveanalyzer_400a_measure(wa_400a_api):
    # --- Test with force_new=True ---
    print("\nTesting 400A measure(force_new=True)...")
    scan_new = wa_400a_api.measure(force_new=True)
    # RBW varies, check_pol depends on device setting, so don't pass expected_rbw
    _check_wascan_structure(scan_new)
    assert "noise_power" in scan_new.metadata
    assert "polarization" in scan_new.metadata
    assert "timestamp" in scan_new.metadata

    print(f"  Scan ID (force_new=True): {scan_new.scanid}")
    print(f"  Data points: {scan_new.data.size}")
    print(f"  RBW: {scan_new.rbw}") # Print RBW from WAScan object
    print(f"  Metadata includes noise power: {scan_new.metadata.get('noise_power')}")
    print(f"  Metadata includes polarization flag: {scan_new.metadata.get('polarization')}")

    # --- Test with force_new=False ---
    time.sleep(0.1)
    print("\nTesting 400A measure(force_new=False)...")
    scan_cached = wa_400a_api.measure(force_new=False)
    _check_wascan_structure(scan_cached) # RBW varies
    assert scan_cached.scanid >= scan_new.scanid # Can be same or newer
    assert "noise_power" in scan_cached.metadata

    print(f"  Scan ID (force_new=False): {scan_cached.scanid}")
    print(f"  Data points: {scan_cached.data.size}")
    print(f"  RBW: {scan_cached.rbw}") # Print RBW from WAScan object
    print(f"  Metadata includes noise power: {scan_cached.metadata.get('noise_power')}")

# --- 1500B Tests ---
def test_waveanalyzer_1500b_get_device_info(wa_1500b_api):
    assert wa_1500b_api.model == "1500B"
    assert hasattr(wa_1500b_api, "firmware_version")
    assert wa_1500b_api.firmware_version is not None and wa_1500b_api.firmware_version != "" and wa_1500b_api.firmware_version != "N/A"
    assert hasattr(wa_1500b_api, "pno")
    assert wa_1500b_api.pno is not None and wa_1500b_api.pno != "" and wa_1500b_api.pno != "N/A"
    assert isinstance(wa_1500b_api.info_valid, bool)
    assert wa_1500b_api.serial_number is not None # May be N/A

    print("\nWaveAnalyzer1500B device info:")
    print(f"  Model: {wa_1500b_api.model}")
    print(f"  Serial Number: {wa_1500b_api.serial_number}")
    print(f"  Firmware Version: {wa_1500b_api.firmware_version}")
    print(f"  Pno: {wa_1500b_api.pno}")
    print(f"  Info Valid: {wa_1500b_api.info_valid}")

def test_waveanalyzer_1500b_set_scan(wa_1500b_api):
    # Note: 1500B _validate_scan_mode currently returns input, so any string works,
    # but we use a key from its scanmodes dict for consistency.
    scan_mode_key = "Normal"
    available_modes = wa_1500b_api.get_scan_modes()
    success = wa_1500b_api.set_scan(center=193700000, span="full", scan_mode=scan_mode_key)
    assert success is True, f"set_scan returned False or an unexpected value"

# No get_scan_info test for 1500B (same reason as 400A)

def test_waveanalyzer_1500b_measure(wa_1500b_api):
    # --- Test with force_new=True ---
    print("\nTesting 1500B measure(force_new=True)...")
    scan_new = wa_1500b_api.measure(force_new=True)
    _check_wascan_structure(scan_new) # RBW varies
    assert "noise_power" in scan_new.metadata
    assert "polarization" in scan_new.metadata
    assert "timestamp" in scan_new.metadata

    print(f"  Scan ID (force_new=True): {scan_new.scanid}")
    print(f"  Data points: {scan_new.data.size}")
    print(f"  RBW: {scan_new.rbw}") # Print RBW from WAScan object
    print(f"  Metadata includes noise power: {scan_new.metadata.get('noise_power')}")
    print(f"  Metadata includes polarization flag: {scan_new.metadata.get('polarization')}")

    # --- Test with force_new=False ---
    time.sleep(0.1)
    print("\nTesting 1500B measure(force_new=False)...")
    scan_cached = wa_1500b_api.measure(force_new=False)
    _check_wascan_structure(scan_cached) # RBW varies
    assert scan_cached.scanid >= scan_new.scanid # Can be same or newer
    assert "noise_power" in scan_cached.metadata

    print(f"  Scan ID (force_new=False): {scan_cached.scanid}")
    print(f"  Data points: {scan_cached.data.size}")
    print(f"  RBW: {scan_cached.rbw}") # Print RBW from WAScan object
    print(f"  Metadata includes noise power: {scan_cached.metadata.get('noise_power')}")

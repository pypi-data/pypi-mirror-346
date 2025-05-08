import os
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from WaveShaperAPIs import WaveShaperProfile, WaveShaperAPI

DEVICE_ADDR = "ws201558.local"
TEST_WSP_FILE = os.path.join(os.path.dirname(__file__), "test.wsp")

@pytest.fixture(scope="module")
def ws_api():
    # Initialize the WaveShaperAPI using the real device.
    return WaveShaperAPI(DEVICE_ADDR)

def test_get_profile(ws_api):
    # Ensure that get_profile returns a WaveShaperProfile with non-empty data.
    profile = ws_api.get_profile()
    assert isinstance(profile, WaveShaperProfile)
    assert profile.data.size > 0

def test_load_parametric_profile(ws_api):
    # Use a valid filter type and parameters.
    # This should load a new profile on the device and return True on success.
    result = ws_api.load_parametric_profile("bandpass", 2, 193, 1, 4)
    assert result is True

def test_blockall(ws_api):
    # Block all channels on a given port and expect True.
    result = ws_api.blockall(2)
    assert result is True

def test_transmit(ws_api):
    # Return port 2 to transmit mode and expect True.
    result = ws_api.transmit(2)
    assert result is True

def test_upload_wsp(ws_api):
    # Ensure the test WSP file exists.
    assert os.path.exists(TEST_WSP_FILE), f"test.wsp not found at {TEST_WSP_FILE}"
    # Upload the WSP file and expect True upon success.
    result = ws_api.upload_wsp(TEST_WSP_FILE)
    assert result is True
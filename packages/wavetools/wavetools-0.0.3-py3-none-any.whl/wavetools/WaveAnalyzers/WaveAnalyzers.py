import httpx
import numpy as np
from typing import Optional, Any, Union, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, validate_call, ValidationError
import json
import string
from abc import ABC, abstractmethod

class WAScanInfo(BaseModel):
    """
    Scan metadata reported by WaveAnalyzer.
    """
    scanid: int
    center: int
    span: int
    startfreq: int
    stopfreq: int
    port: str

class WAScan(BaseModel):
    """
    WaveAnalyzer scan data class.
    """
    scanid: int  # scan is invalid if scanid <= 0
    is_valid: bool 
    power_unit: str = "mW"
    frequency_unit: str = "MHz"
    rbw : float
    data: np.ndarray = Field(default_factory=lambda: np.array([])) 
    metadata: dict = Field(default_factory=dict)  # Optional metadata field
    # "Frequency", "Absolute Power", "Power X-Polarization", "Power Y-Polarization", "Flag"
    model_config = ConfigDict(arbitrary_types_allowed = True)

    @field_validator('data', mode='before') # 'before' corresponds to pre=True
    @classmethod
    def check_data_structure(cls, v):
        """
        Validate the structure of the data field.

        Args:
            v: The value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If the value is not a numpy array or has an incorrect dtype.
        """
        if not isinstance(v, np.ndarray):
             raise ValueError("data must be a numpy array")
        if v.dtype != np.dtype([("Frequency", np.int32), ("Absolute Power", np.float32), ("Power X-Polarization", np.float32), ("Power Y-Polarization", np.float32), ("Flag", np.int32)]):
            raise ValueError(f"data must have dtype {np.dtype([('Frequency', np.int32), ('Absolute Power', np.float32), ('Power X-Polarization', np.float32), ('Power Y-Polarization', np.float32), ('Flag', np.int32)])}, but got {v.dtype}")
        return v
    
    @field_validator('metadata', mode='before')
    @classmethod
    def check_metadata_structure(cls, v):
        """
        Validate the structure of the metadata field.

        Args:
            v: The value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If the value is not a dictionary.
        """
        if not isinstance(v, dict):
             raise ValueError("metadata must be a dictionary")
        return v
    
    @property
    def frequency_THz(self) -> np.ndarray:
        """
        Convert frequency from MHz to THz.

        Returns:
            np.ndarray: Frequency in THz.
        """
        return self.data["Frequency"] * 1e-6
    
    @property
    def power_dBm(self) -> np.ndarray:
        """
        Convert power from mW to dBm.

        Returns:
            np.ndarray: Power in dBm.
        """
        return 10 * np.log10(self.data["Absolute Power"])
    
    @property
    def power_mW(self) -> np.ndarray:
        """
        Return power in mW.

        Returns:
            np.ndarray: Power in mW.
        """
        return self.data["Absolute Power"]
    
    @property
    def power_x_pol_dBm(self) -> np.ndarray:
        """
        Convert power from mW to dBm for X-Polarization.

        Returns:
            np.ndarray: Power in dBm for X-Polarization.
        """
        return 10 * np.log10(self.data["Power X-Polarization"])
    
    @property
    def power_x_pol_mW(self) -> np.ndarray:
        """
        Return power in mW for X-Polarization.

        Returns:
            np.ndarray: Power in mW for X-Polarization.
        """
        return self.data["Power X-Polarization"]
    
    @property
    def power_y_pol_dBm(self) -> np.ndarray:    
        """
        Convert power from mW to dBm for Y-Polarization.

        Returns:
            np.ndarray: Power in dBm for Y-Polarization.
        """
        return 10 * np.log10(self.data["Power Y-Polarization"])
    
    @property
    def power_y_pol_mW(self) -> np.ndarray:
        """
        Return power in mW for Y-Polarization.

        Returns:
            np.ndarray: Power in mW for Y-Polarization.
        """
        return self.data["Power Y-Polarization"]
    
    @property
    def flags(self) -> np.ndarray:
        """
        Return flags as a numpy array.

        Returns:
            np.ndarray: Flags.
        """
        return self.data["Flag"]
    
class WaveAnalyzer(ABC):
    """
    WaveAnalyzer base class. This is an abstract class which should not be instantiated directly. Use create_waveanalyzer() factory function to create device-specific instances.
    This class defines the common interface for all WaveAnalyzer devices.
    It provides methods for connecting to the device, configuring scans, and retrieving scan data.

    """
    _default_center: int = 193700000

    @classmethod
    @validate_call
    def get_model(cls, address : str) -> str:
        """
        Get the model name of the WaveAnalyzer device at the given address.

        Args:
            address (str): The network address of the device.

        Returns:
            str: The model name of the device (e.g., "1500S", "WA400A").
        
        Raises:
            httpx.RequestError: If the HTTP request fails.
            json.JSONDecodeError: If the response is not valid JSON.
            KeyError: If the 'model' key is missing in the response.
        """
        response = httpx.get(f"http://{address}/wanl/info", timeout=10)
        response.raise_for_status()
        model = response.json()['model']
        return model
    
    @abstractmethod
    @validate_call
    def __init__(self, address: str, preset: bool = True):
        """ 
        Connect to WaveAnalyzer device.
        
        Args:
            address (str): Device network address (e.g., "wa000186.local").
            preset (bool): If True, the device is set default scan profile. 
        """
        self.base_url = f"http://{address}/wanl"
        infoJson = self.__get_device_info()
        self.model = infoJson['model']
        self.serial_number = infoJson['sno']
        self.version = infoJson['version']
        self.vendor = infoJson['vendo']

    @validate_call
    @abstractmethod
    def get_scan_modes(self) -> list[str]:
        """
        Get the list of available scan modes.
        Returns:
            list[str]: List of available scan modes. "Normal" is guranteed to be supported by all models
        """
        pass

    @validate_call
    @abstractmethod
    def _validate_scan_mode(self, scan_mode: str) -> str:
        """
        Validate the scan mode identifier for the specific device model.
        
        This method should be implemented by subclasses to check if the provided
        scan_mode string is valid for that model and potentially return an 
        internal representation if needed.

        Args:
            scan_mode (str): The scan mode identifier to validate (e.g., "HighRes").

        Returns:
            str: The validated scan mode identifier, possibly transformed for internal use.
        
        Raises:
            ValueError: If the scan mode is not recognized by the specific model.
        """
        pass
    
    @validate_call
    def set_scan(self, center: int = _default_center, span: Union[int, Literal["full"]] = "full", scan_mode: Optional[str] = None) -> bool:
        """
        Configure the device to perform a scan.

        Args:
            center (int): Center frequency in MHz.
            span (Union[int, "full"]): Span in MHz or "full".
            scan_mode (str, optional): Optional scan mode identifier (e.g., "Normal"). This method may raise an error (model-specific) if the scan mode is not recognized. The scan modes are model-specific, but "Normal" is guaranteed to work.

        Returns:
            bool: True if the scan was successfully configured, False otherwise.
        """
        if span == "full":
            span = -1
        url = f"{self.base_url}/scan/{center}/{span}"
        if scan_mode:
            tag = self._validate_scan_mode(scan_mode)
            url += f"/{tag}"
        # Send a PUT request to the device
        try:    
            response = httpx.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            response_json = response.json()
            if response_json.get("rc") != 0:
                return False
            return True
        except httpx.RequestError as exc:
            raise ConnectionError(f"HTTP request failed: {exc}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON response: {e}")
        except KeyError as e:
            raise ValueError(f"Unexpected response format: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}") 

    @property
    @validate_call
    def scan_info(self) -> WAScanInfo:
        """
        Get information about the current scan.

        Returns:
            WAScanInfo: Information about the current scan.
        """
        url = f"{self.base_url}/scan/info"
        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
            return WAScanInfo(**response.json()) 
        except httpx.RequestError as exc:
            raise ConnectionError(f"HTTP request failed: {exc}")
        except ValidationError as e:
             raise ValueError(f"Failed to validate scan info response: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to get or parse scan info: {e}")

    @abstractmethod
    @validate_call
    def measure(self, force_new: bool = False) -> WAScan:
        """
        Fetch measurement data from the device.

        Args:
            force_new (bool): If True, the returned measurement is guaranteed 
                              to be captured after this function call. If False,
                              the device may return a previously captured scan 
                              if available.

        Returns:
            WAScan: Measurement data.
        """
        pass

    @validate_call
    def __get_device_info(self):
        """
        Get device information.

        Returns:
            dict: Device information.

        Raises:
            ConnectionError: If the HTTP request fails.
            ValueError: If the JSON response cannot be decoded.
            RuntimeError: If any other error occurs.
        """
        url = f"{self.base_url}/info" 
        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise ConnectionError(f"HTTP request failed: {exc}")
        except json.JSONDecodeError as e:
             raise ValueError(f"Failed to decode JSON response from {url}: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to get device info: {e}")

class WaveAnalyzer1500S(WaveAnalyzer): 
    """
    WaveAnalyzer1500S device class. This class implements the specific methods for the 1500S model.
    """
    @validate_call
    def __init__(self, address : str, preset: bool = True):
        """
        Initialize the WaveAnalyzer1500S device.

        Args:
            address (str): Device network address.
            preset (bool): If True, the device is set to the default scan profile.
        """
        super().__init__(address, preset=preset) # Call parent constructor
        self.scanmodes = {
                "Normal":"Normal", 
                "Normal20MHz":"Normal20MHz",
                "HighSens":"HighSens", 
                "HighSens20MHz":"HighSens20MHz",
                }
        self.rbw = 150 # RBW of 1500S is always 150MHz

        if preset:
            # Set default scan configuration
            self.set_scan()

    @validate_call
    def get_scan_modes(self) -> list[str]:
        """
        Get the list of available scan modes for the 1500S model.

        Returns:
            list[str]: List of available scan modes.
        """
        return self.scanmodes.keys()
    
    @validate_call
    def _validate_scan_mode(self, scan_mode: str) -> str:
        """
        Validate the scan mode for the 1500S model.

        Args:
            scan_mode (str): The scan mode to validate.

        Returns:
            str: The validated scan mode.

        Raises:
            ValueError: If the scan mode is not recognized.
        """
        if scan_mode not in self.scanmodes:
            raise ValueError(f"Invalid scan mode '{scan_mode}'. Available modes: {list(self.scanmodes.keys())}")
        return self.scanmodes[scan_mode]

    @validate_call
    def __download_data(self, blocking: bool = True) -> WAScan:
        """
        Download measurement data from the device.

        Args:
            blocking (bool): If True, wait for the scan to complete.

        Returns:
            WAScan: Measurement data.

        Raises:
            ValueError: If the data cannot be decoded or validated.
        """
        url = f"{self.base_url}/{'linear'}data/bin"
        response = httpx.get(url, timeout=10)
        header = None
        ret_bytes = None
        while True:
            if response.status_code == 404:
                raise ValueError("Error: Triggering is not supported for this device")
            elif response.status_code != 200:
                raise ValueError(f"Error: {response.status_code}")
            ret_bytes = response.content
            # Extract header from first 1000 bytes filtering out non-printable characters.
            try:
                header_str = "".join(filter(lambda x: x in string.printable, ret_bytes[:1000].decode("utf-8", errors='ignore'))) 
            except Exception as e:
                 raise ValueError(f"Failed to decode header bytes: {e}")
            try:
                header = json.loads(header_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to decode header JSON: {e} - Header string received: '{header_str}'")

            if header.get('id', -1) != 0 or not blocking: 
                break
            response = httpx.get(url, timeout=10) # Re-fetch if blocking and id is 0

        data = ret_bytes[1000:]
        dt_names = ["Frequency", "Absolute Power", "Power X-Polarization", "Power Y-Polarization", "Flag"]
        dt_formats = [np.int32, np.float32, np.float32, np.float32, np.int32]
        
        try:
            if not data:
                 raise ValueError("Received empty data buffer after header.")
            data_arr = np.ravel(np.frombuffer(data, dtype=np.dtype({"names": dt_names, "formats": dt_formats})))
        except ValueError as e:
             raise ValueError(f"Failed to interpret data buffer (size: {len(data)}) with dtype {dt_formats}: {e}")

        try:
            scan_data = {
                "scanid": header.get("id", -1), 
                "is_valid": header.get("id", -1) >= 0,
                "power_unit": "mW",
                "rbw": self.rbw,
                "data": data_arr
            }
            return WAScan(**scan_data)
        except ValidationError as e:
            raise ValueError(f"Failed to validate WAScan data: {e}")
        
    @validate_call
    def measure(self, force_new: bool = False) -> WAScan:
        """
        Fetch measurement data from the device.

        Args:
            force_new (bool): If True, the returned measurement is guaranteed to be captured after this function call.

        Returns:
            WAScan: Measurement data.
        """
        if force_new:
            # Wait for the scan to complete
            last_scanid = -1
            while last_scanid in [-1, 0]:
                last_scanid = self.scan_info.scanid
            while True:
                scan_info = self.scan_info
                if scan_info.scanid not in [-1,0] and scan_info.scanid != last_scanid:
                    break
                if scan_info.scanid not in [-1,0]:
                    last_scanid = scan_info.scanid
        return self.__download_data(blocking=True)

class _WANewFormatScan(BaseModel):
    """
    WaveAnalyzer scan data class. Contains extra metadata defined in /waveanalyzer routes.
    """
    noise_power: float
    polarization: bool
    port: str
    rbw: int
    scanid: int
    scantype: str
    timestamp: str
    type: str
    power_unit: str
    frequency_unit: str = "MHz"
    data: np.ndarray = Field(default_factory=lambda: np.array([]))
    model_config = ConfigDict(arbitrary_types_allowed = True)
        
    @field_validator('data', mode='before')
    @classmethod
    def check_wa400_data_structure(cls, v):
        """
        Validate the structure of the data field.

        Args:
            v: The value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If the value is not a numpy array.
        """
        if not isinstance(v, np.ndarray):
             raise ValueError("data must be a numpy array")
        return v

    @classmethod
    def to_WAScan(cls, v) -> WAScan:
        """
        Convert _WANewFormatScan to WAScan.

        Args:
            v (_WANewFormatScan): The _WANewFormatScan object to convert.

        Returns:
            WAScan: The converted WAScan object.
        """
        scan_data = {
            "scanid": v.scanid,
            "is_valid": v.scanid >= 0,
            "power_unit": v.power_unit,
            "rbw": v.rbw,
            "data": v.data
        }
        scan_data["metadata"] = {
            "noise_power": v.noise_power,
            "polarization": v.polarization,
            "port": v.port,
            "scantype": v.scantype,
            "timestamp": v.timestamp,
            "type": v.type
        }
        scan_data["data"] = np.empty(v.data.shape[0], dtype=[("Frequency", np.int32), ("Absolute Power", np.float32), ("Power X-Polarization", np.float32), ("Power Y-Polarization", np.float32), ("Flag", np.int32)])
        scan_data["data"]["Frequency"] = v.data["Frequency"]
        scan_data["data"]["Absolute Power"] = v.data["Absolute Power"]
        scan_data["data"]["Flag"] = np.zeros(v.data.shape[0], dtype=np.int32)
        if not v.polarization:
            scan_data["data"]["Power X-Polarization"] = np.zeros(v.data.shape[0], dtype=np.float32)
            scan_data["data"]["Power Y-Polarization"] = np.zeros(v.data.shape[0], dtype=np.float32)
        else:
            scan_data["data"]["Power X-Polarization"] = v.data["Power X-Polarization"]
            scan_data["data"]["Power Y-Polarization"] = v.data["Power Y-Polarization"]
        return WAScan(**scan_data)

class _WaveAnalyzerNewAPI(WaveAnalyzer):
    @validate_call
    def __init__(self, address: str, preset: bool = True):
        """
        Initialize the _WaveAnalyzerNewAPI device.

        Args:
            address (str): Device network address.
            preset (bool): If True, the device is set to the default scan profile.
        """
        super().__init__(address, preset=preset) # Call parent constructor
        self.base_url_new_api = f"http://{address}/waveanalyzer" # Override base_url for /waveanalyzer APIs
        info_dict = self.__get_device_info()
        self.firmware_version = info_dict.get('firmware_version', 'N/A') 
        self.pno = info_dict.get('pno', 'N/A')
        self.info_valid = info_dict.get('result') == 'OK'

        if preset:
            self.set_scan()

    @validate_call
    def __download_measurement_data(self, query: bool = False) -> _WANewFormatScan:
        """
        Download measurement data from the device.

        Args:
            query (bool): If True, query the device for existing data.

        Returns:
            _WANewFormatScan: Measurement data.

        Raises:
            ConnectionError: If the HTTP request fails.
            ValueError: If the data cannot be decoded or validated.
        """
        url = f"{self.base_url_new_api}/data.bin?scale=linear&scantype={'query' if query else 'measure'}"
        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status() # Check for HTTP errors
        except httpx.RequestError as exc:
            raise ConnectionError(f"HTTP request failed: {exc}")

        try:
            header_str = "".join(filter(lambda x: x in string.printable, response.content[:1000].decode("utf-8", errors='ignore')))
            header_dict = json.loads(header_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode header JSON: {e} - Header string: '{header_str}'")
        except Exception as e:
             raise RuntimeError(f"Error processing header: {e}")

        details = header_dict.get("data", {}).get("details", {})
        
        scan_init_data = {
            "noise_power": details.get("noisePower", 0.0),
            "polarization": details.get("polarization", False),
            "port": details.get("port", "N/A"),
            "rbw": details.get("rbw", 0),
            "scanid": details.get("scanid", -1),
            "scantype": details.get("scantype", -1),
            "timestamp": header_dict.get("data", {}).get("timestamp", ""),
            "type": header_dict.get("type", "N/A"),
            "power_unit": "mW"
        }

        if scan_init_data["polarization"]:
            dt_names = ["Frequency", "Absolute Power", "Power X-Polarization", "Power Y-Polarization"]
            dt_formats = [np.int32] + [np.float32]*3
        else:
            dt_names = ["Frequency", "Absolute Power"]
            dt_formats = [np.int32] + [np.float32]
        
        try:
            binary_data = response.content[1000:]
            if not binary_data:
                 raise ValueError("Received empty data buffer after header for /waveanalyzer.")
            scan_init_data["data"] = np.ravel(
                np.frombuffer(binary_data, dtype=np.dtype({"names": dt_names, "formats": dt_formats}))
            )
        except ValueError as e:
             raise ValueError(f"Failed to interpret /waveanalyzer data buffer (size: {len(binary_data)}) with dtype {dt_formats}: {e}")
        except Exception as e:
             raise RuntimeError(f"Error processing /waveanalyzer binary data: {e}")

        try:
            measurement_data = _WANewFormatScan(**scan_init_data)
            return measurement_data
        except ValidationError as e:
            raise ValueError(f"Failed to validate _WANewFormatScan data: {e}")

    @validate_call
    def measure(self, force_new = False):
        """
        Fetch measurement data from the device.

        Args:
            force_new (bool): If True, the returned measurement is guaranteed to be captured after this function call.

        Returns:
            WAScan: Measurement data.
        """
        data = self.__download_measurement_data(query=not force_new)
        return data.to_WAScan(data)

    @validate_call
    def __get_device_info(self):
        """
        Get device information.

        Returns:
            dict: Device information.

        Raises:
            ConnectionError: If the HTTP request fails.
            ValueError: If the JSON response cannot be decoded.
            RuntimeError: If any other error occurs.
        """
        url = f"{self.base_url_new_api}/info"
        try:
            # Get device info from the new API
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise ConnectionError(f"HTTP request failed: {exc}")
        except json.JSONDecodeError as e:
             raise ValueError(f"Failed to decode JSON response from {url}: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to get device info: {e}")
        
class WaveAnalyzer200A(_WaveAnalyzerNewAPI):
    """
    WaveAnalyzer200A device class. This class implements the specific methods for the 200A model.
    Note that WaveAnalyzer200A has a fixed scan profile and does not support scan mode changes.
    """
    @validate_call
    def __init__(self, address: str, preset: bool = True):
        _default_center: int = 193700000
        super().__init__(address, preset=preset) # Call parent constructor

    @validate_call
    def get_scan_modes(self) -> list[str]:
        return ["Normal"]
    
    @validate_call
    def _validate_scan_mode(self, scan_mode: str) -> str:
        if scan_mode != "Normal":
            raise ValueError(f"Invalid scan mode '{scan_mode}'. WaveAnalyzer200A only supports 'Normal' mode.")
        return "Normal"
    
    @validate_call
    def set_scan(self, center: int = 193700000, span: Union[int, Literal["full"]] = "full", scan_mode: Optional[str] = None) -> bool:
        '''
        WaveAnalyzer200A has a fixed scan profile, therefore, only supports full scans. This method ignores center and scan_mode parameters.
        '''
        if scan_mode is not None:
            self._validate_scan_mode(scan_mode)
        if span != "full" and span != -1:
            raise ValueError("WaveAnalyzer200A only supports full scans.")
        return True

class WaveAnalyzer400A(_WaveAnalyzerNewAPI):
    """
    WaveAnalyzer400A device class. This class implements the specific methods for the 400A model.
    """
    @validate_call
    def __init__(self, address: str, preset: bool = True):
        """
        Initialize the WaveAnalyzer400A device.

        Args:
            address (str): Device network address.
            preset (bool): If True, the device is set to the default scan profile.
        """
        self.scanmodes = {
                "Normal":"LowRes",
                "LowRes":"LowRes", 
                "HighRes":"HighRes",
                }

        super().__init__(address, preset=preset) # Call parent constructor

    @validate_call
    def get_scan_modes(self) -> list[str]:
        """
        Get the list of available scan modes for the 400A model.

        Returns:
            list[str]: List of available scan modes.
        """
        return self.scanmodes.keys()
    
    @validate_call
    def _validate_scan_mode(self, scan_mode: str) -> str:
        """
        Validate the scan mode for the 400A model.

        Args:
            scan_mode (str): The scan mode to validate.

        Returns:
            str: The validated scan mode.

        Raises:
            ValueError: If the scan mode is not recognized.
        """
        if scan_mode not in self.scanmodes:
            raise ValueError(f"Invalid scan mode '{scan_mode}'. Available modes: {list(self.scanmodes.keys())}")
        return self.scanmodes[scan_mode]
   

class WaveAnalyzer1500B(_WaveAnalyzerNewAPI):
    """
    WaveAnalyzer1500B device class. This class implements the specific methods for the 1500B model.
    """
    @validate_call
    def __init__(self, address: str, preset: bool = True):
        """
        Initialize the WaveAnalyzer1500B device.

        Args:
            address (str): Device network address.
            preset (bool): If True, the device is set to the default scan profile.
        """
        self.scanmodes = {
                "Normal":"LowRes",
                "LowRes":"LowRes", 
                "HighRes":"HighRes",
                }

        super().__init__(address, preset=preset) # Call parent constructor

    @validate_call
    def get_scan_modes(self) -> list[str]:
        """
        Get the list of available scan modes for the 1500B model.

        Returns:
            list[str]: List of available scan modes.
        """
        return self.scanmodes.keys()
    
    @validate_call
    def _validate_scan_mode(self, scan_mode: str) -> str:
        """
        (Not yet in effect) Validate the scan mode for the 1500B model. (For 1500B, the scan modes are currently not validated)

        Args:
            scan_mode (str): The scan mode to validate.

        Returns:
            str: The validated scan mode.
        """
        return scan_mode
        

@validate_call
def create_waveanalyzer(address: str, preset: bool = True) -> WaveAnalyzer:
    """
    Factory method to create model-specific WaveAnalyzer instance.

    Args:
        address (str): Device network address (e.g., "wa000186.local").
        preset (bool): If True, the device is set default scan profile.

    Returns:
        WaveAnalyzerAPI: Instance of the appropriate API class.
    """
    model = WaveAnalyzer.get_model(address)
    if model == "1500S":
        return WaveAnalyzer1500S(address, preset=preset)
    elif model in ["WA200A"]:
        return WaveAnalyzer200A(address, preset=preset)
    elif model in ["WA400A"]:
        return WaveAnalyzer400A(address, preset=preset)
    elif model in ["1500B"]:
        return WaveAnalyzer1500B(address, preset=preset)
    else:
        raise ValueError(f"Unsupported WaveAnalyzer model: {model}")
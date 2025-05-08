import httpx
import numpy as np
from typing import Union, Optional
from dataclasses import dataclass, field
import json
import string
from io import StringIO

@dataclass
class WaveShaperProfile:
    num_ports: int
    data: np.ndarray = field(default_factory=lambda: np.array([]))  # Structured array with fields:

class WaveShaperAPI:
    def __init__(self, addr):
        self.base_url = f"http://{addr}/waveshaper"
        dev_info = self.__get_device_info()
        self.model : str = dev_info['model']
        self.serial_number : str = dev_info['sno']
        self.version : str = dev_info['ver']
        self.star_frequency_THz : float = dev_info['startfreq']
        self.stop_frequency_THz : float = dev_info['stopfreq']
        self.ip : str = dev_info['ip']
        self.port_count : int = dev_info['portcount']
        self.status : str = dev_info['msg']
        self.extra_info : dict = dict((key,dev_info[key]) for key in dev_info if key not in ['model', 'sno', 'ver', 'startfreq', 'stopfreq', 'ip', 'portcount', 'msg'])

    def __get_device_info(self) -> dict:
        url = f"{self.base_url}/devinfo"
        response = httpx.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to get device info: {response.text}")
        return response.json()

    def get_profile(self) -> WaveShaperProfile:
        url = f"{self.base_url}/getprofile"
        response = httpx.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to get profile: {response.text}")
        dt_names = ["Frequency", "Attenuation", "Phase", "Port"]
        dt_formats =  [np.float32]*3 + [np.int32]
        data_file = StringIO(response.content.decode('utf-8').replace('\t', ' '))
        data = np.genfromtxt(data_file,dtype={'names': dt_names, 'formats': dt_formats})
        return WaveShaperProfile(self.port_count, data)
    
    PARAMETRIC_FILTER_TYPES = ["bandpass", "bandstop", "gaussian"]
    def load_parametric_profile(self, type : str, port : int, center: float, bandwidth: float, attenuation: float) -> bool:
        if type not in WaveShaperAPI.PARAMETRIC_FILTER_TYPES:
            raise ValueError(f"Invalid filter type: {type}, valid options are {WaveShaperAPI.PARAMETRIC_FILTER_TYPES}")
        config_json = json.dumps({"type": type, "port": port, "center": center, "bandwidth": bandwidth, "attn": attenuation})
        url = f"{self.base_url}/loadprofile"
        response = httpx.post(url, data=config_json)
        if response.status_code != 200:
            raise Exception(f"Failed to load parametric profile: {response.text}")
        return json.loads(response.content.decode('utf-8'))["rc"] == 0

    def blockall(self, port : int) -> bool:
        url = f"{self.base_url}/loadprofile"
        config_json = json.dumps({"type": "blockall", "port": port})
        response = httpx.post(url, data=config_json)
        if response.status_code != 200:
            raise Exception(f"Failed to set block all: {response.text}")
        return json.loads(response.content.decode('utf-8'))["rc"] == 0

    def transmit(self, port : int) -> bool:
        url = f"{self.base_url}/loadprofile"
        config_json = json.dumps({"type": "transmit", "port": port})
        response = httpx.post(url, data=config_json)
        if response.status_code != 200:
            raise Exception(f"Failed to set transmit: {response.text}")
        return json.loads(response.content.decode('utf-8'))["rc"] == 0

    def upload_wsp(self, wsp_filename : str) -> bool:
        wsp_file = open(wsp_filename, 'r')
        config_json = json.dumps({"type": "wsp", "wsp": wsp_file.read()})   
        url = f"{self.base_url}/loadprofile"     
        response = httpx.post(url, data=config_json)
        if response.status_code != 200:
            raise Exception(f"Failed to upload WSP file: {response.text}")
        return json.loads(response.content.decode('utf-8'))["rc"] == 0

if __name__ == "__main__":
    import time
    print("WaveShaperAPIs.py is being run directly")
    ws = WaveShaperAPI("ws201558.local")
    print(ws.extra_info)
    '''
    print(ws.get_profile())
    print(ws.load_parametric_profile("bandstop", 2, 193.5, 2, 1))
    time.sleep(10)
    print(ws.blockall(2))
    time.sleep(10)
    print(ws.transmit(2))
    '''
    #print(ws.load_parametric_profile("bandstop", 2, 193.5, 2, 1))
    #time.sleep(10)
    #print(ws.upload_wsp("/home/edwardfan/Downloads/download_2.wsp"))

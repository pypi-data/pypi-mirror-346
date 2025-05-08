import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from WaveShaperAPIs import WaveShaperProfile, WaveShaperAPI

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Waveshaper Profile Example")
        self.resize(1000, 700)
        layout = QtWidgets.QVBoxLayout(self)
        
        # Configuration form for device address and profile parameters.
        form_layout = QtWidgets.QFormLayout()
        
        self.device_addr_edit = QtWidgets.QLineEdit("ws201558.local")
        form_layout.addRow("Device Address:", self.device_addr_edit)
        
        self.filter_type_combo = QtWidgets.QComboBox()
        self.filter_type_combo.addItems(["bandpass", "bandstop", "gaussian"])
        form_layout.addRow("Filter Type:", self.filter_type_combo)
        
        self.port_edit = QtWidgets.QLineEdit("2")
        form_layout.addRow("Port (for configuration):", self.port_edit)
        
        self.center_edit = QtWidgets.QLineEdit("195")
        form_layout.addRow("Center (THz):", self.center_edit)
        
        self.bandwidth_edit = QtWidgets.QLineEdit("1")
        form_layout.addRow("Bandwidth (THz):", self.bandwidth_edit)
        
        self.attenuation_edit = QtWidgets.QLineEdit("4")
        form_layout.addRow("Attenuation (dB):", self.attenuation_edit)
        layout.addLayout(form_layout)
        
        # Group box for port display selection.
        self.ports_group = QtWidgets.QGroupBox("Display Ports")
        self.ports_layout = QtWidgets.QHBoxLayout()
        self.ports_group.setLayout(self.ports_layout)
        layout.addWidget(self.ports_group)
        self.port_checkboxes = {}
        
        # Create two PlotWidgets: one for attenuation and one for phase.
        self.atten_plot = pg.PlotWidget(title="Attenuation vs Frequency for All Ports")
        self.atten_plot.setLabel('bottom', "Frequency (THz)")
        self.atten_plot.setLabel('left', "Attenuation (dB)")
        layout.addWidget(self.atten_plot)
        
        self.phase_plot = pg.PlotWidget(title="Phase vs Frequency for All Ports")
        self.phase_plot.setLabel('bottom', "Frequency (THz)")
        self.phase_plot.setLabel('left', "Phase (rad)")
        layout.addWidget(self.phase_plot)
        
        # Buttons section.
        btn_layout = QtWidgets.QHBoxLayout()
        
        self.config_button = QtWidgets.QPushButton("Configure and Download Profile")
        self.config_button.clicked.connect(self.run_example)
        btn_layout.addWidget(self.config_button)
        
        self.info_button = QtWidgets.QPushButton("Show Device Info")
        self.info_button.clicked.connect(self.show_device_info)
        btn_layout.addWidget(self.info_button)
        
        self.read_config_button = QtWidgets.QPushButton("Read Current Config")
        self.read_config_button.clicked.connect(self.read_current_config)
        btn_layout.addWidget(self.read_config_button)
        
        # Button to upload a local .wsp file.
        self.upload_button = QtWidgets.QPushButton("Upload WSP File")
        self.upload_button.clicked.connect(self.upload_wsp_file)
        btn_layout.addWidget(self.upload_button)
        
        # New: Button to export readback config to a .wsp file.
        self.export_button = QtWidgets.QPushButton("Export Config to .wsp")
        self.export_button.clicked.connect(self.export_config)
        btn_layout.addWidget(self.export_button)
        
        layout.addLayout(btn_layout)
        
        self.ws_api = None
        self.colors = ['b', 'r', 'g', 'c', 'm', 'y']
    
    def run_example(self):
        try:
            device_addr = self.device_addr_edit.text().strip()
            filt_type = self.filter_type_combo.currentText()
            config_port = int(self.port_edit.text())
            center = float(self.center_edit.text())
            bandwidth = float(self.bandwidth_edit.text())
            attenuation = float(self.attenuation_edit.text())
            
            self.ws_api = WaveShaperAPI(device_addr)
            response = self.ws_api.load_parametric_profile(
                type=filt_type, 
                port=config_port, 
                center=center, 
                bandwidth=bandwidth, 
                attenuation=attenuation
            )
            print("Configuration response:", response)
            self.plot_profile()
        except Exception as e:
            print("Error during configuration or profile retrieval:", e)
    
    def read_current_config(self):
        try:
            if not self.ws_api:
                device_addr = self.device_addr_edit.text().strip()
                self.ws_api = WaveShaperAPI(device_addr)
            self.plot_profile()
        except Exception as e:
            print("Error reading current config:", e)
    
    def update_port_checkboxes(self, ports):
        for i in reversed(range(self.ports_layout.count())):
            widget = self.ports_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.port_checkboxes = {}
        for p in sorted(ports):
            cb = QtWidgets.QCheckBox(f"Port {p}")
            cb.setChecked(True)
            cb.stateChanged.connect(self.plot_profile)
            self.port_checkboxes[p] = cb
            self.ports_layout.addWidget(cb)
    
    def plot_profile(self):
        profile: WaveShaperProfile = self.ws_api.get_profile()
        data = profile.data
        if data.size == 0:
            print("No profile data available.")
            return
        
        unique_ports = np.unique(data['Port'])
        self.update_port_checkboxes(unique_ports)
        
        self.atten_plot.clear()
        self.phase_plot.clear()
        
        for idx, p in enumerate(sorted(unique_ports)):
            if p in self.port_checkboxes and not self.port_checkboxes[p].isChecked():
                continue
            mask = (data['Port'] == p)
            freq = data['Frequency'][mask]
            attn = data['Attenuation'][mask]
            phase = data['Phase'][mask]
            color = self.colors[idx % len(self.colors)]
            self.atten_plot.plot(freq, attn, pen=color, symbol='o', symbolSize=5,
                                 symbolBrush=color, name=f"Port {p}")
            self.phase_plot.plot(freq, phase, pen=color, symbol='x', symbolSize=5,
                                 symbolBrush=color, name=f"Port {p}")
    
    def upload_wsp_file(self):
        try:
            # Open a file dialog to select a .wsp file.
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select WSP File", "", "WSP Files (*.wsp);;All Files (*)")
            if not filename:
                return
            if not self.ws_api:
                device_addr = self.device_addr_edit.text().strip()
                self.ws_api = WaveShaperAPI(device_addr)
            response = self.ws_api.upload_wsp(filename)
            print("Upload response:", response)
            QtWidgets.QMessageBox.information(self, "Upload WSP", f"Upload successful:\n{response}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Upload WSP", f"Error uploading WSP file: {str(e)}")
    
    def export_config(self):
        try:
            if not self.ws_api:
                QtWidgets.QMessageBox.warning(self, "Export Config", "No device connection available.")
                return
            # Retrieve current profile/config from the device.
            profile: WaveShaperProfile = self.ws_api.get_profile()
            data = profile.data
            if data.size == 0:
                QtWidgets.QMessageBox.warning(self, "Export Config", "No profile data available to export.")
                return
            # Open file dialog to select export file location.
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Config", "", "WSP Files (*.wsp);;All Files (*)")
            if not filename:
                return
            # Write profile data to selected file in tab-separated format.
            with open(filename, "w") as f:
                for row in data:
                    f.write(f"{row['Frequency']:.3f}\t{row['Attenuation']:.2f}\t{row['Phase']:.2f}\t{row['Port']}\n")
            QtWidgets.QMessageBox.information(self, "Export Config", "Configuration exported successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Export Config", f"Error exporting configuration: {str(e)}")
    
    def show_device_info(self):
        try:
            if not self.ws_api:
                device_addr = self.device_addr_edit.text().strip()
                self.ws_api = WaveShaperAPI(device_addr)
            info = (f"Model: {self.ws_api.model}\n"
                    f"Serial Number: {self.ws_api.serial_number}\n"
                    f"Version: {self.ws_api.version}\n"
                    f"Start Frequency (THz): {self.ws_api.star_frequency_THz}\n"
                    f"Stop Frequency (THz): {self.ws_api.stop_frequency_THz}\n"
                    f"IP: {self.ws_api.ip}\n"
                    f"Port Count: {self.ws_api.port_count}\n"
                    f"Status: {self.ws_api.status}")
            QtWidgets.QMessageBox.information(self, "Device Info", info)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Device Info", f"Error retrieving device info: {str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
"""Wave Analyzer GUI Example"""

import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from scipy.signal import find_peaks, savgol_filter  # Import savgol_filter
import sys, os
parent_dir = ".."
sys.path.append(parent_dir)

try:
    from wavetools import WaveAnalyzer, create_waveanalyzer
except ImportError:
    from ..WaveAnalyzers import create_waveanalyzer, WaveAnalyzer # for development environment 
import json  # For pretty printing info

class MainWindow(QtWidgets.QWidget):
    def __init__(self, update_interval=2000, parent=None):
        super().__init__(parent)
        self.api: WaveAnalyzer | None = None  # Type hint for API object
        self.update_interval = update_interval
        self.peak_labels = []  # List to hold text items for peak frequency labels
        self.avg_freq_step_mhz = None  # Store average frequency step

        # Main layout.
        main_layout = QtWidgets.QVBoxLayout(self)

        # Create a horizontal layout for the two configuration sections.
        top_layout = QtWidgets.QHBoxLayout()

        # -- Device Configuration Group --
        device_group = QtWidgets.QGroupBox("Device Configuration")
        device_layout = QtWidgets.QFormLayout(device_group)
        # Default IP, user can change this
        self.ip_edit = QtWidgets.QLineEdit("wa000186.local")
        device_layout.addRow("IP Address:", self.ip_edit)
        self.connect_button = QtWidgets.QPushButton("Connect / Update Device")
        self.connect_button.clicked.connect(self.connect_device)
        device_layout.addRow(self.connect_button)
        # Button to display device info.
        self.device_info_button = QtWidgets.QPushButton("Show Device Info")
        self.device_info_button.clicked.connect(self.show_device_info)
        self.device_info_button.setEnabled(False)
        device_layout.addRow(self.device_info_button)

        # -- Scan Configuration Group --
        self.scan_group = QtWidgets.QGroupBox("Scan Configuration")
        self.scan_group.setEnabled(False)  # Enable only after connection.
        scan_layout = QtWidgets.QFormLayout(self.scan_group)
        self.center_edit = QtWidgets.QLineEdit("193700000")
        scan_layout.addRow("Center (MHz):", self.center_edit)
        
        # --- Span Input and Full Span Checkbox ---
        span_layout = QtWidgets.QHBoxLayout() # Layout for span edit and checkbox
        self.span_edit = QtWidgets.QLineEdit("-1")
        span_layout.addWidget(self.span_edit)
        self.full_span_checkbox = QtWidgets.QCheckBox("Full Span")
        self.full_span_checkbox.stateChanged.connect(self.toggle_span_input)
        span_layout.addWidget(self.full_span_checkbox)
        scan_layout.addRow("Span (MHz):", span_layout) # Add the combined layout
        # --- End Span Input ---

        # --- Scan Mode Dropdown ---
        self.scan_mode_combo = QtWidgets.QComboBox()
        scan_layout.addRow("Scan Mode:", self.scan_mode_combo)
        # --- End Scan Mode Dropdown ---

        # Checkbox for switching between linear and logarithmic display modes.
        self.mode_checkbox = QtWidgets.QCheckBox("Linear Display (mW)")
        self.mode_checkbox.setChecked(False)  # Default to logarithmic (dBm)
        self.mode_checkbox.stateChanged.connect(self.update_plot_mode)  # Update plot on change
        scan_layout.addRow("Display Mode:", self.mode_checkbox)

        # --- Peak Finding Controls ---
        self.peak_checkbox = QtWidgets.QCheckBox("Mark Top N Peaks")
        scan_layout.addRow("Mark Peaks:", self.peak_checkbox)
        
        peak_n_layout = QtWidgets.QHBoxLayout()
        self.peak_n_edit = QtWidgets.QLineEdit("3")
        self.peak_n_edit.setMaximumWidth(50)
        peak_n_layout.addWidget(self.peak_n_edit)
        peak_n_layout.addWidget(QtWidgets.QLabel("peaks"))
        scan_layout.addRow("Number of Peaks:", peak_n_layout)

        peak_dist_layout = QtWidgets.QHBoxLayout()
        self.peak_dist_edit = QtWidgets.QLineEdit("1000") # Default distance 100 MHz
        self.peak_dist_edit.setMaximumWidth(50)
        peak_dist_layout.addWidget(self.peak_dist_edit)
        peak_dist_layout.addWidget(QtWidgets.QLabel("MHz"))
        scan_layout.addRow("Min Peak Distance:", peak_dist_layout)
        # --- End Peak Finding Controls ---


        # Polarization checkboxes (will be enabled/disabled based on data)
        self.pol_x_checkbox = QtWidgets.QCheckBox("Show X-Polarization")
        self.pol_x_checkbox.setEnabled(False)
        scan_layout.addRow("X-Polarization:", self.pol_x_checkbox)
        self.pol_y_checkbox = QtWidgets.QCheckBox("Show Y-Polarization")
        self.pol_y_checkbox.setEnabled(False)
        scan_layout.addRow("Y-Polarization:", self.pol_y_checkbox)

        # --- Savitzky-Golay Filter ---
        self.sg_filter_checkbox = QtWidgets.QCheckBox("Apply S-G Filter")
        scan_layout.addRow("Filter Data:", self.sg_filter_checkbox)
        self.sg_rbw_edit = QtWidgets.QLineEdit("100")  # Default RBW in MHz
        self.sg_rbw_edit.setMaximumWidth(50)
        scan_layout.addRow("Filter RBW (MHz):", self.sg_rbw_edit)
        # --- End S-G Filter ---

        self.apply_button = QtWidgets.QPushButton("Apply Scan")
        self.apply_button.clicked.connect(self.apply_scan_config)
        scan_layout.addRow(self.apply_button)
        # Button to display scan info.
        self.info_button = QtWidgets.QPushButton("Show Scan Info")
        self.info_button.clicked.connect(self.show_scan_info)
        scan_layout.addRow(self.info_button)

        # Add the two groups to the top horizontal layout.
        top_layout.addWidget(device_group)
        top_layout.addWidget(self.scan_group)
        main_layout.addLayout(top_layout)

        # -- Plot Widget --
        self.plotWidget = pg.PlotWidget(title="Frequency vs Absolute Power")
        self.plotWidget.setLabel('bottom', "Frequency", units='THz')
        # Initially, the label is set based on checkbox state.
        initial_unit = 'mW' if self.mode_checkbox.isChecked() else 'dBm'
        self.plotWidget.setLabel('left', "Absolute Power", units=initial_unit)
        main_layout.addWidget(self.plotWidget)
        self.curve = self.plotWidget.plot(pen='y')
        # Scatter plot item for peak markers.
        self.peak_scatter = pg.ScatterPlotItem(size=10, pen=pg.mkPen('r'), brush=pg.mkBrush('r'))
        self.plotWidget.addItem(self.peak_scatter)
        # Polarization curves
        self.pol_curve_x = self.plotWidget.plot(pen='g')  # X-pol curve
        self.pol_curve_y = self.plotWidget.plot(pen='b')  # Y-pol curve

        # -- Scan ID Display (below the chart) --
        self.scan_id_field = QtWidgets.QLineEdit()
        self.scan_id_field.setReadOnly(True)
        self.scan_id_field.setPlaceholderText("Scan ID will be shown here")
        main_layout.addWidget(self.scan_id_field)

        # -- Total Power Display (below the chart) -- # Renamed from Average Power
        self.total_power_field = QtWidgets.QLineEdit()
        self.total_power_field.setReadOnly(True)
        self.total_power_field.setPlaceholderText("Total Power will be shown here")
        main_layout.addWidget(self.total_power_field)

        # -- Average Frequency Step Size Display --
        self.avg_step_field = QtWidgets.QLineEdit()
        self.avg_step_field.setReadOnly(True)
        self.avg_step_field.setPlaceholderText("Average Frequency Step Size (MHz)")
        main_layout.addWidget(self.avg_step_field)

        # -- Metadata Display --
        self.metadata_field = QtWidgets.QLineEdit()
        self.metadata_field.setReadOnly(True)
        self.metadata_field.setPlaceholderText("Scan Metadata")
        main_layout.addWidget(self.metadata_field)

        # -- Timer for continuous updates --
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        # Start timer only after successful connection
        # self.timer.start(self.update_interval)

    def connect_device(self):
        ip = self.ip_edit.text().strip()
        try:
            # Use the factory function to create the appropriate API instance
            self.api = create_waveanalyzer(ip)
            print(f"Connected to device: {self.api.__class__.__name__}")
            print(f"  Version: {getattr(self.api, 'version', 'N/A')}")  # Use getattr for safety
            print(f"  Firmware: {getattr(self.api, 'firmware_version', 'N/A')}")

            # --- Populate Scan Modes ---
            try:
                scan_modes = self.api.get_scan_modes()
                self.scan_mode_combo.clear()
                if scan_modes:
                    self.scan_mode_combo.addItems(scan_modes)
                    self.scan_mode_combo.setCurrentIndex(-1)  # Do not select a default mode
                    print(f"  Available scan modes: {scan_modes}")
                else:
                    print("  No scan modes reported by device.")
                self.scan_mode_combo.setEnabled(bool(scan_modes))  # Enable if modes exist
            except Exception as mode_err:
                print(f"  Warning: Could not get scan modes: {mode_err}")
                self.scan_mode_combo.clear()
                self.scan_mode_combo.setEnabled(False)
            # --- End Populate Scan Modes ---

            self.scan_group.setEnabled(True)
            self.device_info_button.setEnabled(True)
            self.timer.start(self.update_interval)  # Start updates after connection

            # Optionally apply the default scan config immediately
            # self.apply_scan_config()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Connection Error", f"Error connecting to device: {e}")
            self.scan_group.setEnabled(False)
            self.device_info_button.setEnabled(False)
            self.timer.stop()  # Stop updates on error
            self.api = None  # Ensure API is None on error

    def toggle_span_input(self, state):
        """Enable/disable the span input field based on the 'Full Span' checkbox."""
        if state == QtCore.Qt.Checked:
            self.span_edit.setEnabled(False)
            self.span_edit.setText("-1") # Set to -1 when disabled, as this often means full span
        else:
            self.span_edit.setEnabled(True)

    def apply_scan_config(self):
        if not self.api:
            QtWidgets.QMessageBox.warning(self, "Scan Config", "Device not connected!")
            return
        try:
            center = int(self.center_edit.text())
            
            # Determine span based on checkbox state
            if self.full_span_checkbox.isChecked():
                span = "full"
            else:
                span = int(self.span_edit.text()) # Get span from the text field
                
            # Get selected scan mode (tag) from the dropdown
            tag = self.scan_mode_combo.currentText()
            if not tag:
                QtWidgets.QMessageBox.warning(self, "Scan Config", "No scan mode selected!")
                return

            success = self.api.set_scan(center, span, tag)
            if not success:
                # API returns True on success, raises error otherwise
                QtWidgets.QMessageBox.warning(self, "Scan Config", "Failed to apply scan config (API returned False or raised an error).")
            else:
                print(f"Scan configuration applied successfully: Center={center}, Span={span}, Mode='{tag}'")
                # Force an immediate plot update after applying config
                self.update_plot()
        except ValueError as e:
             QtWidgets.QMessageBox.critical(self, "Scan Config Error", f"Invalid number/format for Center or Span. Original message {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Scan Config Error", f"Error applying scan configuration: {e}")

    def update_plot_mode(self):
        """Forces plot update when display mode changes."""
        self.update_plot()

    def update_y_axis_label(self, unit):
        """Updates the Y-axis label based on the power unit."""
        self.plotWidget.setLabel('left', "Absolute Power", units=unit)

    def _apply_sg_filter(self, data_mw, polyorder=2):  # Renamed parameter to indicate input is mW
        """Applies Savitzky-Golay filter based on GUI settings to linear (mW) data."""
        if data_mw is None: # Handle case where input data might be None (e.g., polarization)
            return None
        if not self.sg_filter_checkbox.isChecked() or self.avg_freq_step_mhz is None or self.avg_freq_step_mhz <= 0:
            return data_mw  # Return original linear data if filter disabled or step size invalid

        try:
            rbw_mhz = float(self.sg_rbw_edit.text())
            if rbw_mhz == 0: # Check if RBW is explicitly set to 0
                print("RBW is 0, returning unfiltered data.")
                return data_mw # Return original data if RBW is 0
            if rbw_mhz < 0: # Check for negative RBW
                print("Warning: Invalid RBW for S-G filter, must be non-negative.")
                return data_mw
        except ValueError:
            print("Warning: Invalid RBW value for S-G filter.")
            return data_mw

        # Calculate window length based on RBW and average step size
        window_length = int(round(rbw_mhz / self.avg_freq_step_mhz))

        # Ensure window_length is odd and >= polyorder + 1
        if window_length % 2 == 0:
            window_length += 1
        window_length = max(window_length, polyorder + 1)

        # Ensure window_length is not larger than data size
        if window_length > len(data_mw):
            print(f"Warning: Calculated S-G window length ({window_length}) too large for data size ({len(data_mw)}). Using max possible odd length.")
            window_length = len(data_mw) if len(data_mw) % 2 != 0 else len(data_mw) - 1
            if window_length < polyorder + 1:
                print("Warning: Data size too small for S-G filter with chosen polyorder.")
                return data_mw  # Cannot apply filter

        try:
            # Apply the filter to the linear data
            # savgol_filter returns a new array (copy)
            filtered_data_mw = savgol_filter(data_mw, window_length, polyorder)
            # Ensure non-negativity before potential log conversion later
            # Use np.maximum to create a new array if modification is needed
            epsilon = 1e-10
            filtered_data_mw = np.maximum(filtered_data_mw, epsilon) 
            return filtered_data_mw
        except Exception as e:
            print(f"Error applying S-G filter: {e}")
            return data_mw  # Return original linear data on filter error

    def update_plot(self):
        if not self.api:
            return
        try:
            # Use measure() method
            scan = self.api.measure(force_new=False)

            if not scan or not hasattr(scan, 'is_valid') or not scan.is_valid:  # Check if scan is valid
                print("Waiting for valid scan data...")
                return  # Skip update if scan is invalid

            # Determine display mode and units
            linear_display = self.mode_checkbox.isChecked()
            unit = 'mW' if linear_display else 'dBm'
            self.update_y_axis_label(unit)

            # Use the frequency_THz property for plotting
            frequencies_thz = scan.frequency_THz

            # --- Get Linear Power Data ---
            # Make copies to ensure we don't modify the original scan data
            abs_power_mw = np.copy(scan.power_mW)
            pol_x_power_mw = np.copy(scan.power_x_pol_mW) if "Power X-Polarization" in scan.data.dtype.names else None
            pol_y_power_mw = np.copy(scan.power_y_pol_mW) if "Power Y-Polarization" in scan.data.dtype.names else None

            # --- Calculate Average Frequency Step (needed for S-G filter and peak distance) ---
            if scan.data.size > 1:
                freq_steps = np.diff(scan.data["Frequency"])
                self.avg_freq_step_mhz = np.mean(freq_steps)
                self.avg_step_field.setText(f"Avg Step: {self.avg_freq_step_mhz:.3f} MHz")
            elif scan.data.size == 1:
                self.avg_freq_step_mhz = None
                self.avg_step_field.setText("Avg Step: N/A (1 point)")
            else:
                self.avg_freq_step_mhz = None
                self.avg_step_field.clear()

            # --- Apply S-G Filter to Linear Data if enabled (for plotting) ---
            # _apply_sg_filter returns either the original array or a new filtered array
            abs_power_mw_processed = self._apply_sg_filter(abs_power_mw)
            pol_x_power_mw_processed = self._apply_sg_filter(pol_x_power_mw) # Handles None input
            pol_y_power_mw_processed = self._apply_sg_filter(pol_y_power_mw) # Handles None input
            # --- End S-G Filter ---

            # --- Select Data for Plotting based on Display Mode ---
            epsilon = 1e-10 # Define epsilon for log conversion
            if linear_display:
                abs_power_plot = abs_power_mw_processed
                pol_x_power_plot = pol_x_power_mw_processed
                pol_y_power_plot = pol_y_power_mw_processed
            else:
                # Convert processed linear data to dBm for display
                # Use np.maximum to handle potential zero/negative values without modifying the input array in-place
                abs_power_plot = 10 * np.log10(np.maximum(abs_power_mw_processed, epsilon))
                
                pol_x_power_plot = None
                if pol_x_power_mw_processed is not None:
                   pol_x_power_plot = 10 * np.log10(np.maximum(pol_x_power_mw_processed, epsilon))

                pol_y_power_plot = None
                if pol_y_power_mw_processed is not None:
                   pol_y_power_plot = 10 * np.log10(np.maximum(pol_y_power_mw_processed, epsilon))
            # --- End Data Selection ---


            self.curve.setData(frequencies_thz, abs_power_plot)

            # Update Scan ID field using scanid attribute
            self.scan_id_field.setText(f"Scan ID: {scan.scanid}")

            # --- Calculate and display total power ---
            # Use the original unfiltered linear data (abs_power_mw) for summation
            if len(abs_power_mw) > 0 and self.avg_freq_step_mhz is not None and hasattr(scan, 'rbw') and scan.rbw is not None and scan.rbw > 0:
                # Sum the original unfiltered linear power values and scale by RBW ratio
                # This approximates integration assuming power is power density (mW/RBW)
                total_power_mw = np.sum(abs_power_mw) * (self.avg_freq_step_mhz / scan.rbw)

                if linear_display:
                    total_power_display = total_power_mw
                    display_unit = 'mW'
                else:
                    # Convert the total linear power to dBm
                    total_power_mw = max(total_power_mw, epsilon)  # Ensure positive before log
                    total_power_display = 10 * np.log10(total_power_mw)
                    display_unit = 'dBm'

                total_power_text = f"Total Power: {total_power_display:.2f} {display_unit}"
                # No longer add "(Filtered)" as total power always uses unfiltered data now
                
                self.total_power_field.setText(total_power_text)  # Update the correct field
            else:
                self.total_power_field.setText("Total Power: N/A") # Indicate if calculation isn't possible


            # --- Display Metadata ---
            if scan.metadata:
                # Convert metadata dict to a readable string
                metadata_str = json.dumps(scan.metadata, indent=None, separators=(',', ':'))  # Compact JSON
                self.metadata_field.setText(f"Metadata: {metadata_str}")
            else:
                self.metadata_field.clear()


            # --- Peak Finding Logic (use plotted data) ---
            # Clear previous peak markers and labels
            self.peak_scatter.setData(spots=[])
            for label in self.peak_labels:
                self.plotWidget.removeItem(label)
            self.peak_labels = []

            # Use the potentially filtered and converted abs_power_plot for peak finding
            peak_data = abs_power_plot
            if self.peak_checkbox.isChecked() and len(peak_data) > 0:
                try:
                    n = int(self.peak_n_edit.text())
                except ValueError:
                    n = 3  # Default to 3 peaks if input is invalid
                
                # Calculate peak distance in points
                peak_distance_points = None
                if self.avg_freq_step_mhz is not None and self.avg_freq_step_mhz > 0:
                    try:
                        peak_dist_mhz = float(self.peak_dist_edit.text())
                        if peak_dist_mhz > 0:
                            peak_distance_points = int(round(peak_dist_mhz / self.avg_freq_step_mhz))
                    except ValueError:
                        print("Warning: Invalid peak distance value.")
                        peak_distance_points = 1 # Default to minimum distance if invalid

                # Find peaks - adjust parameters (height, distance) as needed
                # Use a reasonable minimum height to avoid noise peaks, especially in dBm mode
                min_height = np.min(peak_data) if len(peak_data) > 0 else None
                if min_height is not None:
                    # Pass distance parameter if calculated
                    peaks, properties = find_peaks(peak_data, height=min_height, distance=peak_distance_points)
                else:
                    peaks = []

                if len(peaks) > 0:
                    # Get indices of the top N peaks based on their height (power)
                    top_peak_indices = peaks[np.argsort(peak_data[peaks])[-n:]]

                    peak_x = frequencies_thz[top_peak_indices]
                    peak_y = peak_data[top_peak_indices]  # Use peak_data here

                    # Update scatter plot for peaks
                    spots = [{'pos': [float(x), float(y)]} for x, y in zip(peak_x, peak_y)]
                    self.peak_scatter.setData(spots=spots)

                    # Add text labels for peaks
                    for x, y in zip(peak_x, peak_y):
                        # Format label text to include both X (Frequency) and Y (Power)
                        label_text = f"{x:.5f} THz<br>{y:.2f} {unit}" # Added Y value and unit
                        text = pg.TextItem(html=f"<div style='color:white;background-color:rgba(0,0,0,0.7);padding:2px;'>{label_text}</div>", 
                                           anchor=(0.5, 1.2)) # Anchor slightly above the point (0.5, 1.2)
                        text.setPos(x, y)
                        self.plotWidget.addItem(text)
                        self.peak_labels.append(text)  # Keep track of labels

            # --- Polarization Plotting Logic ---
            # Check if polarization data exists
            has_pol_x = pol_x_power_plot is not None
            has_pol_y = pol_y_power_plot is not None

            self.pol_x_checkbox.setEnabled(has_pol_x)
            self.pol_y_checkbox.setEnabled(has_pol_y)

            if has_pol_x and self.pol_x_checkbox.isChecked():
                self.pol_curve_x.setData(frequencies_thz, pol_x_power_plot)
            else:
                self.pol_curve_x.clear()  # Clear curve if checkbox is off or no data

            if has_pol_y and self.pol_y_checkbox.isChecked():
                self.pol_curve_y.setData(frequencies_thz, pol_y_power_plot)
            else:
                self.pol_curve_y.clear()  # Clear curve if checkbox is off or no data

        except Exception as e:
            print(f"Error updating plot: {e}")
            import traceback
            traceback.print_exc() # Print full traceback for debugging
            # Optionally stop timer on repeated errors
            # self.timer.stop()

    def show_scan_info(self):
        if not self.api:
            QtWidgets.QMessageBox.warning(self, "Scan Info", "Device not connected!")
            return
        try:
            # get_scan_info might not be available on all concrete implementations
            if hasattr(self.api, 'scan_info'):
                info = self.api.scan_info
                # Use model_dump() for Pydantic models for cleaner string representation
                info_str = json.dumps(info.model_dump(), indent=2)
                QtWidgets.QMessageBox.information(self, "Scan Info", f"<pre>{info_str}</pre>")  # Use pre for formatting
            else:
                QtWidgets.QMessageBox.information(self, "Scan Info", "scan_info not available for this device type.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Scan Info", f"Error retrieving scan info: {e}")

    def show_device_info(self):
        if not self.api:
            QtWidgets.QMessageBox.warning(self, "Device Info", "Device not connected!")
            return
        try:
            # Gather info from API attributes using getattr for safety
            info_lines = [
                f"Type: {self.api.__class__.__name__}",
                f"Model: {getattr(self.api, 'model', 'N/A')}",
                f"Serial Number: {getattr(self.api, 'serial_number', 'N/A')}",
                f"Version: {getattr(self.api, 'version', 'N/A')}",
                f"Vendor: {getattr(self.api, 'vendor', 'N/A')}",
                f"Firmware Version: {getattr(self.api, 'firmware_version', 'N/A')}",
                f"PNO: {getattr(self.api, 'pno', 'N/A')}",  # Present on 400A
                f"Info Valid: {getattr(self.api, 'info_valid', 'N/A')}"  # Present on 400A
            ]
            # Filter out lines where the value is 'N/A' or None
            info = "\n".join(line for line in info_lines if ": N/A" not in line and ": None" not in line)
            QtWidgets.QMessageBox.information(self, "Device Info", info)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Device Info", f"Error retrieving device info: {e}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    # Set update interval (e.g., 2000 ms = 2 seconds)
    window = MainWindow(update_interval=2000)
    window.setWindowTitle("Wave Analyzer Scan Visualization")
    window.resize(900, 700)  # Slightly larger window
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QFont, QColor, QMovie
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QLabel, QTableWidgetItem, QHeaderView, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
import requests
from functools import partial

from .utilities.IOWidget import MINIINPUT
from .layouts.gauge import Gauge
from .layouts import ui_calibrator2
from .interactive.myUtils import CustomGraphicsView
from .utilities.devThread import Command, SCOPESTATES
import numpy as np
import json

class ImageLoaderThread(QThread):
    imageLoaded = pyqtSignal(QPixmap, str)
    errorOccurred = pyqtSignal(str)

    def __init__(self, url, fname):
        super().__init__()
        self.url = url
        self.fname = fname

    def run(self):
        try:
            # Fetch the image from the URL
            image_data = requests.get(self.url).content
            
            # Load the image into a QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            
            # Emit the signal with the loaded image
            self.imageLoaded.emit(pixmap, self.fname)
        except Exception as e:
            self.errorOccurred.emit(str(e))

class Expt(QtWidgets.QWidget, ui_calibrator2.Ui_Form):
    def __init__(self, device, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.device = device  # Device handler passed to the Expt class.
        print(self.device.read_bulk_flash(self.device.ADC_POLYNOMIALS_LOCATION, 100))
        self.selectedChannel = None
        self.dataset_x = []
        self.dataset_y = []
        spingif = os.path.join(os.path.dirname(__file__),'interactive/spin.gif')
        self.loading_movie = QMovie(spingif)  # Path to your spinning icon
        self.loading_movie.setScaledSize(QSize(100, 100))  # Set the size of the movie
        self.calPixmap = None
        self.calName = None
        # Set up UI elements that aren't in the .ui file
        self.setupAdditionalUI()
        
        if not hasattr(self.device, 'aboutArray') or not self.device.calibrated:
            self.calibrationTitle.setText('Device not calibrated')
            self.calibrationTitle.setStyleSheet('color:red;')
            # Display default or empty calibration table
            self.createEmptyCalibrationTable()
        else:
            self.calibrationTitle.setText('Device Calibration Data')
            self.calibrationTitle.setStyleSheet('color:green;')
            # Format and display the calibration data
            self.formatAndDisplayCalibration()
        self.fetchOnlineCalibration()

    def setupAdditionalUI(self):
        """Set up additional UI elements"""
        # Create button row for file operations
        buttonLayout = QtWidgets.QHBoxLayout()        
        
        # Add explanatory text
        helpText = QLabel("Calibration coefficients are used to convert ADC readings to physical units.")
        helpText.setWordWrap(True)
        helpText.setStyleSheet("color: #555; font-style: italic;")
        
        # Add to the main layout - assuming there's a verticalLayout in the UI file
        self.verticalLayout.addWidget(helpText)
        self.verticalLayout.addLayout(buttonLayout)

    def createEmptyCalibrationTable(self):
        """Create an empty table with appropriate headers"""
        headers = ["Channel", "Slope", "Intercept", "Unit"]
        self.calibrationTable.setRowCount(0)
        self.calibrationTable.setColumnCount(len(headers))
        self.calibrationTable.setHorizontalHeaderLabels(headers)
        self.calibrationTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def fetchOnlineCalibration(self):
        import re
        from urllib.parse import quote

        """Fetch online calibration data from device"""
        if not self.device or not self.device.connected:
            QMessageBox.warning(self, "No Device", "No device connected or device not available.")
            return
        s = self.device.read_bulk_flash(self.device.ADC_POLYNOMIALS_LOCATION, 100)
        s = re.sub(r"[\'\"b]", "", s.split(b'\n')[0].decode())
        if len(s) > 24:
            print(s[-24:])
            self.calLabel.setMovie(self.loading_movie)
            self.loading_movie.start()
            fname = s[-24:]
            url = f"https://expeyes.scischool.in:4000/savedcals/{quote(fname)}.png"
            
            # Create and start the image loader thread
            self.imageLoaderThread = ImageLoaderThread(url, fname)
            self.imageLoaderThread.imageLoaded.connect(self.onImageLoaded)
            self.imageLoaderThread.errorOccurred.connect(self.onImageLoadError)
            self.imageLoaderThread.start()
        else:
            QMessageBox.warning(self, "No Calibration", "No calibration timestamp available.")
            print(s)

    def onImageLoaded(self, pixmap, fname):
        """Handle the image loaded signal"""
        self.loading_movie.stop()
        self.calLabel.setPixmap(pixmap)
        self.calPixmap = pixmap
        self.calName = fname
        self.calLabel.mouseReleaseEvent = self.showCalDialog

    def showCalDialog(self,*args):
        if self.calPixmap is None:
            return
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(f"Calibration Process Image | Timestamp : {self.calName}")
        
        # Create a label and set the pixmap
        label = QLabel(dialog)
        label.setPixmap(self.calPixmap)
        
        # Set the layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)
        
        # Show the dialog
        dialog.exec_()

    def onImageLoadError(self, error_message):
        """Handle the error signal"""
        QMessageBox.critical(self, "Error", f"Failed to load image: {error_message}")

    def formatAndDisplayCalibration(self):
        """Format calibration data into a user-friendly table with proper sections for ADC channels"""
        # Use clear headers
        headers = ["Parameter", "Value", "Description"]
        self.calibrationTable.setColumnCount(len(headers))
        self.calibrationTable.setHorizontalHeaderLabels(headers)
        
        # Create structured data for display
        display_data = []
        current_channel = None
        current_section = None

        display_data.append(['--- Analog Inputs ---', 'Values',])
        for a in self.device.analogInputSources:
            p = self.device.analogInputSources[a].polynomials
            display_data.append([f'Channel: {a}', '---Polynomials---'])
            gains = [1,2,4,5,8,10,16,32]
            for i in range(len(p)):
                display_data.append([f'{a} @ {gains[i]}x', '%s X^2 + %s X + %s' % tuple(  ['%.3e' % v for v in p[i]]), ''])
        
        display_data.append(['--- Analog Outputs ---', 'Calibration Polynomial','Applied in addition to'])
        p = self.device.DAC.CHANS['PV1'].polynomial
        praw = self.device.DAC.CHANS['PV1'].VToCode
        display_data.append([f'Channel: PV1', '%s X^2 + %s X + %s' % tuple(  ['%.3e' % v for v in p]), '%s X + %s' % tuple(  ['%.3e' % v for v in praw])])

        p = self.device.DAC.CHANS['PV2'].polynomial
        praw = self.device.DAC.CHANS['PV2'].VToCode
        display_data.append([f'Channel: PV2', '%s X^2 + %s X + %s' % tuple(  ['%.3e' % v for v in p]), '%s X + %s' % tuple(  ['%.3e' % v for v in praw])])


        display_data.append(['--- Meters ---', '---', ''])
        display_data.append(['--- Capacitance ---', self.device.SOCKET_CAPACITANCE, 'Socket Capacitance'])
        display_data.append(['--- Capacitance ---', self.device.currentScalers, 'scalers for [sock,550uA,55uA,5.5uA,.55uA]'])
        display_data.append(['--- Capacitance ---', self.device.CAP_RC_SCALING, 'RC Scale Factor(>1uF)'])
        display_data.append(['--- Resistance ---', self.device.resistanceScaling, 'Scale factor'])
        display_data.append(['--- CCS ---', self.device.currentSourceValue, 'Constant current source scaling'])
        # Populate the table with processed data
        self.calibrationTable.setRowCount(len(display_data))
        
        # Alternating section colors for better readability
        section_colors = [QColor("#e3f2fd"), QColor("#f1f8e9")]  # Light blue, light green
        current_section_color = 0
        current_section_name = None
        
        for row_idx, row_data in enumerate(display_data):
            # Check if this is a section header (they start with ---)
            is_section_header = False
            if isinstance(row_data[0], str) and row_data[0].startswith("---"):
                current_section_name = row_data[0]
                current_section_color = (current_section_color + 1) % len(section_colors)
                is_section_header = True
            
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                
                # Style based on item type
                if is_section_header:  # Section headers
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(section_colors[current_section_color])
                elif col_idx == 0:  # Parameter names
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    
                    # Use subtle background for alternating rows
                    if row_idx % 2 == 0 and not is_section_header:
                        item.setBackground(QColor("#f9f9f9"))
                
                self.calibrationTable.setItem(row_idx, col_idx, item)
        
        # Set up the table appearance
        self.calibrationTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.calibrationTable.verticalHeader().setVisible(False)  # Hide vertical header
        self.calibrationTable.setAlternatingRowColors(True)

    def recalA1(self):
        """Recalibrate A1"""
        self.X2.setText(f'{self.device.analogInputSources["A1"].polynomials[0][2]:.3e}')
        self.X1.setText(f'{self.device.analogInputSources["A1"].polynomials[0][1]:.3e}')
        self.X0.setText(f'{self.device.analogInputSources["A1"].polynomials[0][0]:.3e}')
        self.updatePolynomialLabel()
        self.selectedChannel = "A1"
        #self.formatAndDisplayCalibration()

    def recalA2(self):
        """Recalibrate A2"""
        self.X2.setText(f'{self.device.analogInputSources["A2"].polynomials[0][2]:.3e}')
        self.X1.setText(f'{self.device.analogInputSources["A2"].polynomials[0][1]:.3e}')
        self.X0.setText(f'{self.device.analogInputSources["A2"].polynomials[0][0]:.3e}')
        self.updatePolynomialLabel()
        self.selectedChannel = "A2"
        #self.formatAndDisplayCalibration() 

    def recalA3(self):
        """Recalibrate A3"""
        self.X2.setText(f'{self.device.analogInputSources["A3"].polynomials[0][2]:.3e}')
        self.X1.setText(f'{self.device.analogInputSources["A3"].polynomials[0][1]:.3e}')
        self.X0.setText(f'{self.device.analogInputSources["A3"].polynomials[0][0]:.3e}')
        self.updatePolynomialLabel()
        self.selectedChannel = "A3"
        #self.formatAndDisplayCalibration()

    def updatePolynomialLabel(self):
        """Update the polynomial label"""
        self.dataset_x = []
        self.dataset_y = []
        self.polyLabel.setText(f'{self.X2.text()} X^2 + {self.X1.text()} X + {self.X0.text()}')

    def updatePolynomial(self):
        """Update the polynomial"""
        self.device.analogInputSources[self.selectedChannel].polynomials[0] = np.poly1d([float(self.X2.text()), float(self.X1.text()), float(self.X0.text())])
        gains = [1,2,4,5,8,10,16,32]
        if self.selectedChannel == "A1":
            for a in range(8):
                self.device.analogInputSources["A1"].polynomials[a] = np.poly1d([float(self.X2.text())/gains[a], float(self.X1.text())/gains[a], float(self.X0.text())/gains[a]])
        elif self.selectedChannel == "A2":
            for a in range(8):
                self.device.analogInputSources["A2"].polynomials[a] = np.poly1d([float(self.X2.text())/gains[a], float(self.X1.text())/gains[a], float(self.X0.text())/gains[a]])
        self.formatAndDisplayCalibration()

    def applyGND(self):
        if not self.checkReady():
            return
        self.device.set_gain(self.selectedChannel, 7)
        self.appliedEdit.setText('0')
    def apply3V3(self):
        if not self.checkReady():
            return
        self.device.set_gain(self.selectedChannel, 2)
        self.appliedEdit.setText('3.3')
    def apply5V(self):
        if not self.checkReady():
            return
        self.device.set_gain(self.selectedChannel, 1)
        self.appliedEdit.setText('5')
    def measureRaw(self):
        adcval = self.device.__get_raw_average_voltage__(self.selectedChannel)
        self.measuredValue.setText(f'{adcval:.3f}')       
        self.dataset_x.append(adcval)
        self.dataset_y.append(float(self.appliedEdit.text()))
        self.updateDatasetLabel()


    def checkReady(self):
        self.updateDatasetLabel()
        if self.selectedChannel is None:
            QMessageBox.warning(self, "No Channel Selected", "Please select a channel to calibrate.").exec_()
            return False
        return True

    def popDataset(self):
        self.dataset_x.pop()
        self.dataset_y.pop()
        self.updateDatasetLabel()

    def updateDatasetLabel(self):
        self.datasetLabel.setText(f'{[f"{x:.3f} {y:.3f}" for x,y in zip(self.dataset_x, self.dataset_y) ]}')

    def uploadDataset(self):
        if not self.dataset_x or not self.dataset_y:
            QMessageBox.warning(self, "No Dataset", "No dataset available to upload.")
            return

        # Fit dataset_x vs dataset_y using numpy's polyfit
        degree = 2  # Assuming a quadratic fit is desired
        coefficients = np.polyfit(self.dataset_x, self.dataset_y, degree)
        polynomial = np.poly1d(coefficients)

        # Display the polynomial
        QMessageBox.information(self, "Polynomial Fit", f"Polynomial fit: {polynomial}")

    def getCalibrationDescription(self, param_name):
        """Return descriptive text for known calibration parameters"""
        descriptions = {
            "PV1": "Programmable Voltage Source 1",
            "PV2": "Programmable Voltage Source 2",
            "PV3": "Programmable Voltage Source 3",
            "CH1": "Analog Channel 1",
            "CH2": "Analog Channel 2",
            "CH3": "Analog Channel 3",
            "RESISTANCE": "Resistance measurement",
            "CAPACITANCE": "Capacitance measurement",
            "PCS": "Current source",
            # Add more as needed
        }
        return descriptions.get(param_name, "Calibration parameter")

    def saveCalibrationFile(self):
        """Save calibration data to a JSON file"""
        if not hasattr(self.device, 'aboutArray') or not self.device.calibrated:
            QMessageBox.warning(self, "No Calibration Data", "No calibration data available to save.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Calibration Data", "", "JSON Files (*.json);;All Files (*)")
        if not file_path:
            return
            
        try:
            # Get calibration data from device
            calibration_data = {
                "CAP AND PCS": self.device.read_bulk_flash(self.device.CAP_AND_PCS, 5 + 8 * 4),
                "ADC Polynomials": self.device.read_bulk_flash(self.device.ADC_POLYNOMIALS_LOCATION, 600),
            }
            
            # Write to file
            with open(file_path, 'w') as f:
                json.dump(calibration_data, f, indent=4)
                
            QMessageBox.information(self, "Success", f"Calibration data saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save calibration data: {str(e)}")

    def readCalibrationFile(self):
        """Load calibration data from a JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Calibration Data", "", "JSON Files (*.json);;All Files (*)")
        if not file_path:
            return
            
        try:
            with open(file_path, 'r') as f:
                calibration_data = json.load(f)
                
            # Display the loaded data
            if "aboutArray" in calibration_data:
                self.formatAndDisplayCalibration()
                self.calibrationTitle.setText(f'Calibration Data (from file: {os.path.basename(file_path)})')
                self.calibrationTitle.setStyleSheet('color:blue;')
            else:
                QMessageBox.warning(self, "Invalid Format", "The selected file does not contain valid calibration data.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load calibration data: {str(e)}")

    def readCalibrationDevice(self):
        """Read calibration data from connected device"""
        if not self.device or not self.device.connected:
            QMessageBox.warning(self, "No Device", "No device connected or device not available.")
            return
            
        try:
            # Request fresh calibration data from device
            if hasattr(self.device, 'get_calibration'):
                calibration_data = self.device.get_calibration()
                self.formatAndDisplayCalibration(calibration_data)
                self.calibrationTitle.setText('Device Calibration Data (refreshed)')
                self.calibrationTitle.setStyleSheet('color:green;')
            else:
                QMessageBox.information(self, "Not Supported", "This device does not support reading calibration data directly.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read calibration from device: {str(e)}")

    def saveCalibrationDevice(self):
        """Save current calibration data to device"""
        if not self.device or not self.device.connected:
            QMessageBox.warning(self, "No Device", "No device connected or device not available.")
            return
            
        # Confirm before writing to device
        reply = QMessageBox.question(self, "Confirm Write", 
                                    "Are you sure you want to write calibration data to the device? This may overwrite existing calibration.",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
            
        try:
            # Extract calibration data from the table
            rows = self.calibrationTable.rowCount()
            calibration_data = []
            
            for row in range(rows):
                row_data = []
                for col in range(self.calibrationTable.columnCount()):
                    item = self.calibrationTable.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                calibration_data.append(row_data)
                
            # Call device method to save calibration if available
            if hasattr(self.device, 'save_calibration'):
                self.device.save_calibration(calibration_data)
                QMessageBox.information(self, "Success", "Calibration data saved to device.")
            else:
                QMessageBox.information(self, "Not Supported", "This device does not support writing calibration data directly.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save calibration to device: {str(e)}")


# This section is necessary for running calibrator.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 
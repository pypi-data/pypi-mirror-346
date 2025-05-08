import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap  # Import QPixmap for image handling
from PyQt5.QtWidgets import QGraphicsScene,QGraphicsPixmapItem, QLabel
from PyQt5.QtCore import Qt

from .utilities.IOWidget import MINIINPUT  # Import Qt for alignment
from .layouts.gauge import Gauge
from .layouts import DCOhmsLaw
from .interactive.myUtils import CustomGraphicsView
from .utilities.devThread import Command, SCOPESTATES
import numpy as np
class Expt(QtWidgets.QWidget, DCOhmsLaw.Ui_Form ):
    def __init__(self, device, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.device = device  # Device handler passed to the Expt class.

        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene)
        self.view.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove the frame border
        imagepath = os.path.join(os.path.dirname(__file__),'interactive/res-compare.png')        

        mypxmp = QPixmap(imagepath)
        myimg = QGraphicsPixmapItem(mypxmp)
        myimg.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(myimg)


        self.scope_thread = None
        if 'scope_thread' in kwargs:
            self.scope_thread = kwargs['scope_thread']
            self.running = True


        self.PV1 = MINIINPUT(self, self.device, 'PV1', confirmValues=None, scope_thread=self.scope_thread) #Don't use device directly..
        self.A1 = MINIINPUT(self, self.device, 'A1', confirmValues=None, scope_thread=self.scope_thread) 

        self.gaugeLayout.addWidget(self.PV1)
        self.gaugeLayout.addWidget(self.A1)

        self.imageLayout.addWidget(self.view)

        # Create a QTimer for periodic voltage measurement
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_all)  # Connect the timeout signal to the update method
        self.timer.start(5)  # Start the timer with a 5mS interval

    def update_all(self):
        self.A1.update_vals()
        self.PV1.update_vals()
        self.R2 = self.R2Value.value()
        if self.R2 > 0:
            I = self.A1.last_value/self.R2
            self.currentLabel.setText(f"{1000*I:.2f} mA")
            VR1 = self.PV1.last_value - self.A1.last_value
            if I > 0:
                R1 = float(VR1/I)
                if R1<1:
                    R1 = 0
                self.R1Value.setText(f"{R1:.2f} kΩ")
            else:
                self.R1Value.setText(f"Inf")
        else:
            self.currentLabel.setText("0.00 mA")


# This section is necessary for running new.py as a standalone program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Expt(None)  # Pass None for the device in standalone mode
    window.show()
    sys.exit(app.exec_()) 
import os
import sys

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from serial.tools import list_ports

import serial,time

from eyes17 import eyes
from .layouts import ui_field_vis

class Expt(QMainWindow, ui_field_vis.Ui_MainWindow):
    def __init__(self,device=None, **kwargs):
        super().__init__()
        self.setupUi(self)
        self.p = device
        self.dir = 1
        self.ydir = 1
        self.offset=0
        self.looping = True

        self.laser = None
        self.mag = None
        self.basemag = [0,0,0]
        self.zoomLevel = 1.
        try:
            self.initDevices()
        except Exception as e:
            print('Failed to connect:', e)
            pass

        # Set up the main window layout
        self.setWindowTitle('3D Magnetic Vector Field')
        self.setGeometry(100, 100, 800, 600)

        # Create the 3D vector field using GLViewWidget
        self.view = gl.GLViewWidget()
        axisitem = gl.GLAxisItem()
        self.view.addItem(axisitem)


        self.viewLayout.addWidget(self.view)

        # Display the 3D vector field
        self.pts = 30
        self.scale = 150./self.pts #mm per point.
        self.magscale = 1. # 8mg range should become 1 unit.

        self.baseColor = [0,0,1.,1.]
        self.baseColorButton.setColor([0,0,255], False)

        self.tipColor = [1.,0.2,0.2,1.]
        self.tipColorButton.setColor([255,0,0], False)

        self.create_vector_field()

        self.sensorText = gl.GLTextItem()
        self.sensorText.setData(pos=(-self.pts/2, -self.pts/2, 1), color=(127, 255, 127, 255), text='SENSOR')
        self.view.addItem(self.sensorText)

        self.view.setBackgroundColor(pg.mkColor('#223'))
        self.bgColor = [0.2,0.2,0.2]
        self.bgColorButton.setColor([30,30,30], False)

        self.view.setCameraPosition(distance=self.pts*1.5)
        self.grid = gl.GLGridItem()
        self.grid.scale(2, 2, 1)
        self.view.addItem(self.grid)

        self.xpos=0
        self.ypos=0
        self.timer = QTimer()
        #self.on_button_clicked()

    def initDevices(self):
        available_ports = [a.device for a in  list_ports.comports() if ('ttyACM' in a.device or 'cu' in a.device or 'ttyUSB' in a.device or 'COM' in a.device) and ('Bluetooth' not in a.description) and a.device!=self.p.H.portname]
        print(available_ports)
        if len(available_ports)>0:
            self.laser = serial.Serial(available_ports[0], 115200, timeout=0.5)
            time.sleep(0.2)
            print('residual data', self.laser.read())
            self.laser.write(b'G1 F15000\n')  # Motor speed
            # Home
            self.laser.write(f'G1 X{0} Y{0}\n'.encode('utf-8'))
            print('homing...')

            #self.laser.write(b'G1 F1000\n')  # Motor speed

            self.p.I2C.config(100000)
            print(self.p.get_voltage('A1'))
            #self.mag = self.p.guess_sensor()[0]
            from eyes17.SENSORS import QMC5883L
            self.mag = QMC5883L.connect(self.p.I2C)
            time.sleep(0.5)
            for a in range(10):
                self.mag.getRaw()
            self.basemag = np.array([0,0,0])
        else:
            print('Laser unavailable')
    def start_recording(self):
        self.xpos=0
        self.ypos=0
        self.dir=1
        self.timer.timeout.connect(self.updateEverything)
        self.timer.start(130)
        if self.looping:
            #self.controlsFrame.setEnabled(False)
            self.viewFrame.showFullScreen()

    def stopRecording(self):
        self.timer.disconnect()
        np.save('binarydata.npy', self.vectors)

        hdr = f"Distance Scale:{self.scale}\n"
        hdr += f"Points:{self.pts}\n"

        np.savetxt('txtdata.txt', self.vectormags, fmt='%1.2f', header=hdr)
        self.statusbar.showMessage('Finished', 2000)

    def goHome(self):
        print('homing...')
        self.sensorText.setData(pos=(- self.pts / 2,- self.pts / 2,1))
        self.laser.write(f'G1 X{0} Y{0}\n'.encode('utf-8'))
        self.statusbar.showMessage('homing...',2000)

    def goCenter(self):
        self.laser.write(f'G1 X{self.pts*self.scale/2} Y{self.pts*self.scale/2}\n'.encode('utf-8'))
        self.sensorText.setData(pos=(0,0,1))
        self.statusbar.showMessage('centering...',2000)

    def removeBG(self):
        sum = np.zeros(3)
        avg = 5
        for a in range(avg):
            sum = sum + np.array(self.mag.getRaw())
        self.basemag = sum / avg
        print(sum, self.basemag)

    def setZoom(self,z):
        z /= 20.
        self.zoomLevel = z
        for x in range(self.pts):
            for y in range(self.pts):
                orig = np.array([x - self.pts / 2, y - self.pts / 2, 0])
                vec = self.vectors[x][y]
                start = orig - [vec[0]*z,vec[1]*z,vec[2]*z]
                end = orig + [vec[0]*z,vec[1]*z,vec[2]*z]
                color = np.array([self.baseColor, self.tipColor])

                self.arrows[x][y].setData(pos = [start, end], color = color)

        print(z)

    def clearVectors(self):
        for x in range(self.pts):
            for y in range(self.pts):
                orig = np.array([x - self.pts / 2, y - self.pts / 2, 0])
                color = np.array([self.baseColor, self.tipColor])

                self.arrows[x][y].setData(pos=[orig, orig], color=color)

        print(z)

    def setArrowColor(self,btn):
        self.tipColor = btn.color().getRgbF()
        self.setZoom(self.zoomLevel*20.)

    def setArrowStartColor(self,btn):
        self.baseColor = btn.color().getRgbF()
        self.setZoom(self.zoomLevel*20.)

    def setBGColor(self,btn):
        self.bgColor = btn.color().getRgb()
        self.view.setBackgroundColor(self.bgColor)

    def updateEverything(self):
        m = None
        magnitude=0
        pos = np.array([self.xpos - self.pts / 2, self.ypos - self.pts / 2, 0])
        #pos = self.arrows[self.xpos][self.ypos].pos
        if self.p is not None:
            sum = np.zeros(3)
            avg = 5
            for a in range(avg):
                sum = sum+ np.array(self.mag.getRaw())
            m = sum/avg
            # interchange x, y. y is ok.
            m = m - np.array(self.basemag) #baseline subtraction. with magnet removed.
            x = m[0]
            y = m[2]  #sensor is mounted incorrectly.
            z = m[1]
            magnitude = np.sqrt(m[0]**2+m[1]**2+m[2]**2)
            start = pos-[x*self.magscale*self.zoomLevel,y*self.magscale*self.zoomLevel,z*self.magscale*self.zoomLevel]
            end = pos+[x*self.magscale*self.zoomLevel,y*self.magscale*self.zoomLevel,z*self.magscale*self.zoomLevel]
        else:  # Dummy
            start = pos
            end = pos+[0,0,self.xpos/5]

        self.arrows[self.xpos][self.ypos].setData(pos = [start,end], color=np.array([self.baseColor, self.tipColor]),width=3)
        self.vectors[self.xpos][self.ypos] = np.array([x*self.magscale, y*self.magscale, z*self.magscale])
        self.vectormags[self.xpos][self.ypos] = self.xpos/5
        self.xpos+=self.dir
        if self.xpos==self.pts: #Reached one end. reverse
            self.xpos=self.pts-1
            self.dir=-1
            self.incrementY()
        elif self.xpos==-1:
            self.xpos=0
            self.dir=1
            self.incrementY()

        if self.laser is not None: #Go to new position
            cmd = f'G1 X{self.xpos * self.scale} Y{self.ypos * self.scale}\n'.encode('utf-8')
            self.laser.write(cmd)
            self.sensorText.setData(pos=(self.xpos - self.pts / 2, self.ypos - self.pts / 2, 1))
            self.statusbar.showMessage(f"{cmd}, {self.xpos}, {self.ypos}, {m}, {magnitude}",500)
            #print(cmd, self.xpos, self.ypos, m, magnitude)
        print(magnitude)

    def incrementY(self):
        self.ypos += self.ydir
        if self.ypos == -1:# was in reverse
            self.ypos = 0
            self.ydir *= -1
            self.clearVectors()
            return

        elif self.ypos == self.pts:
            if self.looping:
                self.ydir *= -1
                self.ypos = self.pts - 1
                self.clearVectors()
                return

            self.ypos = 0
            self.timer.disconnect()
            np.save('binarydata.npy', self.vectors)

            hdr = f"Distance Scale:{self.scale}\n"
            hdr += f"Points:{self.pts}\n"

            np.savetxt('txtdata.txt', self.vectormags, fmt='%1.2f', header=hdr)
            self.statusbar.showMessage('Finished',2000)
            print('finished')


    def create_vector_field(self):
        # Create a grid of points in 3D space for the vector field
        self.arrows = [[0 for k in range(self.pts)] for j in range(self.pts)] # 2D plane
        self.vectors = np.zeros([self.pts, self.pts, 3])
        self.vectormags = np.zeros([self.pts, self.pts])

        # Create arrows at each grid point
        for i in range(self.pts):
            for j in range(self.pts):
                #pos = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])  # Convert to NumPy array
                pos = np.array([i - self.pts/2, j- self.pts/2, 0])

                # Create a line for the vector (an arrow can be added if needed)
                arrow = gl.GLLinePlotItem(pos=np.array([pos, pos + [0,0,0]]), color=np.array([[1, 1, 1, 1],[.5 , 1., 0.2, 1]]), width=2)
                arrow.setGLOptions('translucent')

                self.arrows[i][j] = arrow
                self.view.addItem(arrow)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = Expt()
    mw.show()
    sys.exit(app.exec_())

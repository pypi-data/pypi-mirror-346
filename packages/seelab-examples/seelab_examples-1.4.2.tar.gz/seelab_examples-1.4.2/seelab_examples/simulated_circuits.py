'''
Code for viewing I2C sensor data using ExpEYES
Logs data from various sensors.
Author  : Jithin B.P, jithinbp@gmail.com
Date    : Sep-2019
License : GNU GPL version 3
'''
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap, QMovie

from collections import OrderedDict
import time, os.path
import subprocess
import tempfile
import zipfile
import os


from .layouts import ui_simulated_circuits, ui_circuit_row
from .layouts.advancedLoggerTools import LOGGER


class ZoomableGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(ZoomableGraphicsView, self).__init__(parent)
        # Enable antialiasing for smoother edges
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # Enable smooth transformation for better image scaling
        self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.scaleFactor = 1.15  # Define the scale factor for zooming

    def wheelEvent(self, event):
        # Zoom in or out based on the wheel event
        if event.angleDelta().y() > 0:
            self.scale(self.scaleFactor, self.scaleFactor)
        else:
            self.scale(1 / self.scaleFactor, 1 / self.scaleFactor)

class CIRCUITROW(QtWidgets.QWidget, ui_circuit_row.Ui_Form):
    def __init__(self, parent, **kwargs):
        super(CIRCUITROW, self).__init__(parent)
        self.setupUi(self)
        self.url = kwargs.get('url')
        self.schematic_path = kwargs.get('schematic')
        self.result_path = kwargs.get('result')
        self.zip_path = kwargs.get('zip')
        self.titletext = kwargs.get('title')
        self.title.setText(self.titletext)
        if len(kwargs.get('description','')) ==0:
            self.description.setParent(None)
        else:
            self.description.setText(kwargs.get('description'))
        kicad_imagepath = os.path.join(os.path.dirname(__file__),'layouts/kicad-dl.png')

        # Set the background image for the launchButton with aspect ratio maintained
        self.launchButton.setStyleSheet(f"""
            background-image: url({kicad_imagepath});
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
        """)

        # Ensure the button has a size policy that allows resizing
        #self.launchButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Optionally, set a fixed size if needed
        # self.launchButton.setFixedSize(100, 100)  # Example fixed size

        self.scene = QtWidgets.QGraphicsScene()
        self.image.setScene(self.scene)
        spingif = os.path.join(os.path.dirname(__file__),'interactive/spin.gif')
        self.loading_movie = QMovie(spingif)  # Path to your spinning icon
        self.title.setMovie(self.loading_movie)
        self.loading_movie.start()  # Start the spinning animation

        self.image.mousePressEvent = self.handleImageClick  # Connect click event

        self.scene2 = QtWidgets.QGraphicsScene()
        self.image2.setScene(self.scene2)
        self.image2.mousePressEvent = self.handleImage2Click  # Connect click event

        self.network_manager = QNetworkAccessManager()
        self.network_manager2 = QNetworkAccessManager()

        self.network_manager.finished.connect(self._handle_downloaded_image)
        self.network_manager2.finished.connect(self._handle_downloaded_zip)

        if self.url and self.schematic_path:
            image_url = self.url + '/' + self.schematic_path
            if 'http' in self.schematic_path:
                image_url = self.schematic_path
            request = QNetworkRequest(QtCore.QUrl(image_url))
            self.network_manager.get(request)
        else:
            print("Schematic info missing.")

        if self.url and self.result_path:
            image_url = self.url + '/' + self.result_path
            if 'http' in self.result_path:
                image_url = self.result_path
            request = QNetworkRequest(QtCore.QUrl(image_url))
            self.network_manager.get(request)
        else:
            print("Result info missing.")

    def handleImageClick(self, event):
        # Open the image with the native viewer on any mouse click
        self.openImageWithNativeViewer(self.scene)

    def handleImage2Click(self, event):
        # Open the image with the native viewer on any mouse click
        self.openImageWithNativeViewer(self.scene2)

    def openImageWithNativeViewer(self, scene):
        # Assuming the scene has only one item which is the image
        items = scene.items()
        if not items:
            return

        pixmap_item = items[0]
        pixmap = pixmap_item.pixmap()

        # Save the pixmap to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        pixmap.save(temp_file.name, "PNG")
        temp_file.close()

        # Open the image with the native viewer
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['xdg-open', temp_file.name], check=True)
            elif sys.platform.startswith('win'):
                os.startfile(temp_file.name)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', temp_file.name], check=True)
            else:
                print("Unsupported platform")
        except Exception as e:
            print(f"Failed to open image with native viewer: {e}")

    def _handle_downloaded_image(self, reply: QNetworkReply):
        self.loading_movie.stop()
        self.title.setText(self.titletext)
        if reply.error() == QNetworkReply.NoError:
            image_data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self._set_pixmap(pixmap, reply.url().toString())
            print(f"Image downloaded successfully from: {reply.url().toString()}")
        else:
            print(f"Error downloading image from {reply.url().toString()}: {reply.errorString()}")

        reply.deleteLater()

    def _set_pixmap(self, pixmap: QtGui.QPixmap, url):
        pic = QtWidgets.QGraphicsPixmapItem(pixmap)
        if 'schematic' in url:
            self.scene.clear()  # Clear any previous items in the scene
            self.scene.addItem(pic)
            rect = pixmap.rect()  # This returns a QRect
            scene_rect = QtCore.QRectF(rect)  # Convert QRect to QRectF
            self.scene.setSceneRect(scene_rect)  # Set the scene rect with QRectF
            self.image.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        elif 'result' in url:
            self.scene2.clear()  # Clear any previous items in the scene
            self.scene2.addItem(pic)
            rect = pixmap.rect()  # This returns a QRect
            scene_rect = QtCore.QRectF(rect)  # Convert QRect to QRectF
            self.scene2.setSceneRect(scene_rect)  # Set the scene rect with QRectF
            self.image2.fitInView(self.scene2.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        if self.scene.items():
            self.image.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        if self.scene2.items():
            self.image2.fitInView(self.scene2.sceneRect(), QtCore.Qt.KeepAspectRatio)
        super().resizeEvent(event)
    
    def download(self):
        if self.url and self.zip_path:
            zip_url = self.url + '/' + self.zip_path
            if 'http' in self.zip_path:
                zip_url = self.zip_path
            request = QNetworkRequest(QtCore.QUrl(zip_url))
            self.network_manager2.get(request)
        else:
            print("Zip file info missing.")

    def _handle_downloaded_zip(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            zip_data = reply.readAll()
            
            # Check if the data is not empty
            if not zip_data.isEmpty():
                print(f"Downloaded zip file size: {zip_data.size()} bytes")
                
                # Create a temporary file to hold the zip data
                temp_zip_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
                temp_zip_file.write(zip_data)
                temp_zip_file.close()

                # Sanitize the title to create a valid directory name
                sanitized_title = self.title.text().replace(' ', '_')
                temp_dir = os.path.join(tempfile.gettempdir(), sanitized_title)

                # Create the directory if it doesn't exist
                os.makedirs(temp_dir, exist_ok=True)

                # Extract the zip file
                with zipfile.ZipFile(temp_zip_file.name, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Open the directory with the native file explorer
                try:
                    if sys.platform.startswith('linux'):
                        subprocess.run(['xdg-open', temp_dir], check=True)
                    elif sys.platform.startswith('win'):
                        os.startfile(temp_dir)
                    elif sys.platform.startswith('darwin'):
                        subprocess.run(['open', temp_dir], check=True)
                    else:
                        print("Unsupported platform")
                except Exception as e:
                    print(f"Failed to open directory with native file explorer: {e}")

                print(f"Zip file extracted and directory opened: {temp_dir}")
            else:
                print("Downloaded data is empty. Check the URL or server response.")
        else:
            print(f"Error downloading zip file from {reply.url().toString()}: {reply.errorString()}")

        reply.deleteLater()

class Expt(QtWidgets.QWidget, ui_simulated_circuits.Ui_Form):
    def __init__(self, device=None):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.circuitList = []
        self.scan()



    ############ I2C SENSORS #################
    def clearList(self):
        for a in self.circuitList:
            for t in range(3):
                if a is not None:
                    a.setParent(None)
        self.circuitList = []

    def scan(self):
        import requests
        #self.url = "http://localhost:4000/static/eyes/simulations.json"
        self.url = "https://csparkresearch.in/assets/kicad/simulations.json"
        self.baseurl = '/'.join(self.url.split('/')[:-1])
        print(self.url)
        self.clearList()
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            json_data = response.json()  # Parse the response as JSON
            for title, details in json_data['files'].items():
                description = details.get('description', '')
                schematic = details.get('schematic', '')
                result = details.get('result', '')
                zip = details.get('zip', '')
                print(description, schematic, result, zip)
                btn = CIRCUITROW(self,url = self.baseurl, title=title, description=description, zip=zip, schematic=schematic, result = result)
                self.circuitLayout.addWidget(btn)
                self.circuitList.append(btn)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        #for a in x:
        #btn = SENSORROW(self, name=s['name'].split(' ')[0], address=a, description=' '.join(
        #btn.launchButton.clicked.connect(dialog.launch)

if __name__ == '__main__':
    import eyes17.eyes

    dev = eyes17.eyes.open()
    app = QtWidgets.QApplication(sys.argv)

    # translation stuff
    lang = QtCore.QLocale.system().name()
    t = QtCore.QTranslator()
    t.load("lang/" + lang, os.path.dirname(__file__))
    app.installTranslator(t)
    t1 = QtCore.QTranslator()
    t1.load("qt_" + lang,
            QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(t1)

    mw = Expt(dev)
    mw.show()
    sys.exit(app.exec_())
